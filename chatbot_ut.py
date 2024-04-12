import os
from dotenv import load_dotenv

import chromadb
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core import StorageContext
from llama_index.core import Settings, VectorStoreIndex, SimpleDirectoryReader, StorageContext
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding

load_dotenv()

openai_api_key= os.getenv("OPENAI_API_KEY")

Settings.embed_model = OpenAIEmbedding(model = 'text-embedding-3-small', api_key=openai_api_key)
Settings.llm = OpenAI(model= 'gpt-3.5-turbo', api_key=openai_api_key)

VECTOR_STORE_EXISTS = True # Set to False to create index and embeddings from scratch

class ChatbotUT:
    def __init__(self):
        self.initialize()

    def initialize(self):
        documents = SimpleDirectoryReader("./docs").load_data()
        db = chromadb.PersistentClient(path="./chroma_db")
        self.chroma_collection = db.get_or_create_collection("docs_collection")
        self.vector_store = ChromaVectorStore(chroma_collection=self.chroma_collection)
        self.storage_context = StorageContext.from_defaults(vector_store=self.vector_store)

        if not VECTOR_STORE_EXISTS:  # Creates index and vector embeddings from scratch
            self.index = VectorStoreIndex.from_documents(
                documents, storage_context=self.storage_context
            )
        else:  # Loads existing index with stored vectors
            self.index = VectorStoreIndex.from_vector_store(
                self.vector_store, storage_context=self.storage_context
            )
        
        self.chat_engine = self.index.as_chat_engine(chat_mode="condense_question", verbose=True)

    def get_chat(self):
        return self.index.as_chat_engine(chat_mode="condense_question", verbose=True)
