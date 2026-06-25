import streamlit as st
import os
from rag_backend import load_and_chunk_pdf, create_vector_database, ask_question

st.set_page_config(page_title="Smart Study Companion", page_icon="📚")
st.title("📚 Smart Study Companion")
st.write("Upload a document and ask questions factual to its content.")

# 1. Initialize session state so we don't reload the database on every click
if "db" not in st.session_state:
    st.session_state.db = None

# 2. File Upload Widget
uploaded_file = st.file_uploader("Upload a study PDF", type=["pdf"])

if uploaded_file is not None:
    # Save the uploaded file locally to read it
    with open("temp.pdf", "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    if st.button("Process Document ⚙️"):
        with st.spinner("Extracting text and building vector database..."):
            try:
                chunks = load_and_chunk_pdf("temp.pdf")
                st.session_state.db = create_vector_database(chunks)
                st.success("Document processed successfully! Ask away.")
            except Exception as e:
                # 🛑 Catch any error (e.g., corrupt file, API failure) and show a clean message
                st.error(f"Failed to process the document. Error details: {e}")

# 3. Chat Interface Component
if st.session_state.db is not None:
    user_question = st.text_input("Ask a question about your document:")
    if user_question:
        with st.spinner("Searching context..."):
            answer = ask_question(user_question, st.session_state.db)
        st.write("🤖 **AI Answer:**", answer)