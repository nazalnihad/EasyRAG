import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
api_key = os.getenv('API_KEY')
genai.configure(api_key=api_key)

# Initialize the model
model = genai.GenerativeModel('gemini-1.5-flash')

def get_response(query, chunks):
    # Construct the prompt
    prompt = f"""
    **User Query:**
    {query}

    **Top 5 Information Chunks:**
    """

    for i, chunk in enumerate(chunks, 1):
        file_name = chunk['metadata'].get('filename', 'Unknown file')
        page_number = chunk['metadata'].get('page_number', 'Unknown page')
        prompt += f"{i}. Chunk: {chunk['chunk']}\n   Source: {file_name}, Page: {page_number}\n\n"

    prompt += """
    **Instructions:**
    1. Answer the query based on the provided best chunk that matches the query the best.
    2. If the information in the chunks does not cover the query, respond with "I can't find info on that" only.
    3.Format the references to the file name and page number in your response exactly like this: (source:filename.pdf,page:X), 
    where filename.pdf is the actual file name and X is the specific page number mention the source at the end only once.If there are no relevant chunks donot mention the source   
    4. Do not mention chunks in the response.
    5. Format your response using Markdown with correct spacing for better readability.

    **Response:**
    """

    # Generate the response
    try:
        response = model.generate_content(prompt)
        if response:
            print(response.text)
        return response.text if response and response.text else "No response generated."
    except Exception as e:
        return f"An error occurred: {str(e)}"