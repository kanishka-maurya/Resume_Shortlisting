import chromadb
from chromadb.config import Settings
import json

# <__________________________________________________________****************************______________________________________________________>
# Creating Vector Database
collection = chromadb.Client(Settings(
    chroma_db_impl="duckdb+parquet",
    persist_directory="./chroma_store"  # Local directory to store vectors
))

# defining variables
num_vectors = collection.count()
num_vectors = int(0.8*(num_vectors))

# <__________________________________________________________****************************______________________________________________________>
# saving data to vector database 
def save_to_chromaDB(summarized_text):
    collection.add(
        documents=[summarized_text],
        ids=[str(hash(summarized_text))]
    )

# <__________________________________________________________****************************______________________________________________________>
# retrieving top 80% match
def query_vectorstore(formatted_jd_prompt_template,num_vectors):
    results = collection.query(
    query_texts=[formatted_jd_prompt_template],  
    n_results=num_vectors, 
    include=["documents"]
    )
    documents = results.get("documents")  
    extracted_list = []
    for doc in documents[0]:  
        try:
            doc_dict = json.loads(doc)  # using JSON parser 
            extracted_text = {
                "name": doc_dict.get("Full Name", "N/A"),
                "email": doc_dict.get("Email", "N/A")
            }
            extracted_list.append(extracted_text)
        except Exception as e:
            print("Error parsing document:", doc)
            print("Error:", e)
    return extracted_list
    