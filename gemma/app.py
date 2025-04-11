import os
import streamlit as st
from langchain_groq import ChatGroq
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.retrieval import create_retrieval_chain
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv
import time

load_dotenv()

groq_api_key = os.getenv("GROQ_API_KEY")
os.environ['GOOGLE_API_KEY'] = os.getenv("GOOGLE_API_KEY")

# Page Configuration
st.set_page_config(page_title="Gemma Document Q&A", page_icon="📄", layout="wide")

st.title("Gemma Model Document Q&A 🧠")

llm = ChatGroq(groq_api_key=groq_api_key, model_name="gemma2-9b-it")

prompt = ChatPromptTemplate.from_template(
    """
    Answer the questions based on the provided context only. 
    Please provide the most accurate response based on the question.
    <context>
    {context}
    <context>

    Question: {input}
    """
)

# Sidebar
st.sidebar.header("Instructions")
st.sidebar.write("1. Upload PDFs to the ./pdfs directory.")
st.sidebar.write("2. Click 'Generate Document Embeddings'.")
st.sidebar.write("3. Ask your question once the embedding process completes.")

# Embedding Function with Visual Feedback
def vector_embedding():
    with st.spinner('Generating embeddings... Please wait.'):
        if "vectors" not in st.session_state:
            st.session_state.embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
            st.session_state.loader = PyPDFDirectoryLoader("./pdfs")  # Data ingestion
            st.session_state.docs = st.session_state.loader.load()  # Document loading
            st.session_state.text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
            st.session_state.final_documents = st.session_state.text_splitter.split_documents(st.session_state.docs)
            st.session_state.vectors = FAISS.from_documents(st.session_state.final_documents, st.session_state.embeddings)
        st.success("Embeddings generated successfully! Now you can ask your question.")

# Buttons for Actions
if st.button("Generate Document Embeddings 💾"):
    vector_embedding()

# Text Input for Questions with Submit Button
with st.form("question_form"):
    prompt1 = st.text_input("What would you like to ask from your documents?")
    submitted = st.form_submit_button("Submit Question")

if submitted and prompt1:
    st.info("Retrieving the most relevant information...")
    document_chain = create_stuff_documents_chain(llm, prompt)
    retriever = st.session_state.vectors.as_retriever()
    retrieval_chain = create_retrieval_chain(retriever, document_chain)

    start = time.process_time()
    response = retrieval_chain.invoke({'input': prompt1})

    st.success("Here is the answer to your question:")
    st.write(response['answer'])

    with st.expander("Document Similarity Search Results 📄"):
        for u, doc in enumerate(response['context']):
            st.write(doc.page_content)
            st.write("---")

    end = time.process_time()
    st.caption(f"Response generated in {end - start:.2f} seconds")
