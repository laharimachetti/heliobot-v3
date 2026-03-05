---
title: Heliobot V3
emoji: 🤖
colorFrom: blue
colorTo: green
sdk: docker
pinned: false
---

# HelioBot 3.0 🤖
**LLM-Powered College Recommendation Chatbot using RAG**

> Stack: FastAPI · ChromaDB · Groq (Llama 3.3) · Sentence Transformers

🔗 **Live Demo:** https://heliobotv3.netlify.app

---

## ✨ Features

- 🧠 **RAG Pipeline** — retrieves real JoSAA college cutoff data before every answer
- 💬 **Conversation Memory** — remembers rank, branch, category and name across messages
- 🎯 **Smart Grouping** — colleges grouped as Safe / Moderate / Dream based on your rank
- 🔍 **Metadata Filtering** — ChromaDB filters colleges within your realistic rank range
- 🃏 **Card UI** — college results shown as clean interactive cards
---


## 🔁 How It Works

```
User Message
     ↓
FastAPI receives request + session ID
     ↓
Conversation memory loaded for this session
     ↓
ChromaDB metadata-filtered retrieval (rank range)
     ↓
Groq API → Llama 3.3 generates answer
     ↓
Safe / Moderate / Dream cards displayed
```

---



## 📁 Project Structure
```
heliobot-v3/
├── data/
│   └── 2022.csv          ← Dataset
├── chroma_db/            ← Auto-created during Docker build
├── ingest.py             ← Runs automatically in Docker
├── rag_chain.py          ← RAG pipeline
├── main.py               ← FastAPI backend
├── Dockerfile            ← Docker configuration
├── requirements.txt
├── .env                  ← Your API keys
└── frontend/
    └── index.html        ← Deploy on Netlify
```
---
## 🌐 Deployment

| Layer | Platform | URL |
|---|---|---|
| Backend | HuggingFace Spaces (Docker) | https://lahi04-heliobot-v3.hf.space |
| Frontend | Netlify (free) | https://heliobotv3.netlify.app |

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| LLM | Llama 3.3 70B via Groq API |
| Embeddings | sentence-transformers/all-MiniLM-L6-v2 |
| Vector DB | ChromaDB |
| Backend | FastAPI + Uvicorn |
| Container | Docker |
| Frontend | HTML + CSS + Vanilla JS |

---

## 💬 Example Questions HelioBot Can Answer
- "Which NITs can I get with rank 5000 in OPEN category?"
- "What is the closing rank for IIT Bombay CSE?"
- "Show me ECE colleges under rank 3000"
- "Best colleges for OPEN category rank 8000"
- "Compare IIT vs NIT cutoffs for Mechanical Engineering"

---

---
## 💬 Chat Flow Example
HelioBot remembers everything — no need to repeat your rank!
```
You:      Hi, my name is Lucy
HelioBot: Hey Lucy! What's your rank and category?

You:      rank 4523, OPEN, CSE
HelioBot: Here are your options Lucy! 🎓

          ✅ Safe Picks
          NIT Durgapur  — CSE | Closing Rank: 5,200 | OPEN
          NIT Patna     — CSE | Closing Rank: 4,800 | OPEN

          ⚡ Moderate Chance
          NIT Warangal  — CSE | Closing Rank: 4,600 | OPEN

          🎯 Dream Colleges
          NIT Trichy    — CSE | Closing Rank: 3,900 | OPEN

          Want more or a different branch? 😊

You:      give me more
HelioBot: (shows more CSE colleges — never asks rank again ✅)

You:      show ECE options
HelioBot: (uses rank 4523 automatically, switches to ECE ✅)

You:      what if my rank is 1200?
HelioBot: (shows colleges for 1200 for this reply only ✅)

You:      thanks bye!
HelioBot: Good luck Lucy! 🍀 Come back anytime.

```

## 🚀 Future Upgrades (v4.0)
- Add Neo4j graph database for relationship queries
- Multi-year trend analysis (2016–2022)
- Agentic AI with LangGraph

