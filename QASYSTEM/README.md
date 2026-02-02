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

QASYSTEM/
│
├── app.py # Main Streamlit chatbot application
├── Data/ # Place your documents here
│ ├── file1.pdf
│ ├── file2.txt
│
├── .env # Contains your Gemini API Key
└── README.md # Project documentation


# 🔑 Setup Gemini API Key

Create a .env file inside the project folder:

GOOGLE_API_KEY=your_actual_gemini_api_key_here


Make sure there are no quotes around the key.


📥 Add Documents

Place your documents inside the Data/ folder:

Supported formats include: 

PDF

TXT

DOCX

Markdown files

Example:

Data/
 ├── report.pdf
 ├── notes.txt

▶️ Run the Chatbot

Start the Streamlit app using:

streamlit run app.py


Once running, open your browser:

http://localhost:8501