import doc_handle
import vector_db
from langchain_core.documents import Document
import os
import json
import warnings

# Suppress specific FutureWarnings
warnings.filterwarnings("ignore", category=FutureWarning, message=".*clean_up_tokenization_spaces.*")
warnings.filterwarnings("ignore", category=FutureWarning, message=".*torch.load.*")
PROCESSED_FILES_PATH = 'processed_files.json'

def load_processed_files():
    if os.path.exists(PROCESSED_FILES_PATH):
        print(f"Loading processed files from {PROCESSED_FILES_PATH}")
        with open(PROCESSED_FILES_PATH, 'r') as f:
            return set(json.load(f))
    else:
        print(f"{PROCESSED_FILES_PATH} does not exist. Creating it.")
        with open(PROCESSED_FILES_PATH, 'w') as f:
            json.dump([], f)
        return set()

def save_processed_files(processed_files):
    print(f"Saving processed files to {PROCESSED_FILES_PATH}")
    with open(PROCESSED_FILES_PATH, 'w') as f:
        json.dump(list(processed_files), f)

def main(doc_path, query):
    processed_files = load_processed_files()
    filename = os.path.basename(doc_path)
    
    db = vector_db.VectorDatabase()
    
    # Check if file has been processed
    if filename in processed_files:
        response = input(f"The PDF '{filename}' has already been processed. Do you want to skip reprocessing and just get the query results? (y/n): ")
        if response.lower() == 'y':
            print("Fetching query results from existing data...")
            search_results = db.perform_similarity_search(query, k=3)
            for res in search_results:
                print(f"* {res.page_content} [{res.metadata}]")
            return
        else:
            print("Reprocessing the document...")
    
    # Handle document
    chunks = doc_handle.handle_document(doc_path)
    
    # Create Document objects
    documents = [Document(page_content=chunk['page_content'], metadata=chunk['metadata']) for chunk in chunks]
    
    # Add documents to vector store
    db.add_docs(documents)
    
    # Perform similarity search
    search_results = db.perform_similarity_search(query, k=3)
    
    # Print results
    for res in search_results:
        print(f"* {res.page_content} [{res.metadata}]")
    
    # Add filename to processed files list if it's not already there
    if filename not in processed_files:
        processed_files.add(filename)
        save_processed_files(processed_files)
    else:
        print(f"The file '{filename}' is already in the processed files list.")

# Example usage
if __name__ == "__main__":
    document_path = 'test/example.pdf'
    search_query = 'oal has been that the authors do not need to make modifications'
    main(document_path, search_query)
