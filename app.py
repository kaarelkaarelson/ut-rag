from langchain_core.callbacks import BaseCallbackManager
import streamlit as st

from chatbot_ut import ChatbotUT

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
    {"title": "Kui palju on Tartu Ülikoolis tudengeid?"},
    {"title": "What language test I have to complete to go on a study abroad program with Erasmus?"},
    {"title": "Mis teleskoobid on Tartu Ülikoolil?"}
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

