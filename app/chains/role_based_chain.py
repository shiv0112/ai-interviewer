import os
from app.core.configs import GEMINI_MODEL, GEMINI_TEMP
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate

# Get the API key from the environment
google_api_key = os.getenv("GEMINI_API_KEY")

if not google_api_key:
    raise ValueError("GEMINI_API_KEY is missing from environment variables.")

def get_role_based_chain():
    # Load prompt template
    prompt_path = os.path.join("app", "prompts", "role_prompt.txt")
    with open(prompt_path, "r") as file:
        template = file.read()

    # Create prompt template
    prompt = PromptTemplate(
        input_variables=["role_name"],
        template=template
    )

    # Initialize ChatGoogleGenerativeAI with the API key
    llm = ChatGoogleGenerativeAI(
        model=GEMINI_MODEL,  # Or another version if applicable
        temperature=GEMINI_TEMP,
        google_api_key=google_api_key  # Pass the key here
    )

    # Create LangChain chain
    chain = prompt | llm
    return chain