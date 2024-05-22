
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
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from langchain_core.callbacks import BaseCallbackManager
import streamlit as st

load_dotenv()

openai_api_key= os.getenv("OPENAI_API_KEY")

# Settings.embed_model = OpenAIEmbedding(model = 'text-embedding-3-small', api_key=openai_api_key)
Settings.embed_model = HuggingFaceEmbedding(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

Settings.llm = OpenAI(model= 'gpt-3.5-turbo', api_key=openai_api_key)

qa_prompt_str = (
    "Context information is below.\n"
    "---------------------\n"
    "{context_str}\n"
    "---------------------\n"
    "Given the context information and not prior knowledge, "
    "Only answer the question in the same language as the query and not as the context\n"
    "Query: {query_str}\n"
    "Answer: "
)

system_message = (
    "You are an expert Q&A system that highly trusted in University of Tartu.\n"
    "Always answer the query using the provided context information, and not prior knowledge.\n"
    "Some rules to follow:\n"
    "1. Avoid statements like 'Based on the context, ...' or 'The context information ...' or anything along those lines.\n"
    "2. If you are unable to find any information from context to answer the question, then say you are unable to find any infromation about that."
)

chat_text_qa_msgs = [
    ("system", system_message),
    ("user", qa_prompt_str),
]

text_qa_template = ChatPromptTemplate.from_messages(chat_text_qa_msgs)

class ChatbotUT:
    def __init__(self):
        self.initialize()

    def initialize(self):
        client = chromadb.PersistentClient(path="./chroma_db")

        try:
            self.collection = client.get_collection(name="docs_collection")
            collection_exists = True
        except ValueError:
            collection_exists = False


        if not collection_exists: 
            print("Collection does not exist")
            raise ValueError("Collection does not exist")
        else: 
            documents = SimpleDirectoryReader("./docs", recursive=True).load_data()
            self.vector_store = ChromaVectorStore(chroma_collection=self.collection) 
            self.storage_context = StorageContext.from_defaults(vector_store=self.vector_store)

            self.index = VectorStoreIndex.from_vector_store(
                self.vector_store, storage_context=self.storage_context
            )
            
            self.chat_engine = self.index.as_chat_engine(chat_mode="condense_question", text_qa_template = text_qa_template, verbose=True)
        
    def get_chat(self):
        return self.chat_engine

chatbot_ut = ChatbotUT().get_chat()

class StreamHandler(BaseCallbackManager):
    def __init__(self, container, initial_text=""):
        self.container = container
        self.text = initial_text

    def on_llm_new_token(self, token: str, **kwargs) -> None:
        self.text += token
        self.container.write_stream()

# Define the possible options for the user to select from
options = [
    #{"title": "Kui palju on Tartu Ülikoolis tudengeid?"},
    {"title": "How many students are in University of Tartu?"},
    {"title": "What language test I have to complete to go on a study abroad program with Erasmus?"},
    {"title": "What telescopes does university of Tartu have?"}
]

st.set_page_config(
    page_title="main.py",
)

st.header("UT RAG 🎓🐬")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "avatar": "🐬", "content": "I am a helpful student assistant who knows everything about University of Tartu, ask me anything!"}
    ]

user_prompt = ""

# Display the suggestive prompt cards
col1, col2, col3 = st.columns(3)
with col1:
    if st.button(options[0]["title"]):
        user_prompt = options[0]["title"]
with col2:
    if st.button(options[1]["title"]):
        user_prompt = options[1]["title"]
with col3:
    if st.button(options[2]["title"]):
        user_prompt = options[2]["title"]

if "current_response" not in st.session_state:
    st.session_state.current_response = ""

for message in st.session_state.messages:
    with st.chat_message(message["role"], avatar=message['avatar']):
        st.markdown(message["content"])

if user_prompt := st.chat_input("Ask question here", key="user_input") or user_prompt:

    with st.chat_message("user", avatar="🎓"):
        st.markdown(user_prompt)

    st.session_state.messages.append(
        {"role": "user", "avatar":"🎓", "content": user_prompt}
    )

    streaming_response = chatbot_ut.stream_chat(user_prompt)
    with st.chat_message("assistant", avatar="🐬"): 
        st.write_stream(streaming_response.response_gen)

    st.session_state.messages.append(
        {"role": "assistant", "avatar":"🐬", "content": streaming_response}
    )
