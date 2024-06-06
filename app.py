import os
import sys
import uuid
import streamlit as st
from langdetect import detect
from langchain.prompts import ChatPromptTemplate
from langchain_pinecone import PineconeVectorStore
from langchain_openai import OpenAIEmbeddings
from langchain.chains import create_history_aware_retriever 
from langchain_core.prompts import MessagesPlaceholder
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import MessagesPlaceholder
from langchain_core.prompts import MessagesPlaceholder
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_openai import ChatOpenAI
from langchain_core.messages import AIMessage
from loguru import logger

logger.remove() 
logger.add(
    sink=sys.stdout,
    format="<level>{message}</level>", 
    level="DEBUG"  
)

OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
PINECONE_API_KEY = st.secrets["PINECONE_API_KEY"]

lang_dict = {
    "af": "Afrikaans",
    "sq": "Albanian",
    "am": "Amharic",
    "ar": "Arabic",
    "hy": "Armenian",
    "az": "Azerbaijani",
    "eu": "Basque",
    "be": "Belarusian",
    "bn": "Bengali",
    "bs": "Bosnian",
    "bg": "Bulgarian",
    "my": "Burmese",
    "ca": "Catalan",
    "ceb": "Cebuano",
    "ny": "Chichewa",
    "zh-cn": "Chinese (Simplified)",
    "zh-tw": "Chinese (Traditional)",
    "co": "Corsican",
    "hr": "Croatian",
    "cs": "Czech",
    "da": "Danish",
    "nl": "Dutch",
    "en": "English",
    "es": "Spanish",
    "eo": "Esperanto",
    "et": "Estonian",
    "tl": "Filipino",
    "fi": "Finnish",
    "fr": "French",
    "fy": "Frisian",
    "gl": "Galician",
    "ka": "Georgian",
    "de": "German",
    "el": "Greek",
    "gu": "Gujarati",
    "ht": "Haitian Creole",
    "ha": "Hausa",
    "haw": "Hawaiian",
    "he": "Hebrew",
    "hi": "Hindi",
    "hmn": "Hmong",
    "hu": "Hungarian",
    "is": "Icelandic",
    "ig": "Igbo",
    "id": "Indonesian",
    "ga": "Irish",
    "it": "Italian",
    "ja": "Japanese",
    "jv": "Javanese",
    "kn": "Kannada",
    "kk": "Kazakh",
    "km": "Khmer",
}

def detect_language(text: str) -> dict:
    """Returns the text's language. E.g. 'English', 'Estonian' """

    lang_abbr = detect(text)
    lang = lang_dict[lang_abbr] if lang_dict.get(lang_abbr) else "English"

    logger.debug(f"PROMPT LANGUAGE: {lang}, ABBREVIATION: {lang_abbr}")

    return lang

class Chatbot:
    model_name = "gpt-3.5-turbo"
    embedding_model_name = "text-embedding-3-small"
    pinecone_index_name = "quickstart"
    store = {}

    def __init__(self):
        self.session_id = str(uuid.uuid4())
        logger.debug("initialized chatbot!")

        self.initialize()

    def initialize(self):
       llm = ChatOpenAI(model=self.model_name)
       embeddings = OpenAIEmbeddings(model=self.embedding_model_name, api_key=OPENAI_API_KEY)
       
       vectorstore = PineconeVectorStore.from_existing_index(
            self.pinecone_index_name, embeddings
            )
       retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
       
       contextualize_q_system_prompt = (
            "Given a chat history and the latest user question "
            "which might reference context in the chat history, "
            "formulate a standalone question which can be understood "
            "without the chat history. Do NOT answer the question, "
            "just reformulate it if needed and otherwise return it as is"
        )
       
       contextualize_q_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", contextualize_q_system_prompt),
                MessagesPlaceholder("chat_history"),
                ("human", "{input}"),
            ]
        )
       
       history_aware_retriever = create_history_aware_retriever(
            llm, retriever, contextualize_q_prompt
        )
       
       system_prompt = (
            "Context information is below.\n"
            "---------------------\n"
            "{context}\n"
            "---------------------\n"
            "Given the context information and not prior knowledge,"
            "Please answer the question in the following language: {language}"
        )
       
       qa_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", system_prompt),
                MessagesPlaceholder("chat_history"),
                ("human", "{input}"),
            ]
        )
       
       question_answer_chain = create_stuff_documents_chain(llm, qa_prompt) #| StrOutputParser()
       rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)
       
       self.conversational_rag_chain = RunnableWithMessageHistory(
            rag_chain,
            self.get_session_history,
            input_messages_key="input",
            history_messages_key="chat_history",
            output_messages_key="answer",
        )
       
    def get_session_history(self, session_id: str) -> BaseChatMessageHistory:
        if session_id not in self.store:
            self.store[self.session_id] = ChatMessageHistory()
        return self.store[self.session_id]

    def print_message_history(self):
        for message in self.store[self.session_id].messages:
            if isinstance(message, AIMessage):
                prefix = "AI"
            else:
                prefix = "User"

            logger.debug(f"{prefix}: {message.content}\n")
        
    def get_answer(self, question):
        language = detect_language(question)

        stream = self.conversational_rag_chain.stream({"input": question, "language": language},
                                               config={"configurable": {"session_id": self.session_id}})
        
        for chunk in stream:
            if "answer" in chunk:
                yield chunk['answer']
            
def display_chat_messages() -> None:
    """Print message history
    @returns None
    """
    for message in st.session_state.messages:
        with st.chat_message(message["role"], avatar=message["avatar"]):
            st.markdown(message["content"])

if "chatbot" not in st.session_state:
    st.session_state.chatbot = Chatbot()

chatbot = st.session_state.chatbot

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "avatar": "🐬", "content": "I am a helpful student assistant who knows everything about University of Tartu, ask me anything!"}]

options = [
    {"title": "Kui palju õppekavasid on Tartu ülikoolis?"},
    {"title": "¿Donde está la biblioteca?"},
    {"title": "What telescopes does university of Tartu have?"}
]

prompt_option = ""
question = ""
st.session_state.response_status = "completed"

st.set_page_config(page_title="University of Tartu Chatbot")
st.header("UT Chatbot 🎓🐬")
st.markdown("""
<center>
<a href="https://github.com/kaarelkaarelson/ut-rag" target="_blank">contribute to open-source project</a>
</center>
""", unsafe_allow_html=True)
st.text(" ")

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

if question := st.chat_input("Ask question here", key="user_input", disabled=st.session_state.response_status == "processing") or prompt_option:
    logger.debug('STATUS', st.session_state.response_status, "Prompt option", prompt_option)
    
    if prompt_option:
        prompt_option = ""
    
    st.session_state.response_status = "processing"
    with st.chat_message("user", avatar="🎓"):
        st.markdown(question)

    st.session_state.messages.append({"role": "user", "avatar":"🎓", "content": question})

    with st.chat_message("assistant", avatar="🐬",): 
        response = st.write_stream(chatbot.get_answer(question))

    logger.debug("History:")
    chatbot.print_message_history()

    st.session_state.messages.append({"role": "assistant", "avatar":"🐬", "content": response})
    st.session_state.response_status = "completed"
    st.rerun()