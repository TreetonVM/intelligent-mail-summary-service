from langchain_ollama.llms import OllamaLLM

from config.llm import mistral
from utils.security import sanitize_email_body

from .prompts import EMAIL_SUMMARY_PROMPT


def create_summarizer() -> OllamaLLM:
    return OllamaLLM(
        model=mistral.MODEL,
        temperature=mistral.TEMPERATURE,
        top_p=mistral.TOP_P,
        top_k=mistral.TOP_K,
    )


def summarize_email(body_plain: str, llm: OllamaLLM) -> str:
    sanitized_body = sanitize_email_body(body_plain)
    return llm.invoke(EMAIL_SUMMARY_PROMPT.format(email_body=sanitized_body))
