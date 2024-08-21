import faiss
from langchain_community.docstore.in_memory import InMemoryDocstore
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document
from uuid import uuid4
import os
import pickle

# Initialize the HuggingFaceEmbeddings model
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

faiss_index_path = "faiss_index"
docstore_path = "docstore.pkl"

# Check if the FAISS index and document store already exist
if os.path.exists(faiss_index_path) and os.path.exists(docstore_path):
    # Load the existing FAISS vector store and document store
    with open(docstore_path, 'rb') as f:
        docstore = pickle.load(f)
    vector_store = FAISS.load_local(
        faiss_index_path, 
        embeddings=embeddings, 
        allow_dangerous_deserialization=True
    )
    vector_store.docstore = docstore
else:
    # Create a new FAISS index and document store
    index = faiss.IndexFlatL2(len(embeddings.embed_query("hello world")))
    docstore = InMemoryDocstore()
    vector_store = FAISS(
        embedding_function=embeddings,
        index=index,
        docstore=docstore,
        index_to_docstore_id={},
    )

    # Add documents to the vector store
    # documents = [
    #     Document(page_content="I had chocolate chip pancakes and scrambled eggs for breakfast this morning.", metadata={"source": "tweet"}),
    #     Document(page_content="The weather forecast for tomorrow is cloudy and overcast, with a high of 62 degrees.", metadata={"source": "news"}),
    # ]
    # uuids = [str(uuid4()) for _ in range(len(documents))]
    # vector_store.add_documents(documents=documents, ids=uuids)

    # Save the FAISS index and document store for future use
    vector_store.save_local(faiss_index_path)
    with open(docstore_path, 'wb') as f:
        pickle.dump(docstore, f)

# Perform a similarity search
results = vector_store.similarity_search("weather", k=2)

# Print the results
for res in results:
    print(f"* {res.page_content} [{res.metadata}]")