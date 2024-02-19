# # impoting the required packages
import streamlit as st
import os
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import google.generativeai as genai
from langchain_community.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI 
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv

# gemini api 
load_dotenv()
genai.configure(api_key = os.getenv("GOOGLE_API_KEY"))
             
def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text

def get_text_chunks(text):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size = 10000, chunk_overlap = 1000)
    chunks = text_splitter.split_text(text)
    return chunks

def get_vector_store(text_chunks):
    embeddings = GoogleGenerativeAIEmbeddings(model = "models/embedding-001")
    vector_store = FAISS.from_texts(text_chunks,embeddings) 
    vector_store.save_local("faiss_index") 

def get_conversation_chain():
    # define the prompt
    prompt_template = """
    Answer the question as detailed as possible from the provided context, make sure to provide all the details, if the answer is not in
    provided context just say, "answer is not available in the context", don't provide the wrong answer\n\n
    Context:\n {context}?\n
    Question: \n{question}\n

    Answer:
    """
    model = ChatGoogleGenerativeAI(model = "gemini-pro", temperatue = 0.3)
    prompt = PromptTemplate(template = prompt_template, input_variables= ["context","question"])
    chain = load_qa_chain(model,chain_type="stuff",prompt = prompt)
    return chain

def user_input(user_question):
    embeddings = GoogleGenerativeAIEmbeddings(model = "models/embedding-001")
    new_db = FAISS.load_local("faiss_index", embeddings)
    docs = new_db.similarity_search(user_question)
    chain = get_conversation_chain()
    response = chain(
        {"input_documents":docs, "question": user_question}
        , return_only_outputs=True)
    print(response)
    st.write("You :", user_question)
    st.write("AI : ", response["output_text"])

# main function 
def main():
    # for website name and icon 
    st.set_page_config(
        page_title="Chat With Docs",
        page_icon="📚"
    )

    # removing header space
    st.write('<style>div.block-container{padding-top:2rem;}</style>', unsafe_allow_html=True)

    # to hide hamburger icon and footer 
    hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
    st.markdown(hide_st_style, unsafe_allow_html=True)

    # webpage title and description 
    st.markdown("<h1 style='text-align: center;'>Chat With Docs</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>You can collaborate with your data</p>", unsafe_allow_html=True)    

    with st.sidebar:    
        pdf_docs = st.file_uploader("Upload your PDF Files", accept_multiple_files=True)
        if st.button("Submit & Process"):
            with st.spinner("Processing..."):
                raw_text = get_pdf_text(pdf_docs)
                text_chunks = get_text_chunks(raw_text)
                get_vector_store(text_chunks)
                st.success("Done")

    user_question = st.text_input("Ask a Question:", placeholder="enter your queries")

    if user_question:
        user_input(user_question)

if __name__ == '__main__':
    main()