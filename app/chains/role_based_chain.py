import os
from langchain.prompts import PromptTemplate
from langchain.chains import ConversationChain, LLMChain
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.memory import ConversationBufferMemory
from app.config.settings import GEMINI_MODEL, GEMINI_TEMP, ROLE_PROMPT_PATH, ROLE_EVAL_PROMPT_PATH

google_api_key = os.getenv("GEMINI_API_KEY")
if not google_api_key:
    raise ValueError("GEMINI_API_KEY is missing from environment variables.")

def get_role_conversation_chain(memory: ConversationBufferMemory, role_name: str) -> ConversationChain:

    template_str = ROLE_PROMPT_PATH.read_text()  
    dynamic_prompt = template_str.replace("{role_name}", role_name)


    prompt = PromptTemplate(
        input_variables=["chat_history", "input"],
        template=dynamic_prompt
    )

    llm = ChatGoogleGenerativeAI(
        model=GEMINI_MODEL,
        temperature=GEMINI_TEMP,
        google_api_key=google_api_key
    )

    return ConversationChain(
        llm=llm,
        prompt=prompt,
        memory=memory,
        verbose=True
    )

def get_evaluation_chain() -> LLMChain:

    template = ROLE_EVAL_PROMPT_PATH.read_text()

    prompt = PromptTemplate(
        input_variables=["role_name", "chat_history"],
        template=template
    )

    llm = ChatGoogleGenerativeAI(
        model=GEMINI_MODEL,
        temperature=GEMINI_TEMP,
        google_api_key=google_api_key
    )

    return prompt | llm
