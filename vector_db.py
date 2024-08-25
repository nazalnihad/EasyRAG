import faiss
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
import pickle
import os

class VectorDatabase:
    def __init__(self, faiss_index_path="vectorstore.pkl"):
        self.embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        self.faiss_index_path = faiss_index_path
        self.vector_store = self._initialize_vector_store()

    def _initialize_vector_store(self):
        if os.path.exists(self.faiss_index_path):
            print(f"Loading existing vector store from {self.faiss_index_path}")
            with open(self.faiss_index_path, 'rb') as f:
                vector_store = pickle.load(f)
        else:
            print("Creating a new vector store.")
            vector_store = None
        return vector_store

    def add_docs(self, documents):
        if self.vector_store:
            print("Merging documents into the existing vector store.")
            new_vector_store = FAISS.from_documents(documents, self.embeddings)
            self.vector_store.merge_from(new_vector_store)
        else:
            print("Adding documents to a new vector store.")
            self.vector_store = FAISS.from_documents(documents, self.embeddings)
        
        self._save_vector_store()

    def _save_vector_store(self):
        print(f"Saving vector store to {self.faiss_index_path}")
        with open(self.faiss_index_path, 'wb') as f:
            pickle.dump(self.vector_store, f)

    def perform_similarity_search(self, query, k=2):
        if not self.vector_store:
            print("Vector store is empty. Please add documents first.")
            return []

        print(f"Performing similarity search for query: {query}")
        results = self.vector_store.similarity_search(query, k=k)
        if not results:
            print("No results found.")
        else:
            print(f"Found {len(results)} results.")
        return results

