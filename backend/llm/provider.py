from langchain_core.language_models.chat_models import BaseChatModel
from langchain_groq import ChatGroq

from backend.core.config import settings


def get_chat_model() -> BaseChatModel:
    if settings.llm_provider == "groq":
        return ChatGroq(
        api_key=settings.groq_api_key,
        model=settings.llm_model,
        temperature=0,
        timeout=20,
        max_retries=2,
        max_tokens=512,
)

    raise ValueError(
        f"Unsupported LLM provider: {settings.llm_provider}"
    )