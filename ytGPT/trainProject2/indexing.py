import os
import streamlit as st
from langchain.document_loaders import DirectoryLoader, PyPDFLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI
from langchain.chains import ConversationalRetrievalChain
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

# Set persist directory
persist_directory = 'db'

buffett_loader = DirectoryLoader('./docs/buffett/', glob="*.pdf")
branson_loader = DirectoryLoader('./docs/branson/', glob="*.pdf")

print("Starting to load documents...")

buffett_docs = buffett_loader.load()
print("Finished loading Buffett documents.")
branson_docs = branson_loader.load()
print("Finished loading Branson documents.")

embeddings = OpenAIEmbeddings()
text_splitter = CharacterTextSplitter(chunk_size=250, chunk_overlap=8)

# Split documents and generate embeddings
print("Starting to split and generate embeddings...")
buffett_docs_split = text_splitter.split_documents(buffett_docs)
print("Finished splitting Buffett documents.")
branson_docs_split = text_splitter.split_documents(branson_docs)
print("Finished splitting Branson documents.")

# Create Chroma instances and persist embeddings
print("Starting to create and persist Chroma instances...")
buffettDB = Chroma.from_documents(buffett_docs_split, embeddings, persist_directory=os.path.join(persist_directory, 'buffett'))
print("Finished creating and persisting Buffett Chroma instance.")
buffettDB.persist()

bransonDB = Chroma.from_documents(branson_docs_split, embeddings, persist_directory=os.path.join(persist_directory, 'branson'))
print("Finished creating and persisting Branson Chroma instance.")
bransonDB.persist()

print("Done!")
