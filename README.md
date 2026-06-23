# RAG Complaint Chatbot - CrediTrust Financial

**10 Academy Week 7 Final Project**  
Intelligent Complaint Analysis using RAG

## Features
- Full RAG pipeline (Retrieval + Generation)
- Modern ChatGPT-style UI with conversation memory
- Semantic search over customer complaints
- Source citations for transparency

## How to Run Locally

```powershell
# 1. Activate environment
.\venv\Scripts\Activate

# 2. Rebuild vector store (important!)
python rebuild_vectorstore.py

# 3. Launch the app
python app.py