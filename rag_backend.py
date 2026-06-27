import os
import time
from dotenv import load_dotenv

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import PromptTemplate

# Version-robust imports for retrieval chains
try:
    from langchain.chains import create_retrieval_chain
except ImportError:
    try:
        from langchain.chains.retrieval import create_retrieval_chain
    except ImportError:
        try:
            from langchain_classic.chains import create_retrieval_chain
        except ImportError:
            raise ImportError("Could not import create_retrieval_chain. Please verify langchain installation.")

try:
    from langchain.chains.combine_documents import create_stuff_documents_chain
except ImportError:
    try:
        from langchain_classic.chains.combine_documents import create_stuff_documents_chain
    except ImportError:
         raise ImportError("Could not import create_stuff_documents_chain. Please verify langchain installation.")

load_dotenv()

# ... (Keep your existing imports and load_dotenv() at the top) ...

def load_and_chunk_multiple_pdfs(file_paths):
    """Loads MULTIPLE PDFs, splits them, and combines them into one massive list of chunks."""
    all_chunks = []
    
    # Define our chunking strategy once
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
    )

    # Loop through every file the user uploaded
    for file_path in file_paths:
        print(f"Loading and chunking: {file_path}")
        loader = PyPDFLoader(file_path)
        pages = loader.load()
        
        # Split this specific document
        chunks = text_splitter.split_documents(pages)
        
        # Add these chunks to our master list
        all_chunks.extend(chunks)
        
    print(f"Successfully processed {len(file_paths)} files into {len(all_chunks)} total chunks.")
    return all_chunks

def create_vector_database(chunks):
    """Creates embeddings in batches to prevent 429 rate limit errors."""
    print("Creating embeddings and building Vector Database...")
    embeddings_model = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")
    
    # Batch chunks into groups of 50 to respect Gemini API request limits (max 100/req)
    batch_size = 50
    first_batch = chunks[:batch_size]
    
    db = Chroma.from_documents(first_batch, embeddings_model, persist_directory="./chroma_db")
    
    # Process remaining chunks with a delay to stay below the requests-per-minute limits
    for i in range(batch_size, len(chunks), batch_size):
        print(f"Embedding batch {i // batch_size + 1}... (waiting 2 seconds to avoid rate limits)")
        time.sleep(2)
        batch = chunks[i : i + batch_size]
        db.add_documents(batch)
        
    return db

def ask_question(question, db):
    """Answers the question AND returns the source citations."""
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)

    template = """
    You are a helpful study assistant. Use the following pieces of retrieved context to answer the question. 
    If you don't know the answer, just say that you don't know. 

    Context: {context}

    Question: {input}

    Answer:
    """
    prompt = PromptTemplate.from_template(template)

    combine_docs_chain = create_stuff_documents_chain(llm, prompt)
    retriever = db.as_retriever(search_kwargs={"k": 3}) 
    retrieval_chain = create_retrieval_chain(retriever, combine_docs_chain)

    print(f"Thinking about: '{question}'...")
    response = retrieval_chain.invoke({"input": question})
    
    # 🌟 V2.0 UPGRADE: We now return the answer AND the exact chunks used!
    answer = response["answer"]
    source_documents = response["context"] 
    
    return answer, source_documents

if __name__ == "__main__":
    sample_pdf_path = "test.pdf" 
    
    if os.path.exists(sample_pdf_path):
        my_chunks = load_and_chunk_multiple_pdfs([sample_pdf_path])
        my_db = create_vector_database(my_chunks)
        
        # --- NEW TEST CODE ---
        print("\n--- Testing the AI ---")
        my_question = "What is the main topic of this document?"
        answer, source_docs = ask_question(my_question, my_db)
        
        print("\n🤖 AI Answer:")
        print(answer)
        # ---------------------
    else:
        print(f"Error: Could not find {sample_pdf_path}. Please add a PDF to the folder!")