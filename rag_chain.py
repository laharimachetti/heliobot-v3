"""
rag_chain.py — HelioBot 3.0
RAG Pipeline WITH conversation memory
"""

import chromadb
from chromadb.utils import embedding_functions
from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

CHROMA_PATH = "chroma_db"
COLLECTION_NAME = "heliobot_colleges"
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = "llama-3.3-70b-versatile"

# ── MEMORY STORE ──
# Stores full conversation per session_id
conversation_history = {}

SYSTEM_PROMPT = """You are HelioBot — a friendly, smart college counselling assistant. Think of yourself as a helpful senior student, not a robot.

MOST IMPORTANT — MEMORY:
- You have the FULL conversation history. NEVER ask for something the user already told you.
- If user gave rank earlier → use it, NEVER ask again.
- If user says "give me more" or "more colleges" → show more using the SAME rank and branch from earlier. Do NOT ask for rank.
- If user says "different branch" → ask only which branch. You already have their rank.
- If user gave their name → use it naturally in replies.

PERSONALITY:
- Warm, casual, short replies — like a helpful senior student
- Natural emojis (not too many)
- NEVER say "Based on the context provided" or mention JoSAA, Llama, AI

COLLEGE LIST FORMAT — always use this:
  • NIT Trichy — CSE | Closing Rank: 1240 (OPEN)
  • NIT Warangal — CSE | Closing Rank: 1890 (OPEN)
Show 5 colleges. End with "Want more or a different branch? 😊"

CONVERSATION FLOW:
- "hi/hello" → one warm greeting, ask how to help
- name given → use it from now on
- wants recommendation → ask rank + category TOGETHER in ONE message
- has rank + branch → show colleges IMMEDIATELY, no more questions first
- "give me more" → show more colleges using SAME rank/branch, no questions
- "different branch" → ask only branch name
- "thanks/bye" → short warm farewell

STRICT:
- NEVER write "(4 Years, Bachelor of Technology)"
- NEVER ask for rank if it was already given in this conversation
- Keep replies under 100 words for chat, 150 for college lists
"""

COLLEGE_KEYWORDS = [
    "rank", "nit", "iit", "iiit", "cse", "ece", "college", "branch",
    "seat", "quota", "recommend", "suggest", "list", "more", "closing",
    "opening", "mechanical", "civil", "electrical", "computer", "option",
    "course", "engineering", "admission", "cutoff", "category"
]

def needs_retrieval(query: str) -> bool:
    q = query.lower()
    return any(kw in q for kw in COLLEGE_KEYWORDS)

def get_collection():
    client = chromadb.PersistentClient(path=CHROMA_PATH)
    emb_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name="all-MiniLM-L6-v2"
    )
    return client.get_collection(name=COLLECTION_NAME, embedding_function=emb_fn)

def retrieve(query: str, n_results: int = 12):
    try:
        results = get_collection().query(query_texts=[query], n_results=n_results)
        return results["documents"][0]
    except:
        return []

def get_history(session_id: str):
    return conversation_history.get(session_id, [])

def save_to_history(session_id: str, role: str, content: str):
    if session_id not in conversation_history:
        conversation_history[session_id] = []
    conversation_history[session_id].append({"role": role, "content": content})
    # Keep last 20 messages to avoid token overflow
    conversation_history[session_id] = conversation_history[session_id][-20:]

def ask_heliobot(query: str, session_id: str = "default") -> str:
    try:
        groq_client = Groq(api_key=GROQ_API_KEY)

        # ── Build messages: system prompt + full history ──
        messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        messages.extend(get_history(session_id))  # THIS IS THE MEMORY

        # ── If college query, retrieve relevant data and inject ──
        if needs_retrieval(query):
            # Build a richer search query using conversation history
            history_text = " ".join([
                m["content"] for m in get_history(session_id)
            ])
            # Combine current query + recent history for better retrieval
            search_query = f"{query} {history_text[-400:]}"
            docs = retrieve(search_query, n_results=12)

            if docs:
                context = "\n".join([f"- {d}" for d in docs])
                user_content = f"""College data for reference:
{context}

Student message: {query}

Important: Use rank and branch from our conversation history if already provided."""
            else:
                user_content = query
        else:
            user_content = query

        # Add current message to messages list
        messages.append({"role": "user", "content": user_content})

        # ── Call Groq LLM with full conversation context ──
        response = groq_client.chat.completions.create(
            model=GROQ_MODEL,
            messages=messages,
            temperature=0.5,
            max_tokens=400
        )

        answer = response.choices[0].message.content

        # ── Save CLEAN messages to history (not context-injected version) ──
        save_to_history(session_id, "user", query)
        save_to_history(session_id, "assistant", answer)

        return answer

    except Exception as e:
        return f"Oops, something went wrong! 😅 Please try again in a few hours."
