# ai-interviewer

The application flow is like this

## USER FLOW

```bash
USER INPUT
├── Option 1: Role Based  ✅
│     ➝ ask “Which role?”  
│     ➝ role_based_chain  
│     ➝ LLM  
│     ➝ return next interview question  
│
├── Option 2: JD Only  ✅
│     ➝ upload JD text  
│     ➝ jd_based_chain
│     ➝ LLM  
│     ➝ tailored question  
│
├── Option 3: Resume Only  ✅
│     ➝ upload resume text  
│     ➝ resume_based_chain  
│     ➝ LLM  
│     ➝ tailored question  
│
└── Option 4: Resume + JD  ✅
      ➝ upload JD text  
      ➝ upload resume & JD text  
      ➝ hybrid_chain (RAG + prompt)   
      ➝ LLM question  
      ➝ tailored question
```

## Folder Structure

```bash
ai_interviewer/
│
├── main.py                    # 🚀 Entry point: creates FastAPI app, includes all routers
├── requirements.txt           # 📦 Python dependencies
├── .env                       # 🔐 Env vars (e.g., API keys, model config)
│
├── app/                       # 🧠 Core application logic
│   │
│   ├── chains/                # 💬 LangChain chain definitions
│   │   ├── hybrid_chain.py       # Defines ConversationChain for hybrid mode (resume + JD combo)
│   │   ├── role_based_chain.py   # Defines ConversationChain for role-based chat
│   │   ├── jd_based_chain.py     # Defines ConversationChain for jd-based chat
│   │   └── resume_based_chain.py # Defines ConversationChain for resume-based chat with RAG
│   │
│   ├── config/                # ⚙️ App-wide configuration
│   │   └── settings.py        # Loads env vars and configurable variables
│   │
│   ├── memory/                # 🧠 Session memory management
│   │   ├── hybrid_sessions.py    # `HybridSession` class, `get_session()` logic for hybrid mode
│   │   ├── role_sessions.py      # `ChatSession` class, `get_session()` logic for role-based mode
│   │   ├── jd_sessions.py        # `ChatSession` class, `get_session()` logic for JD-based mode
│   │   └── resume_sessions.py    # `ChatSession` class, `get_session()` logic for resume-based mode
│   │
│   ├── prompts/               # 📝 LLM prompt templates
│   │   ├── hybrid_eval_prompt.txt      # Prompt for evaluating hybrid conversation
│   │   ├── hybrid_prompt.txt           # Prompt for hybrid conversation (resume + JD)
│   │   ├── jd_eval_prompt.txt         # Prompt for evaluating JD-based conversation
│   │   ├── jd_prompt.txt              # Prompt for JD-based conversation
│   │   ├── resume_eval_prompt.txt     # Prompt for evaluating resume-based conversation
│   │   ├── resume_prompt.txt          # Prompt for resume-based conversation
│   │   ├── role_eval_prompt.txt      # Prompt for evaluating role-based conversation
│   │   └── role_prompt.txt           # Prompt for role-based conversation
│   │
│   ├── routers/               # 🌐 FastAPI route handlers
│   │   ├── role_based.py            # /chat/role logic (handles role-based conversation)
│   │   ├── resume.py                # /chat/resume (future expansion)
│   │   ├── jd.py                    # /chat/jd (handles JD input)
│   │   ├── hybrid.py                # /chat/hybrid (handles resume + JD combo)
│   │   └── status.py                # /health or /status (heartbeat or version check)
│   │
│   ├── schemas/              # 🧾 Pydantic models for validation
│   │   ├── hybrid_schemas.py     # `ChatRequest`, `ChatResponse` for hybrid mode
│   │   ├── role_based_schemas.py # `ChatRequest`, `ChatResponse` for role-based mode
│   │   ├── resume_based_schemas.py # `ChatRequest`, `ChatResponse` for resume-based mode
│   │   └── jd_based_schemas.py   # `ChatRequest`, `ChatResponse` for JD-based mode
│   │
│   ├── utils/                 # 🔧 Reusable utility modules
│   │   ├── logger.py              # Centralized logger config
│   │   └── pdf_loader.py          # PDF loading utility
│
│
├── data/                     # 📂 Runtime storage
│   ├── uploads/                 # Uploaded resumes or user files
│   ├── logs/                    # Log output files (if written to disk)
│   └── vectorstore/             # FAISS / pgvector / Chroma storage
│
├── qdrant_db/                 # 📂 Vector db collection (for storing embeddings in Qdrant)
│
├── frontend/
│   └── streamlit_app.py        # 🎨 User interface for the AI Interviewer

```