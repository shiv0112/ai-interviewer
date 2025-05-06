from pathlib import Path

DEBUG = True

# GEMINI_API
GEMINI_TEMP = 0.7
GEMINI_MODEL = "gemini-2.0-flash"
SESSION_TIMEOUT_MINUTES = 20

# ROLE BASED CONFIGS
ROLE_PROMPT_PATH = Path("app/prompts/role_prompt.txt")
ROLE_EVAL_PROMPT_PATH = Path("app/prompts/role_evaluation_prompt.txt")

# JOB DESCRIPTION CONFIGS
JD_PROMPT_PATH = Path("app/prompts/jd_prompt.txt")
JD_EVAL_PROMPT_PATH = Path("app/prompts/jd_evaluation_prompt.txt")

# RESUME CONFIGS
COLLECTION_NAME = "resume_collection"
EMBEDDING_MODEL = "models/embedding-001"
CHUNK_SIZE = 600
CHUNK_OVERLAP = 100
VECTOR_DIM = 768
SEARCH_TYPE = "mmr"
K = 5
MAX_CHUNK_USAGE = 1
QDRANT_PATH = Path("qdrant_db")
RESUME_PROMPT_PATH = Path("app/prompts/resume_prompt.txt")
RESUME_EVAL_PROMPT_PATH = Path("app/prompts/resume_evaluation_prompt.txt")
QDRANT_REMOTE_URL = "http://localhost:6333"