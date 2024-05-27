import os 
import streamlit as st
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, StorageContext, Settings, ChatPromptTemplate
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.vector_stores.pinecone import PineconeVectorStore
from langchain_core.callbacks import BaseCallbackManager
from pinecone import Pinecone

openai_api_key = st.secrets["OPENAI_API_KEY"]
pinecone_api_key = os.environ["PINECONE_API_KEY"]

Settings.embed_model = OpenAIEmbedding(model='text-embedding-3-small', api_key=openai_api_key)
Settings.llm = OpenAI(model='gpt-3.5-turbo', api_key=openai_api_key)

qa_prompt_str = (
    "Context information is below.\n"
    "---------------------\n"
    "{context_str}\n"
    "---------------------\n"
    "Given the context information and not prior knowledge, please answer the question: {query_str}\n"
)

start_messages = [
    (
        "system", 
        "You are an expert Q&A system of University of Tartu.\n"
        "Some rules to follow:\n"
        "1. Avoid statements like 'Based on the context, ...' or 'The context information ...' or anything along those lines.\n"
    ),
    (
        "user", 
        "Context information is below.\n"
        "---------------------\n"
        "{context_str}\n"
        "---------------------\n"
        "Given the context information and not prior knowledge, please answer the question: {query_str}\n"
    ),
]

text_qa_template = ChatPromptTemplate.from_messages(start_messages)

class ChatbotUT:
    def __init__(self):
        self.initialize()

    def initialize(self):
        pc = Pinecone(api_key=pinecone_api_key)
        pinecone_index = pc.Index("quickstart")
        self.vector_store = PineconeVectorStore(pinecone_index=pinecone_index) 
        self.storage_context = StorageContext.from_defaults(vector_store=self.vector_store)
        self.index = VectorStoreIndex.from_vector_store(self.vector_store, storage_context=self.storage_context)
        self.chat_engine = self.index.as_chat_engine(chat_mode="condense_question", text_qa_template=text_qa_template, verbose=True)
        
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

def display_chat_messages() -> None:
    """Print message history
    @returns None
    """
    for message in st.session_state.messages:
        with st.chat_message(message["role"], avatar=message["avatar"]):
            st.markdown(message["content"])


st.set_page_config(page_title="University of Tartu Chatbot")

st.header("UT RAG 🎓🐬")

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "avatar": "🐬", "content": "I am a helpful student assistant who knows everything about University of Tartu, ask me anything!"}]

options = [
    {"title": "Kui palju õppekavasid on Tartu ülikoolis?"},
    {"title": "¿Donde está la biblioteca?"},
    {"title": "What telescopes does university of Tartu have?"}
]

prompt_option = ""
user_prompt = ""
st.session_state.response_status = "completed"


col1, col2, col3 = st.columns(3)
with col1:
    if st.button(options[0]["title"]):
        prompt_option = options[0]["title"]
with col2:
    if st.button(options[1]["title"]):
        prompt_option = options[1]["title"]
with col3:
    if st.button(options[2]["title"]):
        prompt_option = options[2]["title"]

display_chat_messages()
if "current_response" not in st.session_state:
    st.session_state.current_response = ""

if user_prompt := st.chat_input("Ask question here", key="user_input", disabled=st.session_state.response_status == "processing") or prompt_option:
    print('STATUS', st.session_state.response_status, "Prompt option", prompt_option)
    if prompt_option:
        prompt_option = ""
    
    st.session_state.response_status = "processing"
    with st.chat_message("user", avatar="🎓"):
        st.markdown(user_prompt)

    st.session_state.messages.append({"role": "user", "avatar":"🎓", "content": user_prompt})

    streaming_response = chatbot_ut.stream_chat(user_prompt)
    with st.chat_message("assistant", avatar="🐬",): 
        st.write_stream(streaming_response.response_gen)

    st.session_state.messages.append({"role": "assistant", "avatar":"🐬", "content": streaming_response})
    st.session_state.response_status = "completed"
    st.rerun()