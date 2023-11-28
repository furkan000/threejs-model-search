import chromadb
import pandas as pd

chroma_client = chromadb.Client()
collection = chroma_client.create_collection(name="my_collection")

csv_file_path = "Cap3D_automated_Objaverse_highquality.csv"

# Create a function to perform the operation on the second column
# def process_second_column(value):
#     # Replace this with your desired operation
#     # For example, you can apply a function or condition here
#     print(value)

# Create a generator to read the CSV file in chunks (adjust chunk size as needed)
chunk_size = 100  # You can adjust this based on your available memory
csv_reader = pd.read_csv(csv_file_path, usecols=[0,1], chunksize=chunk_size, header=None)

# Iterate through the chunks and process the second column


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