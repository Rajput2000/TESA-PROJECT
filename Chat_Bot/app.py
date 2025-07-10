import streamlit as st
from src.chatbot import ChatBot
import os 

st.write(os.getcwd())  # Debugging line to check current working directory
# Change to the Chat_Bot directory
os.chdir("Chat_Bot")  # Change to the directory where the library file is located
#list folders in current directory
st.write(os.listdir('.'))  # List files and directories in the current directory
st.write(os.path.dirname(os.path.abspath(__file__)))

"""# Bot initialization
chat_bot = ChatBot()

# App config
st.set_page_config(page_title="Library Assistant", page_icon="🤖")
st.title("Library Assistant")

# Sidebar for user identification
st.sidebar.title("User Session")
user_id = st.sidebar.text_input("Enter your name or ID:", key="user_id")

# Add GitHub link in the sidebar
# st.sidebar.markdown(
#     "[🔗 GitHub Repo](https://github.com/Rajput2000/TESA-PROJECT/tree/main/Chat_Bot)"
# )

if not user_id:
    st.warning("Please enter your name or ID in the sidebar to start chatting.")
    st.stop()

# Initialize user-specific chat history
chat_key = f"chat_history_{user_id}"
if chat_key not in st.session_state:
    st.session_state[chat_key] = [("bot", f"Hi {user_id}! I'm your Library Assistant. How can I help you today?")]

# Reset chat button
if st.sidebar.button("Reset Chat"):
    st.session_state[chat_key] = [("bot", f"Hi {user_id}! I'm your Library Assistant. How can I help you today?")]

# User input
user_query = st.chat_input("Type your message here...")
if user_query:
    with st.spinner("Thinking..."):
        try:
            response = chat_bot.send_message(user_query, user_id)
        except Exception:
            response = "Oops! Something went wrong. Please try again later."
    st.session_state[chat_key].append(("user", user_query))
    st.session_state[chat_key].append(("bot", response))

# Display chat history
for role, message in st.session_state[chat_key]:
    with st.chat_message("AI" if role == "bot" else "Human"):
        st.write(message)

# Optional: GitHub link at the bottom of the main page
st.markdown(
    "<hr style='margin-top: 2em;'>"
    "<p style='text-align: center;'>"
    "<a href='https://github.com/Rajput2000/TESA-PROJECT/tree/main/Chat_Bot' target='_blank'>🔗 View this project on GitHub</a>"
    "</p>",
    unsafe_allow_html=True,
)"""
