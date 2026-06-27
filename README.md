# 📚 Smart Study Companion (v2.0)

An AI-powered Retrieval-Augmented Generation (RAG) web application that lets you upload multiple study materials (PDFs) and ask factual questions with source citations in an interactive chat interface.

**🔗 Deployed Application:** [studycompanion.streamlit.app](https://studycompanion.streamlit.app)

---

## 🌟 Features

*   **Multi-PDF Processing & Chunking**: Upload multiple PDFs at once. The application extracts text from all documents and aggregates them using LangChain's `PyPDFLoader` and `RecursiveCharacterTextSplitter`.
*   **Vector Database Store**: Builds a local vector store using **ChromaDB** with **Hugging Face embeddings** (`all-MiniLM-L6-v2`) to index the document chunks locally (100% free, no rate limits).
*   **Conversational Chat History**: Features an interactive chat-style UI using Streamlit's native `st.chat_message` and `st.chat_input` widgets, allowing you to ask questions and see message history.
*   **Source Citations**: For every answer, the AI displays the exact source documents and page numbers used to construct the response in an expandable dropdown.
*   **Factual Q&A Brain**: Connects with the **Gemini 2.5 Flash** model via LangChain to answer questions strictly based on the context retrieved from the PDFs.
*   **Version-Robust Imports**: Includes custom import fallback logic to handle package namespace differences between LangChain v0.1, v0.2, v0.3, and v1.x, ensuring seamless zero-configuration cloud deployment.
*   **Secure Config**: Excludes private documents, databases, and sensitive API keys (`.env`) from GitHub, utilizing Streamlit Secrets in the cloud deployment.

---

## 📂 Project Structure

```text
study_companion/
│
├── app.py                 # Streamlit frontend, sidebar document manager, and chat state manager
├── rag_backend.py         # RAG pipeline logic (chunking, embeddings, vector database, LLM prompt & chain)
├── requirements.txt       # Python package dependencies
├── .gitignore             # Config to ignore local database, virtual environment, and credentials
└── README.md              # Project documentation
```

---

## ⚙️ How It Works (RAG Architecture)

1. **Document Upload**: The user uploads one or more PDFs using the sidebar in the Streamlit interface (`app.py`).
2. **Text Chunking**: The backend (`rag_backend.py`) reads each PDF, splits it into chunks of 1000 characters with a 200-character overlap, and aggregates them into a master list of chunks.
3. **Embeddings & Vector Database**: The chunks are converted into vector embeddings locally using the Hugging Face `all-MiniLM-L6-v2` sentence-transformer model and stored in a local **Chroma** database. Since embeddings run locally, there are **no API quotas or 429 rate limit errors** for processing large documents.
4. **Retrieval**: When a question is asked, Chroma retrieves the top 3 most relevant text chunks matching the query.
5. **Contextual Answer & Sources**: The retrieved chunks are formatted into a strict prompt template and sent to Gemini, which replies with a factual answer. The app returns both the answer and the metadata (filenames and page numbers) of the referenced chunks.
6. **Chat Rendering**: The answer is rendered in the chat window, and the page sources are displayed in an expandable "🔍 View Source Citations" dropdown.

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
