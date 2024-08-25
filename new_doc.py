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

def process_and_search(doc_path):
    processed_files = load_processed_files()
    filename = os.path.basename(doc_path)
    
    db = vector_db.VectorDatabase()
    
    # Check if file has been processed
    if filename in processed_files:
        response = input(f"The PDF '{filename}' has already been processed. Do you want to skip reprocessing and just get the query results? (y/n): ")
        if response.lower() == 'y':
            return db
        else:
            print("Reprocessing the document...")
    
    # Handle document
    chunks = doc_handle.handle_document(doc_path)
    
    # Create Document objects
    documents = [Document(page_content=chunk['page_content'], metadata=chunk['metadata']) for chunk in chunks]
    
    # Add documents to vector store
    db.add_docs(documents)
    
    # Add filename to processed files list if it's not already there
    if filename not in processed_files:
        processed_files.add(filename)
        save_processed_files(processed_files)
    
    return db

def main(doc_path):
    db = process_and_search(doc_path)
    
    while True:
        search_query = input("Enter your search query (type 'q' to quit): ")
        if search_query.lower() == 'q':
            print("Exiting...")
            break
        
        # Perform similarity search
        search_results = db.perform_similarity_search(search_query, k=3)
        
        # Print results
        if search_results:
            for res in search_results:
                print(f"* {res.page_content} [{res.metadata}]")
        else:
            print("No results found.")

# Example usage
if __name__ == "__main__":
    document_path = 'test/example.pdf'
    main(document_path)
