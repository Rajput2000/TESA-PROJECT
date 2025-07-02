import streamlit as st
import requests


# app config
st.set_page_config(page_title="Library Assitant", page_icon="🤖")
st.title("Library Assitant")

# Initialize chat history if not present
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# user input
user_query = st.chat_input("Type your message here...")
if user_query is not None and user_query != "":
  response = requests.post("http://127.0.0.1:8000/chat", json={"message": user_query})
  bot_reply = response.json().get("response", "Error: no response")

  st.session_state.chat_history.append(("user", user_query))
  st.session_state.chat_history.append(("bot", bot_reply))

# conversation
for role, message in st.session_state.chat_history:
    with st.chat_message("AI" if role == "bot" else "Human"):
        st.write(message)
