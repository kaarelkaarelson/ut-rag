import os
from dotenv import load_dotenv

import chromadb
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core import StorageContext
from llama_index.core import Settings, VectorStoreIndex, SimpleDirectoryReader, StorageContext
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.core import ChatPromptTemplate

load_dotenv()

openai_api_key= os.getenv("OPENAI_API_KEY")

Settings.embed_model = OpenAIEmbedding(model = 'text-embedding-3-small', api_key=openai_api_key)
Settings.llm = OpenAI(model= 'gpt-3.5-turbo', api_key=openai_api_key)

VECTOR_STORE_EXISTS = True # Set to False to create index and embeddings from scratch

qa_prompt_str = (
    "Context information is below.\n"
    "---------------------\n"
    "{context_str}\n"
    "---------------------\n"
    "Given the context information and not prior knowledge, "
    "answer the question: {query_str}\n"
    "Answer it in the same language as the question."
)

refine_prompt_str = (
    "We have the opportunity to refine the original answer "
    "(only if needed) with some more context below.\n"
    "------------\n"
    "{context_msg}\n"
    "------------\n"
    "Given the new context, refine the original answer to better "
    "answer the question: {query_str}. "
    "Answer it in the same language as the question."
    "If the context isn't useful, output the original answer again.\n"
    "Original Answer: {existing_answer}"
)

# Text QA Prompt
chat_text_qa_msgs = [
    (
        "system",
        "If context isn't helpful for answering the question, say that you don't have access to the information \
        If you don't understand users question, ask them to rephrase it.",
    ),
    ("user", qa_prompt_str),
]
text_qa_template = ChatPromptTemplate.from_messages(chat_text_qa_msgs)

# Refine Prompt
chat_refine_msgs = [
    (
        "system",
        "If context isn't helpful for answering the question, say that you don't have access to the information \
        If you don't understand users question, ask them to rephrase it.",
    ),
    ("user", refine_prompt_str),
]
refine_template = ChatPromptTemplate.from_messages(chat_refine_msgs)

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
        
        self.chat_engine = self.index.as_chat_engine(chat_mode="condense_question", text_qa_template = text_qa_template, refine_template = refine_template, verbose=True)

    def get_chat(self):
        return self.index.as_chat_engine(chat_mode="condense_question", verbose=True)

