import streamlit as st
import os
import json
from vector_db import VectorDatabase
from doc_handle import handle_document
from langchain_core.documents import Document

# Constants
FOLDER_PATH = 'test'
PROCESSED_FILES_PATH = 'processed_files.json'
db = VectorDatabase()

# Load processed files
def load_processed_files():
    if os.path.exists(PROCESSED_FILES_PATH):
        with open(PROCESSED_FILES_PATH, 'r') as f:
            return set(json.load(f))
    else:
        return set()

# Save processed files
def save_processed_files(processed_files):
    with open(PROCESSED_FILES_PATH, 'w') as f:
        json.dump(list(processed_files), f)

# Main UI Function
def main_ui():
    st.title("Document Management and Query System")

    # Load processed files
    processed_files = load_processed_files()

    # List documents in the folder
    st.subheader("Documents in Folder")
    files = [f for f in os.listdir(FOLDER_PATH) if f.endswith('.pdf')]
    new_files = [f for f in files if f not in processed_files]

    # Display new files
    st.subheader("New Documents")
    for file in new_files:
        st.write(file)
        if st.button(f"Process {file}"):
            process_document(file, processed_files)
    
    # Query Interface
    st.subheader("Query the Document Store")
    query = st.text_input("Enter your query:")
    if query:
        search_results = db.perform_similarity_search(query, k=3)
        for res in search_results:
            st.write(f"* {res.page_content} [{res.metadata}]")

    # Refresh Button
    if st.button("Refresh Folder"):
        st.experimental_rerun()

def process_document(file, processed_files):
    db = VectorDatabase()
    file_path = os.path.join(FOLDER_PATH, file)
    
    # Handle document
    chunks = handle_document(file_path)
    documents = [Document(page_content=chunk['page_content'], metadata=chunk['metadata']) for chunk in chunks]

    # Add documents to vector store
    db.add_docs(documents)
    
    # Mark file as processed
    processed_files.add(file)
    save_processed_files(processed_files)
    st.success(f"{file} processed and added to the vector store.")

if __name__ == "__main__":
    main_ui()
