# ai-interviewer

The user interation is like this

**NOTE**
USER INPUT
├── Option 1: Role name ➝ role_based_chain ➝ LLM ➝ question
├── Option 2: Resume + JD ➝ hybrid_chain (context + RAG) ➝ LLM ➝ tailored question
├── Option 3: Resume only ➝ resume_based_chain ➝ LLM
└── Option 4: JD only ➝ jd_based_chain ➝ LLM
---

The folder structure is like this

**NOTE**
ai_interviewer/
│
├── main.py                          # FastAPI app entry point
├── requirements.txt                 # Python dependencies
├── .env                              # Environment variables
│
├── app/
│   ├── __init__.py                  # Initialize the app package
│   
│   ├── routers/                     # FastAPI route handlers
│   │   ├── __init__.py
│   │   ├── feedback.py              # Feedback-related endpoints
│   │   ├── resume_jd_upload.py      # Resume & JD upload endpoints
│   │   ├── role_based.py            # Role-based interview generation
│   │   └── status.py                # Health check / status route
│
│   ├── models/                      # Pydantic models for validation
│   │   ├── __init__.py
│   │   ├── base.py                  # Common base model
│   │   ├── role.py                  # Role model
│   │   ├── resume.py                # Resume model
│   │   ├── jd.py                    # Job Description model
│   │   └── feedback.py              # Feedback model
│
│   ├── services/                    # Business logic
│   │   ├── __init__.py
│   │   ├── interview_service.py     # Interview question generation logic
│   │   ├── resume_service.py        # Resume handling logic
│   │   ├── jd_service.py            # JD handling logic
│   │   └── feedback_service.py      # Feedback processing logic
│
│   ├── chains/                      # LangChain pipelines for different modes
│   │   ├── __init__.py
│   │   ├── question_chain.py        # General question generation chain
│   │   ├── resume_based_chain.py    # Resume-based question chain
│   │   ├── jd_based_chain.py        # JD-based question chain
│   │   └── hybrid_chain.py          # Hybrid mode chain (both resume and JD)
│
│   ├── prompts/                     # Prompt templates for LangChain
│   │   ├── role_prompt.txt          # Template for role-based prompts
│   │   ├── resume_prompt.txt        # Template for resume-based prompts
│   │   ├── jd_prompt.txt            # Template for JD-based prompts
│   │   └── hybrid_prompt.txt        # Template for hybrid mode prompts
│
│   ├── memory/                      # LangChain memory (optional)
│   │   └── conversation.py          # In-memory conversation tracking
│
│   ├── utils/                       # Helper utilities
│   │   ├── __init__.py
│   │   ├── pdf_parser.py            # Logic to parse PDF resumes
│   │   ├── jd_parser.py             # JD parsing or cleaning
│   │   ├── logger.py                # Logger utility
│   │   └── file_utils.py            # File handling utilities (uploads)
│
│   ├── config/                      # Configuration and settings
│   │   └── settings.py              # Settings, including API keys
│
│   └── vectorstores/                # Vector store for RAG (optional)
│       └── rag_store.py             # Logic for storing and querying knowledge base
│
├── scripts/                         # Miscellaneous utility scripts
│   └── preprocess_resume_data.py    # Data preprocessing script for resume data
│
└── data/                            # Data and uploaded files
    ├── uploads/                     # User-uploaded resumes/JDs
    ├── logs/                        # Logs for the app (can be rotated, archived)
    └── vectorstore/                 # Data for the knowledge base or RAG store
---