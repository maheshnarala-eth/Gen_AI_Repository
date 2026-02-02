# 🤖 Gemini RAG Chatbot (Streamlit + LlamaIndex)

A Retrieval-Augmented Generation (RAG) based chatbot built using **Streamlit**, **LlamaIndex**, **Google Gemini LLM**, and **Local HuggingFace Embeddings**.

This project allows you to chat with your own documents (PDF/TXT/etc.) using an AI assistant powered by **Gemini-2.0-Flash**, while avoiding API quota exhaustion issues using local vector embeddings.

---

## ✅ Features

- 📄 Load and index your own documents from the `Data/` folder  
- 🔍 Semantic search using vector embeddings  
- 🧠 Gemini-powered answer generation  
- ⚡ Local HuggingFace embeddings (no embedding API cost)  
- 🚫 Prevents 429 quota errors with:
  - Button-based querying
  - Session caching
  - Rate-limit delay
  - Retry with exponential backoff  
- 🖥️ Interactive chatbot UI built with Streamlit  

---

## 📂 Project Structure

