import os
from dotenv import load_dotenv

from llama_index.core import (
    SimpleDirectoryReader,
    VectorStoreIndex,
    StorageContext,
    Settings,
)
from llama_index.core.node_parser import SimpleNodeParser
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.vector_stores.chroma import ChromaVectorStore
# from llama_index.embeddings.huggingface import HuggingFaceEmbedding
import chromadb
import warnings

# Load environment variables
load_dotenv()

if __name__ == "__main__":
    print("Ingesting documentation into Chroma...")
    input_dir="llamaindex-docs"
    print(f"llamaindex-docs {input_dir}")

    documents =  SimpleDirectoryReader("./llamaindex-docs").load_data()

    # Set up LLM and embedding model
    llm = OpenAI(model="gpt-4", temperature=0) 
    embed_model = OpenAIEmbedding(
        model="text-embedding-3-small",
        embed_batch_size=100,)
    
    # Add  local embedding model if you want use
    # embed_model = HuggingFaceEmbedding(model_name = "BAAI/bge-small-en-v1.5") 

    # Set global settings
    Settings.llm = llm
    Settings.embed_model = embed_model
    Settings.node_parser = SimpleNodeParser.from_defaults(chunk_size=500, chunk_overlap=20)

    # Set up Chroma vector store
    # client = chromadb.HttpClient(host='http://localhost:8000')
    client = chromadb.HttpClient(host='chroma-db', port=8000)

    chroma_collection_name = "llamaindex-docs"
    collection = client.get_or_create_collection(name=chroma_collection_name)

    vector_store = ChromaVectorStore(chroma_collection=collection)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    # Build the index
    index = VectorStoreIndex.from_documents(
        documents,
        storage_context=storage_context,
        show_progress=True,
    )

    print("Finished ingesting into Chroma.")
