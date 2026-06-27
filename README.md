# 📚 Smart Study Companion

An AI-powered Retrieval-Augmented Generation (RAG) web application that lets you upload study materials (PDFs) and ask factual questions about their content. 

**🔗 Deployed Application:** [studycompanion.streamlit.app](https://studycompanion.streamlit.app)

---

## 🌟 Features

*   **PDF Processing & Chunking**: Extracts content from uploaded PDFs and splits them into manageable chunks using LangChain's `PyPDFLoader` and `RecursiveCharacterTextSplitter`.
*   **Vector Database Store**: Builds a local vector store using **ChromaDB** with Google Gemini embeddings (`models/gemini-embedding-001`) to index the document chunks.
*   **Factual Q&A Brain**: Connects with the **Gemini 2.5 Flash** model via LangChain to answer questions strictly based on the context retrieved from the PDF.
*   **Streamlit Web Interface**: Features a beautiful, interactive frontend for drag-and-drop file uploading and instant chat responses.
*   **Secure Config**: Excludes private documents, databases, and sensitive API keys (`.env`) from GitHub, utilizing Streamlit Secrets in the cloud deployment.

---

## 📂 Project Structure

```text
study_companion/
│
├── app.py                 # Streamlit frontend and session state manager
├── rag_backend.py         # RAG pipeline logic (chunking, embeddings, vector database, LLM prompt & chain)
├── requirements.txt       # Python package dependencies
├── .gitignore             # Config to ignore local database, virtual environment, and credentials
└── README.md              # Project documentation
```

---

## ⚙️ How It Works (RAG Architecture)

1. **Document Upload**: The user uploads a PDF using the Streamlit interface (`app.py`).
2. **Text Chunking**: The backend (`rag_backend.py`) reads the PDF and breaks it down into chunks of 1000 characters with a 200-character overlap.
3. **Embeddings & Vector Database**: The chunks are converted into vector embeddings using Google Generative AI and stored in a local **Chroma** database.
4. **Retrieval**: When a question is asked, Chroma retrieves the top 3 most relevant text chunks matching the query.
5. **Contextual Answer**: The retrieved chunks are formatted into a strict prompt template and sent to Gemini, which replies with a concise, factual answer.

---

## 🚀 Running Locally

Follow these steps to run the application on your own machine.

### 1. Clone the Repository
```bash
git clone git@github.com:saikrishnaallam/study_companion.git
cd study_companion
```

### 2. Set Up a Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Create a file named `.env` in the root of the project and add your Google Gemini API Key:
```env
GEMINI_API_KEY="your-api-key-here"
GOOGLE_API_KEY="your-api-key-here"
```

### 5. Launch the Application
```bash
streamlit run app.py
```
The app will open automatically in your browser at `http://localhost:8501`.

---

## ☁️ Deployment on Streamlit Cloud

To host this application yourself on Streamlit Community Cloud:

1. Push the code to a public/private GitHub repository.
2. Link the repository on [Streamlit Share](https://share.streamlit.io/).
3. In the Streamlit app settings under **Secrets**, copy your Gemini API key in TOML format:
   ```toml
   GEMINI_API_KEY = "your-actual-api-key"
   GOOGLE_API_KEY = "your-actual-api-key"
   ```
4. Deploy the app. Streamlit will install packages from `requirements.txt` and launch automatically!
