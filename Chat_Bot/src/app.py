import streamlit as st
from chatbot import ChatBot # Assuming your ChatBot class is in chatbot.py

# --- Initialize ChatBot instance and User History ---

# Use st.session_state to persist the ChatBot instance across Streamlit re-runs.
# This ensures the bot's internal conversation_history is maintained.
if 'chat_bot_instance' not in st.session_state:
    st.session_state.chat_bot_instance = ChatBot()

# Retrieve the persistent ChatBot instance
chat_bot = st.session_state.chat_bot_instance

# App config
st.set_page_config(page_title="Library Assistant", page_icon="🤖")
st.title("Library Assistant")

# Sidebar for user identification
st.sidebar.title("User Session")
user_id = st.sidebar.text_input("Enter your name or ID:", key="user_id")

# Add GitHub link in the sidebar (uncommented for visibility)
st.sidebar.markdown(
    "[🔗 GitHub Repo](https://github.com/Rajput2000/TESA-PROJECT/tree/main/Chat_Bot)"
)

if not user_id:
    st.warning("Please enter your name or ID in the sidebar to start chatting.")
    st.stop()

# Initialize user-specific chat history for Streamlit display.
# This history is separate from the ChatBot's internal history,
# which is managed by the ChatBot instance itself.
chat_display_key = f"chat_history_display_{user_id}"
if chat_display_key not in st.session_state:
    st.session_state[chat_display_key] = [("bot", f"Hi {user_id}! I'm your Library Assistant. How can I help you today?")]
    # Also, ensure the internal bot history is clear for a new user/session
    chat_bot.conversation_history = [] # Clear internal history for a new session/user

# Reset chat button
if st.sidebar.button("Reset Chat"):
    st.session_state[chat_display_key] = [("bot", f"Hi {user_id}! I'm your Library Assistant. How can I help you today?")]
    chat_bot.conversation_history = [] # Crucially, reset the bot's internal history too

# User input
user_query = st.chat_input("Type your message here...")
if user_query:
    # Append user message to the display history immediately
    st.session_state[chat_display_key].append(("user", user_query))

    with st.spinner("Thinking..."):
        try:
            # Call the send_message on the persistent chat_bot instance.
            # This method internally manages its own conversation_history.
            response = chat_bot.send_message(user_query, user_id)
        except Exception as e:
            st.error(f"An error occurred: {e}") # Display the actual error for debugging
            response = "Oops! Something went wrong. Please try again later."
            # Optionally, you might want to log the full traceback here
            # import traceback
            # st.error(traceback.format_exc())

    # Append bot's response to the display history
    st.session_state[chat_display_key].append(("bot", response))

# Display chat history
for role, message in st.session_state[chat_display_key]:
    with st.chat_message("AI" if role == "bot" else "Human"):
        st.write(message)

# # Optional: GitHub link at the bottom of the main page
# st.markdown(
#     "<hr style='margin-top: 2em;'>"
#     "<p style='text-align: center;'>"
#     "<a href='https://github.com/Rajput2000/TESA-PROJECT/tree/main/Chat_Bot' target='_blank'>🔗 View this project on GitHub</a>"
#     "</p>",
#     unsafe_allow_html=True,
# )