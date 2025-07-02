# 📚 Library Assistant Chatbot 🤖

This is an intelligent chatbot that serves as a **Library Assistant**, built using **Streamlit** and integrated with a backend LLM model. It helps users interact with a digital library assistant through either a direct chat interface or an API-powered setup.

---

## 🚀 Features

- Conversational assistant powered by an LLM.
- Clean and interactive UI using **Streamlit**.
- User session management.
- Resettable chat history.
- Dual setup options: Standalone Streamlit app or FastAPI-based backend.

---

## 📂 Project Structure

```
TESA-PROJECT/
│
├── src/
│   ├── app.py                # Main Streamlit App
│   └── service.py            # ChatBot class (handles backend logic)
│
├── fast_api/
│   ├── backend.py            # FastAPI backend with LLM endpoint
│   └── fast_app_front_end.py # Streamlit frontend that consumes FastAPI
│
└── README.md
```

---

## 🧠 Running the Streamlit App (Standalone)

You can try the app live here:  
👉 [https://tesa-project-chat-bot.streamlit.app/](https://tesa-project-chat-bot.streamlit.app/)

Or run it locally with:

```bash
cd src
streamlit run app.py
```

---

## ⚡ Alternative Setup with FastAPI Backend

Use this method if you want to run the chatbot with a FastAPI backend that serves responses via API.

### Step 1: Start FastAPI Backend

```bash
cd fastapi
uvicorn backend:app --reload
```

This will start the backend at `http://127.0.0.1:8000`.

### Step 2: Start Streamlit Frontend (FastAPI Client)

In another terminal:

```bash
streamlit run fast_app_front_end.py
```

---

## 🛠 Requirements

- Python 3.8+
- Streamlit
- FastAPI
- Uvicorn
- Any dependencies used in your `service.py` or LLM model

Install them using:

```bash
pip install -r requirements.txt
```

---

## 📬 Feedback

For issues or contributions, feel free to open a pull request or raise an issue on the [GitHub repo](https://github.com/Rajput2000/TESA-PROJECT/tree/main/Chat_Bot).

---
