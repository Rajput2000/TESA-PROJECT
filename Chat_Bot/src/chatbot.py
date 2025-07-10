import os
from dotenv import load_dotenv
import google.generativeai as genai
from service import Library
from systemprompt import SYSTEM_INSTRUCTIONS
from function_call import library_functions

# Load environment variables from .env file
load_dotenv()

class ChatBot:
    def __init__(self) -> None:
        self.library = Library()
        APIKEY = os.getenv("API_KEY")
        genai.configure(api_key=APIKEY)  # type: ignore

        self.model = genai.GenerativeModel(     # type: ignore
            model_name="gemini-2.0-flash",
            tools=[{"function_declarations": library_functions}],
            system_instruction=SYSTEM_INSTRUCTIONS
        )
        # We will manage history manually, so no need to start_chat() here immediately
        # self.chat = self.model.start_chat()
        self.conversation_history = [] # Initialize an empty list to store history
        self.history_limit = 15 # Example: Keep last 15 turns (user+model messages)

    def handle_function_call(self, response):
        # Ensure the function_response is correctly formatted for Gemini
        if not response.candidates:
            return None

        candidate = response.candidates[0]
        if not candidate.content.parts:
            return None

        for part in candidate.content.parts:
            if hasattr(part, 'function_call'):
                function_call = part.function_call
                # print(function_call)

                if function_call.name == "search_book":
                    args = {k: v for k, v in function_call.args.items()}
                    result = self.library.search_book(**args)
                    return {"function": "search_book", "result": result}

                elif function_call.name == "is_book_in_shelf":
                    title = function_call.args.get('title', '')
                    author = function_call.args.get('author', '')
                    result = self.library.is_book_in_shelf(title, author)
                    return {"function": "is_book_in_shelf", "result": result}

                elif function_call.name == "borrow_book":
                    title = function_call.args.get('title', '')
                    author = function_call.args.get('author', '')
                    user = function_call.args.get('user', '')

                    if user.strip() and self.user.lower() == user.lower(): # Assuming self.user is set
                        result = self.library.borrow_book(title, author, user)
                        return {"function": "borrow_book", "result": result}
                    else:
                        # If self.user is not set or mismatch, return an error
                        msg = "users can only borrow books for themselves." if user.strip() else "enter username"
                        return {"function": "borrow_book", "result": {"success": False, "message": msg}}

                elif function_call.name == "return_book":
                    title = function_call.args.get('title', '')
                    author = function_call.args.get('author', '')
                    user = function_call.args.get('user', '')

                    if self.user.lower() == user.lower():
                        result = self.library.return_book(title, author, user)
                        return {"function": "return_book", "result": result}
                    else:
                        return {"function": "return_book", "result": {"success": False, "message": "users can only return books through their account."}}
        return None


    def send_message(self, message: str, user: str):
        self.user = user

        
        # Append user message to history
        self.conversation_history.append({"role": "user", "parts": [message]})

        # Limit history to the last 'history_limit' entries
        # A "turn" typically includes a user message and the model's response.
        # So, to keep N turns, you might keep up to 2*N messages.
        # Here, we're simply truncating the raw list, which means it keeps the last N elements.
        # You might need more sophisticated logic for 'turns'.
        if len(self.conversation_history) > self.history_limit:
            # Keep only the most recent messages
            self.conversation_history = self.conversation_history[-self.history_limit:]

        # Start a new chat with the limited history
        # The model will internally convert this list of dicts to Content objects
        chat_session = self.model.start_chat(history=self.conversation_history)

        step = 1
        max_steps = 5
        
        # Send the current user message (which is now the last item in conversation_history)
        response = chat_session.send_message(message) # Send only the current message, history is via start_chat
        # print(response)
        while step <= max_steps:
            function_result = self.handle_function_call(response)

            if function_result:
                function_name = function_result["function"]
                result = function_result["result"]
                # print(result)

                if isinstance(result, dict):
                    final_response_data = result

                else:
                    # Wrap non-dictionary results (lists, strings, booleans, etc.)
                    final_response_data = {"data": result}

                response_payload = {
                    "function_response": {
                        "name": function_name,
                        "response": final_response_data
                    }
                }

                # Ensure the 'response' part for the history append is ALSO a dictionary
                # This is the crucial part that was missed in the previous fix for history.
                if isinstance(result, dict):
                    history_response_data = result
                else:
                    history_response_data = {"data": result} # Wrap lists/strings/booleans
                
                # Append model's function call and result to history
                self.conversation_history.append({"role": "model", "parts": [{"function_call": genai.protos.FunctionCall(name=function_name, args={})}]}) # type: ignore
                self.conversation_history.append({"role": "tool", "parts": [{"function_response": {"name": function_name, "response": history_response_data}}]}) # Use the consistently dictionary-wrapped data for history
                # print(self.conversation_history, len(self.conversation_history))

                response = chat_session.send_message(response_payload)
                step += 1
                continue

            if response.candidates and response.candidates[0].content.parts:
                model_text = ""
                for part in response.candidates[0].content.parts:
                    if hasattr(part, "text"):
                        model_text += part.text
                    elif hasattr(part, "function_call"):
                         # This case should ideally lead to another handle_function_call
                         # but if it reaches here, it implies a direct function call part in model's last turn
                         pass 

                if model_text:
                    # Append model's text response to history
                    self.conversation_history.append({"role": "model", "parts": [model_text]})
                    # print(self.conversation_history, len(self.conversation_history))
                    return model_text
                else:
                    return "No text response available"
            else:
                return "No valid response from Gemini."

        return "Max steps reached. Ending conversation."