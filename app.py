from langchain_core.callbacks import BaseCallbackManager
import streamlit as st
from langchain.prompts import PromptTemplate

from rag import get_or_create_index, prompt

index = get_or_create_index()

class StreamHandler(BaseCallbackManager): 
    def __init__(self, container, initial_text=""):
        self.container = container
        self.text = initial_text

    def on_llm_new_token(self, token: str, **kwargs) -> None:
        self.text += token
        self.container.markdown(self.text)


st.set_page_config(
    page_title="main.py",
)

st.header("UT RAG 🎓🐬")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "I am a helpful student assistant who knows everything about University of Tartu, ask me anything"}
    ]

if "current_response" not in st.session_state:
    st.session_state.current_response = ""

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if user_prompt := st.chat_input("Ask question here", key="user_input"):

    st.session_state.messages.append(
        {"role": "user", "content": user_prompt}
    )

    with st.chat_message("user"):
        st.markdown(user_prompt)

    response = prompt(index, user_prompt) 

    st.session_state.messages.append(
        {"role": "assistant", "content": response}
    )

    with st.chat_message("assistant"):
        st.markdown(response)

