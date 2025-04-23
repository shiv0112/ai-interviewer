from pathlib import Path

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
