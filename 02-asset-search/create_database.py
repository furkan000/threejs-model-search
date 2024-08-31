import chromadb
import pandas as pd
import os
import chromadb.utils.embedding_functions as embedding_functions
import time

# Retrieve API key from environment variable
openai_api_key = os.getenv('OPENAI_API_KEY')

# Flag to determine whether to use OpenAI embeddings
use_openai_embeddings = os.getenv('USE_OPENAI_EMBEDDINGS', 'false').lower() == 'true'

# Set up the embedding function based on the flag
if use_openai_embeddings and openai_api_key:
    openai_ef = embedding_functions.OpenAIEmbeddingFunction(
        api_key=openai_api_key,
        model_name="text-embedding-3-small"
    )
else:
    openai_ef = None  # Or use a different embedding function or None

# Initialize ChromaDB client
chroma_client = chromadb.PersistentClient(path="./openai_full.db")

# Ask the user if they want to proceed or abort
proceed = input("Proceed? (y/n) ")
if proceed.lower() != "y":
    exit()

# Create or get the collection, conditionally use the embedding function
if openai_ef:
    collection = chroma_client.create_collection(name="my_collection", embedding_function=openai_ef)
else:
    collection = chroma_client.create_collection(name="my_collection")

csv_file_path = "Cap3D_automated_Objaverse_highquality.csv"
chunk_size = 1000  # Adjust based on your available memory
csv_reader = pd.read_csv(csv_file_path, usecols=[0, 1], chunksize=chunk_size, header=None)

# Start timer
start = time.time()

for chunk in csv_reader:
    ids = chunk[0].values.tolist()
    ids = [str(i) for i in ids]
    
    keys = chunk[1].values.tolist()
    keys = [str(i) for i in keys]

    collection.add(
        ids=ids,
        documents=keys
    )

end = time.time()
print(f"Time taken: {end - start} seconds")

# Perform a query if using OpenAI embeddings
if use_openai_embeddings:
    results = collection.query(
        query_texts=["blue chair"],
        n_results=5,
    )
    print(results)
else:
    print("OpenAI embeddings are not used. Query functionality is disabled.")
