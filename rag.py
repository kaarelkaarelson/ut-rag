import os
from dotenv import load_dotenv

import chromadb
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core import StorageContext
from llama_index.core import Settings, VectorStoreIndex, SimpleDirectoryReader, StorageContext, PromptTemplate 
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding

load_dotenv()

openai_api_key= os.getenv("OPENAI_API_KEY")

Settings.embed_model = OpenAIEmbedding(model = 'text-embedding-3-small', api_key=openai_api_key)
Settings.llm = OpenAI(model= 'gpt-3.5-turbo', api_key=openai_api_key)

VECTOR_STORE_EXISTS = True # Set to False to create index and embeddings from scratch

def get_or_create_index():

    documents = SimpleDirectoryReader("./docs").load_data()

    db = chromadb.PersistentClient(path="./chroma_db")

    chroma_collection = db.get_or_create_collection("docs_collection")

    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)

    if not VECTOR_STORE_EXISTS: # Creates index and vector embeddings from scratch
        index = VectorStoreIndex.from_documents(
            documents, storage_context=storage_context
        )
    else: # Loads existing index with stored vectors
        index = VectorStoreIndex.from_vector_store(
            vector_store, storage_context=storage_context
        )
    
    return index

def prompt(index, query):
    query_engine = index.as_query_engine(k=5)
    response = query_engine.query(query)
    return response
    
