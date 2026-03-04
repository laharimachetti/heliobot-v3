# HelioBot 3.0 🤖
**LLM-Powered College Recommendation Chatbot using RAG**

> Stack: FastAPI + ChromaDB + Groq (Llama 3.3) + Sentence Transformers

---

## 📁 Project Structure
```
heliobot-v3/
├── data/
│   └── 2022.csv          ← Put your dataset here
├── chroma_db/            ← Auto-created after ingestion
├── ingest.py             ← Run ONCE to load data
├── rag_chain.py          ← RAG pipeline
├── main.py               ← FastAPI backend
├── requirements.txt
├── .env                  ← Your API keys
└── frontend/
    └── index.html        ← Deploy on Netlify
```

---

## ⚙️ Setup (Windows)

### Step 1 — Clone & Setup
```bash
mkdir heliobot-v3
cd heliobot-v3
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### Step 2 — Add your data
```
Copy 2022.csv into the data/ folder
```

### Step 3 — Get FREE Groq API Key
1. Go to https://console.groq.com
2. Sign up (free, no credit card)
3. Create API Key
4. Copy it

### Step 4 — Setup .env
```
Copy .env.example to .env
Add your Groq API key
```
```env
GROQ_API_KEY=gsk_your_key_here
```

### Step 5 — Ingest Data (Run ONCE)
```bash
python ingest.py
```
This creates the `chroma_db/` folder with all embeddings.
⏱️ Takes ~2-5 minutes first time.

### Step 6 — Start Backend
```bash
uvicorn main:app --reload
```
Backend runs at: http://localhost:8000

### Step 7 — Open Frontend
Open `frontend/index.html` in browser
(Or deploy to Netlify)

---

## 🌐 Deploy to Render (Free)

1. Push to GitHub
2. Go to https://render.com → New Web Service
3. Connect your GitHub repo
4. Set:
   - Build Command: `pip install -r requirements.txt && python ingest.py`
   - Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
5. Add Environment Variable: `GROQ_API_KEY = your_key`
6. Deploy!

After deploying, update `API_URL` in `frontend/index.html` with your Render URL.

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

