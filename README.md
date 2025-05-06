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
├── Option 3: Resume Only   
│     ➝ upload resume text  
│     ➝ resume_based_chain  
│     ➝ LLM  
│     ➝ tailored question  
│
└── Option 4: Resume + JD  
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
│   │   ├── role_based_chain.py       # Defines ConversationChain for role-based chat
│   │   ├── jd_based_chain.py         # Defines ConversationChain for jd-based chat
│   │   └── resume_based_chain.py     # Defines ConversationChain for resume based chat that does rag
│   │
│   ├── config/                # ⚙️ App-wide configuration
│   │   └── settings.py               # Used to load env vars and configurable variables
│   │
│   ├── memory/                # 🧠 Session memory management
│   │   ├── role_sessions.py      # `ChatSession` class, `get_session()` logic
│   │   └── jd_sessions.py        # `ChatSession` class, `get_session()` logic
│   │   └── resume_sessions.py    # `ChatSession` class, `get_session()` logic
│   │
│   ├── prompts/               # 📝 LLM prompt templates
│   │   ├── jd_evaluation_prompt.txt     # Prompt to generate the evaluation of jd based conversation
│   │   ├── jd_prompt.txt                # Prompt to generate the jd based conversation
│   │   ├── resume_evaluation_prompt     # Prompt to generate the evaluation of resume based conversation
│   │   ├── resume_prompt.txt           # Prompt to generate the resume based conversation
│   │   ├── role_evaluation_prompt.txt   # Prompt to generate the evaluation of role based conversation
│   │   └── role_prompt.txt              # Prompt to generate the role based conversation
│   │
│   ├── routers/               # 🌐 FastAPI route handlers
│   │   ├── role_based.py              # /chat/role logic (handles role-based conversation)
│   │   ├── resume.py                  # /chat/resume (future expansion)
│   │   ├── jd.py                      # /chat/jd (based on JD input)
│   │   ├── hybrid.py                  # /chat/hybrid (resume + JD combo)
│   │   └── status.py                  # /health or /status (heartbeat or version check)
│   │
│   ├── schemas/              # 🧾 Pydantic models for validation
│   │   ├── role_based_schemas.py     # `ChatRequest`, `ChatResponse` for role mode
│   │   ├── resume_based_schemas.py   # `ChatRequest`, `ChatResponse` for resume mode
│   │   └── jd_based_schemas.py       # `ChatRequest`, `ChatResponse` for jd mode
│   │
│   ├── utils/                 # 🔧 Reusable utility modules
│   │   ├── logger.py                  # Centralized logger config
│   │   └── pdf_loader.py              # for reading pdf files
│
│
├── data/                     # 📂 Runtime storage
│   ├── uploads/                      # Uploaded resumes or user files
│   ├── logs/                         # Log output files (if written to disk)
│   └── vectorstore/                 # FAISS / pgvector / Chroma storage
│
├── qdrant_db/                     # 📂 Vector db collection
│
├── frontend/
│   └── streamlit_app.py      # 🎨 User interface for the AI Interviewer
```