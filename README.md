# ai-interviewer

The user interation is like this

```bash
USER INPUT
├── Option 1: Role name ➝ role_based_chain ➝ LLM ➝ question
├── Option 2: Resume + JD ➝ hybrid_chain (context + RAG) ➝ LLM ➝ tailored question
├── Option 3: Resume only ➝ resume_based_chain ➝ LLM
└── Option 4: JD only ➝ jd_based_chain ➝ LLM
---
```

The folder structure is like this
```bash
ai_interviewer/
├── main.py                        # FastAPI app entry point
├── requirements.txt               # Project dependencies
├── .env                           # Environment variables

├── app/
│   ├── __init__.py

│   ├── routers/                   # FastAPI route handlers
│   │   ├── __init__.py
│   │   ├── feedback.py
│   │   ├── resume_jd_upload.py
│   │   ├── role_based.py
│   │   └── status.py

│   ├── models/                    # Pydantic request/response models
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── role.py
│   │   ├── resume.py
│   │   ├── jd.py
│   │   └── feedback.py

│   ├── services/                  # Core business logic
│   │   ├── __init__.py
│   │   ├── interview_service.py
│   │   ├── resume_service.py
│   │   ├── jd_service.py
│   │   └── feedback_service.py

│   ├── chains/                    # LangChain pipelines
│   │   ├── __init__.py
│   │   ├── question_chain.py
│   │   ├── resume_based_chain.py
│   │   ├── jd_based_chain.py
│   │   └── hybrid_chain.py

│   ├── prompts/                   # Prompt templates for each mode
│   │   ├── role_prompt.txt
│   │   ├── resume_prompt.txt
│   │   ├── jd_prompt.txt
│   │   └── hybrid_prompt.txt

│   ├── memory/                    # Conversation memory (if used)
│   │   └── conversation.py

│   ├── utils/                     # Helper functions
│   │   ├── __init__.py
│   │   ├── pdf_parser.py
│   │   ├── jd_parser.py
│   │   ├── logger.py
│   │   └── file_utils.py

│   ├── config/                    # Configurations and environment setup
│   │   └── settings.py

│   └── vectorstores/              # RAG vector database logic (optional)
│       └── rag_store.py

├── scripts/                       # Standalone scripts
│   └── preprocess_resume_data.py

└── data/                          # File uploads and logs
    ├── uploads/                   # Uploaded resumes & job descriptions
    ├── logs/                      # Application logs
    └── vectorstore/               # Vectorstore data (e.g., FAISS/Chroma)
```
