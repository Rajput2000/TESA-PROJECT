from fastapi import FastAPI
from pydantic import BaseModel
from src.service import ChatBot


#bot initialization
chat_bot = ChatBot()
app = FastAPI()

class ChatRequest(BaseModel):
    message: str


@app.post("/chat")
def chat_endpoint(req: ChatRequest):
    response = chat_bot.send_conversation(req.message)
    return {"response": response}
