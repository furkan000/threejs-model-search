import chromadb
import pandas as pd


# chroma_client = chromadb.Client()
chroma_client = chromadb.PersistentClient(path="./thirty-thousand.db")

# ask the user if they want to proceed or abort
proceed = input("Proceed? (y/n) ")
if proceed.lower() != "y":
    exit()
# chroma_client.reset() # reset the database 

collection = chroma_client.create_collection(name="my_collection")
csv_file_path = "Cap3D_automated_Objaverse_highquality.csv"

chunk_size = 30000  # You can adjust this based on your available memory
csv_reader = pd.read_csv(csv_file_path, usecols=[0,1], chunksize=chunk_size, header=None)


# start timer
import time
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
    break
end = time.time()
print(end - start)


results = collection.query(
    query_texts=["blue chair"],
    n_results=5
)
print(results)