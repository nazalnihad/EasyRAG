from unstructured.chunking.basic import chunk_elements
from unstructured.partition.auto import partition


def handle_document(doc):
    # Extract the text from the document
    elements = partition(doc)
    chunks = chunk_elements(elements,overlap_all=True)
    return chunks

path  = "test\example.pdf"
chunks = handle_document(path)

for chunk in chunks:
  print("=========== chunk details =========")
  print("file_name :" , chunk.metadata.filename)
  # print(""chunk.metadata.file_directory)
  # print(chunk.metadata.is_continuation)
  print("page number :",chunk.metadata.page_number)
  print("chunk type :",chunk.metadata.filetype)
  print("-"*20)
  print("\n===================")
  print(chunk)
  print("===================")