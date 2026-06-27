import streamlit as st
import os
from rag_backend import load_and_chunk_multiple_pdfs, create_vector_database, ask_question

st.set_page_config(page_title="Smart Study Companion v2", page_icon="📚", layout="wide")
st.title("📚 Smart Study Companion (v2.0)")

# 1. Initialize Session State for DB and Chat History
if "db" not in st.session_state:
    st.session_state.db = None
if "messages" not in st.session_state:
    st.session_state.messages = []

# 2. Build the Sidebar for Document Management
with st.sidebar:
    st.header("📄 Document Management")
    # UPGRADE: accept_multiple_files=True
    uploaded_files = st.file_uploader("Upload study PDFs", type=["pdf"], accept_multiple_files=True)
    
    if st.button("Process Documents ⚙️"):
        if uploaded_files:
            with st.spinner("Extracting text from all documents..."):
                try:
                    # Save all uploaded files to disk temporarily
                    file_paths = []
                    for file in uploaded_files:
                        temp_path = f"temp_{file.name}"
                        with open(temp_path, "wb") as f:
                            f.write(file.getbuffer())
                        file_paths.append(temp_path)
                    
                    # Pass the LIST of files to our new backend function
                    chunks = load_and_chunk_multiple_pdfs(file_paths)
                    st.session_state.db = create_vector_database(chunks)
                    
                    # Clean up temporary files to save space
                    for path in file_paths:
                        os.remove(path)
                        
                    st.success("All documents processed successfully!")
                except Exception as e:
                    st.error(f"Failed to process documents: {e}")
        else:
            st.warning("Please upload at least one PDF first.")

# 3. Display Chat History
# This loop draws all previous messages on the screen every time the app reruns
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 4. Chat Input Box (Only show if a database exists)
if st.session_state.db is not None:
    if prompt := st.chat_input("Ask a question about your documents..."):
        
        # Add the user's question to the chat history and display it
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate and display the AI's response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                answer, source_docs = ask_question(prompt, st.session_state.db)
                
                # Display the main answer
                st.markdown(answer)
                
                # Format and display the citations in a dropdown
                with st.expander("🔍 View Source Citations"):
                    for i, doc in enumerate(source_docs):
                        # Extract the filename and page number from the metadata
                        source_file = os.path.basename(doc.metadata.get('source', 'Unknown File'))
                        page_num = doc.metadata.get('page', 'Unknown Page')
                        
                        st.markdown(f"**Source {i+1}:** {source_file} (Page {page_num})")
                        st.caption(doc.page_content[:200] + "...") # Show a tiny snippet
            
            # Save the full response (including markdown citations) to history
            full_response = f"{answer}\n\n*(Check citations for details)*"
            st.session_state.messages.append({"role": "assistant", "content": full_response})
else:
    st.info("👈 Please upload and process some PDFs in the sidebar to begin chatting.")