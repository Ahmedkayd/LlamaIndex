import os
import streamlit as st
from dotenv import load_dotenv
from llama_index.core import VectorStoreIndex, Settings
from llama_index.core.postprocessor import SentenceEmbeddingOptimizer
from llama_index.core.chat_engine.types import ChatMode
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core.callbacks import LlamaDebugHandler, CallbackManager
from node_postprocessors.duplicate_postprocessor import DuplicateRemoverNodePostprocessor
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
import chromadb 

load_dotenv()

print("***Streamlit LlamaIndex Documentation Helper (ChromaDB)***")

# Setup debug callbacks
llama_debug = LlamaDebugHandler(print_trace_on_end=True)
callback_manager = CallbackManager(handlers=[llama_debug])
Settings.callback_manager = callback_manager

@st.cache_resource(show_spinner=False)
def get_index() -> VectorStoreIndex:
    # Initialize Chroma client and persistent DB
    chroma_client = chromadb.HttpClient(host='chroma-db', port=8000)
    chroma_client.heartbeat()
    collection = chroma_client.get_or_create_collection(name="llamaindex-docs")
    vector_store = ChromaVectorStore(chroma_collection=collection)
    return VectorStoreIndex.from_vector_store(vector_store=vector_store)


# Load the index from Chroma
index = get_index()

# Setup chat engine with postprocessors
if "chat_engine" not in st.session_state.keys():
    postprocessor = SentenceEmbeddingOptimizer(
        embed_model=Settings.embed_model,
        percentile_cutoff=0.3,
        threshold_cutoff=0.5,
    )
    st.session_state.chat_engine = index.as_chat_engine(
        chat_mode=ChatMode.CONTEXT,
        verbose=True,
        node_postprocessors=[postprocessor, DuplicateRemoverNodePostprocessor()],
    )

# Streamlit UI setup
st.set_page_config(
    page_title="Chat with LlamaIndex docs, powered by DAU",
    page_icon="🦙",
    layout="centered",
    initial_sidebar_state="expanded"
)

st.markdown("## ●●● Chat with LlamaIndex Docs ●●●")

st.caption("Ask questions. Get answers. Powered by LlamaIndex + ChromaDB 🦙")
# Chat history management
if "messages" not in st.session_state.keys():
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Ask me a question about LlamaIndex's open source Python library?"
        }
    ]

# Input from user
if prompt := st.chat_input("Your question"):
    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

# Display all messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Generate assistant response
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("thinking ...."):
            response = st.session_state.chat_engine.chat(message=prompt)
            st.write(response.response)

            # Show source nodes

            nodes = [node for node in response.source_nodes]
            if nodes:  # Only create columns if there are source nodes
                for col, node, i in zip(st.columns(len(nodes)), nodes, range(len(nodes))):
                    with col:
                        st.header(f"Source Node {i+1}: score = {node.score}")
                        st.write(node.text)


            # Save message
            message = {
                "role": "assistant",
                "content": response.response
            }
            st.session_state.messages.append(message)
