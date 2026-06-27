# 📚 Smart Study Companion

An AI-powered Retrieval-Augmented Generation (RAG) web application that lets you upload study materials (PDFs) and ask factual questions with source citations in an interactive chat interface. 

**🔗 Deployed Application:** [studycompanion.streamlit.app](https://studycompanion.streamlit.app)

---

## 🚀 Release History & Evolution

### 🆕 Version 2.0 (Current Stable Release)
*   **Multi-PDF Support**: Upload and index multiple PDF files simultaneously. The app aggregates text chunks across all documents.
*   **Conversational Chat UI**: Transitioned from standard input text fields to Streamlit's native `st.chat_message` and `st.chat_input` conversational UI with persistent chat history.
*   **Local Embeddings (100% Rate-Limit Free)**: Switched the vector indexing pipeline to use **Hugging Face's `all-MiniLM-L6-v2`** local embeddings model. This completely bypassed Google API's 429 quota limits for embedding generation.
*   **High-Quota LLM Chat**: Switched the chat engine to the stable **`gemini-flash-latest` (Gemini 1.5 Flash)** model, giving the app a generous free tier of **1,500 requests per day** (replaces the restricted 20 requests/day preview tier of 2.5).
*   **Deduplicated Citations**: Added an expandable dropdown that groups and displays the source files and exact page numbers referenced by the model.
*   **Multi-Document Synthesis**: Expanded search window size to `k=15` and updated the prompt templates to instruct the model to synthesize answers across multiple files.
*   **Streamlit Cloud Stability**: Implemented custom system client cache clearing for ChromaDB to resolve tenant connection issues in serverless builds.

### 📜 Version 1.0 (Initial Release)
*   **Single-PDF Q&A**: Supported processing a single PDF document at a time.
*   **Simple Input Fields**: Used static text inputs for Q&A without conversation history.
*   **Google Embeddings**: Relied on Google's `gemini-embedding-001` API which was highly restricted by rate limits for larger documents.
*   **Preview Chat Model**: Used `gemini-2.5-flash` in early preview, limited to 20 daily requests on the free tier.

---

## 🌟 Key Features

*   **PDF Extraction & Chunking**: Parses PDFs and splits text into manageable chunks of 1000 characters with a 200-character overlap using LangChain's `PyPDFLoader` and `RecursiveCharacterTextSplitter`.
*   **Vector Database Store**: Builds a local vector database using **ChromaDB** to index and query document embeddings.
*   **Factual Answers**: Uses a strict prompt template that forces the AI to answer questions using *only* the retrieved document context.
*   **Secure Config**: Excludes private documents, databases, and sensitive API keys (`.env`) from GitHub, utilizing Streamlit Secrets in the cloud deployment.

---

## 📂 Project Structure

```text
study_companion/
│
├── app.py                 # Streamlit frontend, sidebar document manager, and chat state manager
├── rag_backend.py         # RAG pipeline logic (chunking, local embeddings, vector store, and LLM chain)
├── requirements.txt       # Python package dependencies (including PyTorch for local embeddings)
├── .gitignore             # Config to ignore local database, virtual environment, and credentials
└── README.md              # Project documentation
```

---

## ⚙️ How It Works (RAG Architecture)

1. **Document Upload**: The user uploads one or more PDFs using the sidebar in the Streamlit interface (`app.py`).
2. **Text Chunking**: The backend (`rag_backend.py`) reads each PDF, splits it into chunks of 1000 characters with a 200-character overlap, and aggregates them into a master list of chunks.
3. **Embeddings & Vector Database**: The chunks are converted into vector embeddings locally using the Hugging Face `all-MiniLM-L6-v2` sentence-transformer model and stored in a local **Chroma** database. Since embeddings run locally, there are **no API quotas or 429 rate limit errors** for processing large documents.
4. **Retrieval**: When a question is asked, Chroma retrieves the top 15 most relevant text chunks matching the query.
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
