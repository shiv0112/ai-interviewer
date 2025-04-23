from pathlib import Path

# GEMINI_API
GEMINI_TEMP = 0.7
GEMINI_MODEL = "gemini-2.0-flash"
INIT_PROMPT = "Ask user a good and relevant first question for {role_name} role."
PROMPT_PATH = Path("app/prompts/role_prompt.txt")
EVAL_PROMPT_PATH = Path("app/prompts/evaluation_prompt.txt")