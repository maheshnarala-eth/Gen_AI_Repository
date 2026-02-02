import os
import streamlit as st
import nest_asyncio
nest_asyncio.apply()

from dotenv import load_dotenv
load_dotenv()

from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.embeddings.google_genai import GoogleGenAIEmbedding
from llama_index.llms.google_genai import GoogleGenAI
from llama_index.core import Settings

# ✅ Chunk Settings
Settings.chunk_size = 256
Settings.chunk_overlap = 20

# -----------------------------
# CONFIG
# -----------------------------
st.set_page_config(page_title="Gemini RAG Chatbot", layout="wide")
st.title("🤖 Gemini + LlamaIndex RAG Chatbot")

# ✅ Load API Key from .env
google_api_key = os.getenv("GOOGLE_API_KEY")

if not google_api_key:
    st.error("❌ GOOGLE_API_KEY not found in .env file")
    st.stop()

os.environ["GOOGLE_API_KEY"] = google_api_key


# -----------------------------
# LOAD DOCUMENTS + BUILD INDEX
# -----------------------------
@st.cache_resource
def build_index():
    st.info("📄 Loading documents and building index...")

    documents = SimpleDirectoryReader("Data").load_data()

    embed_model = GoogleGenAIEmbedding(model_name="models/embedding-001")

    index = VectorStoreIndex.from_documents(
        documents,
        embed_model=embed_model
    )


    return index


# ✅ Build Index (Outside Function!)
index = build_index()

# ✅ Gemini LLM
llm = GoogleGenAI(model="gemini-2.0-flash")

# ✅ Query Engine
query_engine = index.as_query_engine(llm=llm)

st.success("✅ Chatbot Ready! Ask questions below.")


# -----------------------------
# CHAT HISTORY
# -----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display Previous Messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# -----------------------------
# USER INPUT
# -----------------------------
user_question = st.chat_input("Ask something from your documents...")

if user_question:

    # Show user message
    st.session_state.messages.append(
        {"role": "user", "content": user_question}
    )

    with st.chat_message("user"):
        st.markdown(user_question)

    # Assistant response
    with st.chat_message("assistant"):
        with st.spinner("🤖 Thinking..."):
            response = query_engine.query(user_question)
            st.markdown(str(response))

    # Save response in history
    st.session_state.messages.append(
        {"role": "assistant", "content": str(response)}
    )
