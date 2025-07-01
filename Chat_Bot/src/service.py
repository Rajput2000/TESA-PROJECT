import os
from dotenv import load_dotenv
from google import genai


load_dotenv()


class ChatBot:
    def __init__(self) -> None:
        APIKEY = os.getenv("API_KEY")
        self.client = genai.Client(api_key=APIKEY)

        # Start the chat
        self.chat = self.client.chats.create(model="gemini-2.5-flash")

        # First message acts like a system instruction prompt
        instruction = """
                        You are Jarvis, a Library Assitant at futminna, use the following guidelines to answer and validate users questions:
                        1. Answer questions clearly and precisely
                        2. Never disclose confidential information
                        3. Never provide answers to questions outside the libraty settings. 
                        In a situation where you don't known the answer to a question tell them to contact 090XXXXXXXXX.
                        """
        self.chat.send_message(instruction)

    def send_conversation(self, message):
        # Continue the conversation
        response = self.chat.send_message(message)
        return response.text
