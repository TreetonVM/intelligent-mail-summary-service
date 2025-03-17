# services/llm.py
from langchain_ollama.llms import OllamaLLM

from utils.security import sanitize_email_body

from .prompts import EMAIL_SUMMARY_PROMPT


def create_summarizer(model: str = "mistral") -> OllamaLLM:
    return OllamaLLM(model=model)


def summarize_email(body_plain: str, llm: OllamaLLM) -> str:
    sanitized_body = sanitize_email_body(body_plain)
    return llm.invoke(EMAIL_SUMMARY_PROMPT.format(email_body=sanitized_body))
