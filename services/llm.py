# services/llm.py
from langchain_ollama.llms import OllamaLLM

from .prompts import EMAIL_SUMMARY_PROMPT


def create_summarizer(model: str = "mistral") -> OllamaLLM:
    return OllamaLLM(model=model)


def summarize_email(body_plain: str, llm: OllamaLLM) -> str:
    """Sanitize input and generate summary"""
    return llm.invoke(
        EMAIL_SUMMARY_PROMPT.format(email_body=body_plain[:5000])  # Length limit
    )
