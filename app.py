from flask import Flask, render_template, request, jsonify
import os
import json
from vector_db import VectorDatabase
from doc_handle import handle_document
from langchain_core.documents import Document
from llm_response import get_response

app = Flask(__name__)

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

# Process document
def process_document(file):
    file_path = os.path.join(FOLDER_PATH, file)
    
    # Handle document
    chunks = handle_document(file_path)
    documents = [Document(page_content=chunk['page_content'], metadata=chunk['metadata']) for chunk in chunks]
    
    # Add documents to vector store
    db.add_docs(documents)
    
    # Mark file as processed
    processed_files = load_processed_files()
    processed_files.add(file)
    save_processed_files(processed_files)
    return f"{file} processed and added to the vector store."

@app.route('/')
def index():
    files = [f for f in os.listdir(FOLDER_PATH) if f.endswith('.pdf')]
    processed_files = load_processed_files()
    new_files = [f for f in files if f not in processed_files]
    return render_template('index.html', files=files, new_files=new_files)

@app.route('/process_document', methods=['POST'])
def process_doc():
    file = request.json['file']
    result = process_document(file)
    return jsonify({'message': result})

@app.route('/query', methods=['POST'])
def query():
    query_text = request.json['query']
    search_results = db.perform_similarity_search(query_text, k=5)  # Perform similarity search to get top chunks
    chunks = [{'chunk': res.page_content, 'metadata': res.metadata} for res in search_results]
    
    response_text = get_response(query_text, chunks)
    
    return jsonify({'response': response_text})

@app.route('/get_pdf_content', methods=['POST'])
def get_pdf_content():
    file = request.json['file']
    # Here you would implement the logic to extract and return the PDF content
    # For this example, we'll just return a placeholder
    return jsonify({'content': f"Content of {file} would be displayed here."})

@app.route('/get_new_files', methods=['GET'])
def get_new_files():
    files = [f for f in os.listdir(FOLDER_PATH) if f.endswith('.pdf')]
    processed_files = load_processed_files()
    new_files = [f for f in files if f not in processed_files]
    return jsonify(new_files)

if __name__ == '__main__':
    app.run(debug=True)