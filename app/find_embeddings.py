import chromadb

# 1. Connect to your ChromaDB client
# For a persistent client (local storage):
# client = chromadb.PersistentClient(path="/chroma_data") 
# For a client connecting to a running server:
client = chromadb.HttpClient(host="localhost", port=8000)
#client = chromadb.HttpClient(host='chroma-db', port=8000)
# 2. Get the collection you want to query
collection_name = "llamaindex-docs" # Replace with your collection name
collection = client.get_collection(name=collection_name)

# 3. Retrieve embeddings using the .get() method
# To get all embeddings in the collection:
results_all = collection.get(include=['embeddings'])
print("All embeddings:", results_all['embeddings'])

# To get embeddings for specific IDs:
specific_ids = ["1", "2"] # Replace with your document IDs
results_specific = collection.get(ids=specific_ids, include=['embeddings'])
print("Embeddings for specific IDs:", results_specific['embeddings'])

# To get a limited number of embeddings:
results_limited = collection.get(limit=5, include=['embeddings'])
print("Limited number of embeddings:", results_limited['embeddings'])