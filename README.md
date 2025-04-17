# ai-interviewer

The user interation is like this

```bash
USER INPUT
├── Option 1: Role name ➝ role_based_chain ➝ LLM ➝ question
├── Option 2: Resume + JD ➝ hybrid_chain (context + RAG) ➝ LLM ➝ tailored question
├── Option 3: Resume only ➝ resume_based_chain ➝ LLM
└── Option 4: JD only ➝ jd_based_chain ➝ LLM
```

## Folder Structure

```bash
ai_interviewer/
│
├── main.py
├── requirements.txt
├── .env
│
├── app/
│   ├── __init__.py
│   ├── routers/
│   │   ├── role_based_router.py
│   │   ├── resume_jd_router.py
│   │   ├── feedback_router.py
│   │   └── status.py
│   ├── models/
│   │   ├── base.py
│   │   ├── role.py
│   │   ├── resume.py
│   │   ├── jd.py
│   │   └── feedback.py
│   ├── services/
│   │   ├── interview_service.py
│   │   ├── resume_service.py
│   │   ├── jd_service.py
│   │   └── feedback_service.py
│   ├── chains/
│   │   ├── role_based_chain.py
│   │   ├── resume_based_chain.py
│   │   ├── jd_based_chain.py
│   │   └── hybrid_chain.py
│   ├── prompts/
│   │   ├── role_prompt.txt
│   │   ├── resume_prompt.txt
│   │   ├── jd_prompt.txt
│   │   └── hybrid_prompt.txt
│   ├── memory/
│   │   └── conversation.py
│   ├── utils/
│   │   ├── pdf_parser.py
│   │   ├── jd_parser.py
│   │   ├── logger.py
│   │   └── file_utils.py
│   ├── config/
│   │   └── settings.py
│   └── vectorstores/
│       └── rag_store.py
│
├── scripts/
│   └── preprocess_resume_data.py
│
└── data/
    ├── uploads/
    ├── logs/
    └── vectorstore/
```