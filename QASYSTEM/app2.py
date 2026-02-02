import os
import time
import streamlit as st
import nest_asyncio
nest_asyncio.apply()

from dotenv import load_dotenv
load_dotenv()

from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.google_genai import GoogleGenAI


# ---------------------------------------
# STREAMLIT PAGE CONFIG
# ---------------------------------------
st.set_page_config(page_title="Gemini RAG Chatbot", layout="wide")
st.title("🤖 Gemini RAG Chatbot (429 Safe Version)")


# ---------------------------------------
# LOAD API KEY
# ---------------------------------------
google_api_key = os.getenv("GOOGLE_API_KEY")

if not google_api_key:
    st.error("❌ GOOGLE_API_KEY not found in .env file")
    st.stop()

os.environ["GOOGLE_API_KEY"] = google_api_key


# ---------------------------------------
# BUILD INDEX (Cached)
# ---------------------------------------
@st.cache_resource
def build_index():
    st.info("📄 Loading documents and building index...")

    # Load documents
    documents = SimpleDirectoryReader("Data").load_data()

    # ✅ Local Embeddings (No API calls)
    embed_model = HuggingFaceEmbedding(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    # Build vector index
    index = VectorStoreIndex.from_documents(
        documents,
        embed_model=embed_model
    )

    return index


# ✅ Load index once
index = build_index()


# ---------------------------------------
# CACHE QUERY ENGINE IN SESSION
# ---------------------------------------
if "query_engine" not in st.session_state:
    llm = GoogleGenAI(model="gemini-2.0-flash")

    # ✅ Cache query engine
    st.session_state.query_engine = index.as_query_engine(llm=llm)

query_engine = st.session_state.query_engine


# ---------------------------------------
# SAFE QUERY FUNCTION (Fix 3 + Fix 4)
# ---------------------------------------
def safe_query(question):
    """Gemini query with delay + retry + backoff"""

    for attempt in range(5):
        try:
            # ✅ Fix 3: Small delay to avoid rate limit
            time.sleep(4)

            return query_engine.query(question)

        except Exception as e:
            wait_time = 2 ** attempt
            st.warning(f"⚠️ Quota hit. Retrying in {wait_time} seconds...")

            # ✅ Fix 4: Exponential backoff
            time.sleep(wait_time)

    return "🚫 Gemini quota exhausted. Please try again later."


# ---------------------------------------
# CHAT UI
# ---------------------------------------
st.subheader("💬 Ask Questions From Your Documents")

user_question = st.text_input("Enter your question:")


# ✅ Fix 1: Only call Gemini when button is pressed
if st.button("Submit Question"):

    if user_question.strip() == "":
        st.warning("Please enter a question.")
    else:
        with st.spinner("🤖 Thinking..."):
            response = safe_query(user_question)

        st.success("✅ Answer:")
        st.write(str(response))
