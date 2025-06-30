import streamlit as st
import requests
import sys
from exceptions.custom_exception import RAGCustomException
from custom_logging.log_config import logger

BASE_URL = "http://localhost:8001"

st.set_page_config(
    page_title="Cusomer Support Chatbot",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",    
)

st.title("Welcome to the Support Chatbot")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
st.header("💬 Chat")
for chat in st.session_state.messages:
    if chat["role"] == "user":
        st.markdown(f"**🧑 You:** {chat['content']}")
    else:
        st.markdown(f"**🤖 Bot:** {chat['content']}")

# Chat input box at bottom
with st.form(key="chat_form", clear_on_submit=True):
    user_input = st.text_input("Your message", placeholder="e.g. Suggest a bluetooth earphone", key="user_input")
    submit_button = st.form_submit_button("Send")

    
if submit_button and user_input.strip():
    try:
        # Show user message
        st.session_state.messages.append({"role": "user", "content": user_input})

        # Show thinking spinner while backend processes
        with st.spinner("Bot is thinking..."):
            payload = {"question": user_input}
            response = requests.get(f"{BASE_URL}/generate?query={user_input.strip()}", json=payload)

        if response.status_code == 200:
            answer = response.json().get("answer", "No answer returned.")
            st.session_state.messages.append({"role": "bot", "content": answer})
            st.rerun()  # 🔁 fixed here
        else:
            st.error("❌ Bot failed to respond: " + response.text)
    except Exception as e:
        raise RAGCustomException(e, sys)