from unstructured.chunking.basic import chunk_elements
from unstructured.partition.auto import partition
import hashlib


def handle_document(doc):
    # Extract the text from the document
    elements = partition(doc)
    chunks = chunk_elements(elements, overlap_all=True)
    
    # Format each chunk with the required metadata
    formatted_chunks = []
    for chunk in chunks:
        formatted_chunks.append({
            'page_content': chunk.text,
            'metadata': {
                'filename': chunk.metadata.filename,
                'filetype': chunk.metadata.filetype,
                'page_number': chunk.metadata.page_number,
            }
        })
    
    return formatted_chunks

# path  = "test\example.pdf"
# chunks = handle_document(path)

# for chunk in chunks:
#     print(chunk)
#   print("=========== chunk details =========")
#   print("file_name :" , chunk.metadata.filename)
#   # print(""chunk.metadata.file_directory)
#   # print(chunk.metadata.is_continuation)
#   print("page number :",chunk.metadata.page_number)
#   print("chunk type :",chunk.metadata.filetype)
#   print("-"*20)
#   print("\n===================")
#   print(chunk)
#   print("===================")