# config/llm.py
from pydantic_settings import BaseSettings


class LLMConfig(BaseSettings):
    model_name: str = "mistral"
    max_summary_length: int = 150
    temperature: float = 0.7

    class Config:
        env_prefix = "LLM_"
        env_file = ".env"
