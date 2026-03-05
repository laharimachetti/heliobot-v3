"""
main.py — HelioBot 3.0
FastAPI backend with session-based memory
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from rag_chain import ask_heliobot

app = FastAPI(
    title="HelioBot 3.0 API",
    description="LLM-powered college recommendation chatbot using RAG",
    version="3.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to your Netlify URL after deploying
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str
    session_id: str = "default"  # Each browser tab sends its own session_id

class ChatResponse(BaseModel):
    response: str

@app.get("/")
def root():
    return {"status": "HelioBot 3.0 is running 🚀", "version": "3.0.0"}

@app.api_route("/health", methods=["GET", "HEAD"])
def health():
    return {"status": "healthy"}

@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    if not request.message.strip():
        return ChatResponse(response="Please ask a question!")
    # Pass session_id so each user has their own memory
    answer = ask_heliobot(request.message, session_id=request.session_id)
    return ChatResponse(response=answer)
