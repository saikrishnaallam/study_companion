import os
from dotenv import load_dotenv

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import PromptTemplate
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain

load_dotenv()

def load_and_chunk_pdf(file_path):
    print(f"Loading PDF from: {file_path}")
    loader = PyPDFLoader(file_path)
    pages = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
    )
    chunks = text_splitter.split_documents(pages)
    return chunks

def create_vector_database(chunks):
    print("Creating embeddings and building Vector Database...")
    embeddings_model = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")
    db = Chroma.from_documents(chunks, embeddings_model, persist_directory="./chroma_db")
    return db

# --- NEW FUNCTION START ---
def ask_question(question, db):
    """Searches the database and asks the LLM to answer based on the results."""
    
    # 1. Initialize the Brain (Gemini 2.5 Flash is incredibly fast and free)
    # temperature=0 means we want factual answers, not creative storytelling.
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)

    # 2. Define our strict Prompt Template
    template = """
    You are a helpful study assistant. Use the following pieces of retrieved context to answer the question. 
    If you don't know the answer, just say that you don't know. 
    Use three sentences maximum and keep the answer concise.

    Context: {context}

    Question: {input}

    Answer:
    """
    prompt = PromptTemplate.from_template(template)

    # 3. Create the chains
    # This chain combines the retrieved chunks into the {context} variable
    combine_docs_chain = create_stuff_documents_chain(llm, prompt)
    
    # This chain handles the actual search and passes results to the combination chain
    retriever = db.as_retriever(search_kwargs={"k": 3}) # Retrieve top 3 most relevant chunks
    retrieval_chain = create_retrieval_chain(retriever, combine_docs_chain)

    # 4. Run it!
    print(f"Thinking about: '{question}'...")
    response = retrieval_chain.invoke({"input": question})
    
    return response["answer"]
# --- NEW FUNCTION END ---

if __name__ == "__main__":
    sample_pdf_path = "test.pdf" 
    
    if os.path.exists(sample_pdf_path):
        my_chunks = load_and_chunk_pdf(sample_pdf_path)
        my_db = create_vector_database(my_chunks)
        
        # --- NEW TEST CODE ---
        print("\n--- Testing the AI ---")
        my_question = "What is the main topic of this document?"
        answer = ask_question(my_question, my_db)
        
        print("\n🤖 AI Answer:")
        print(answer)
        # ---------------------
    else:
        print(f"Error: Could not find {sample_pdf_path}. Please add a PDF to the folder!")