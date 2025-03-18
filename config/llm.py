# config/llm.py
from pydantic_settings import BaseSettings


class LLMConfig(BaseSettings):
    _MODEL: str = "mistral"
    _MAX_SUMMARY_LENGTH: int = 150
    _TEMPERATURE: float = 0.7
    _TOP_P: float = 0.95
    _TOP_K: int = 40

    @property
    def MODEL(self) -> str:
        return self._MODEL

    @property
    def MAX_SUMMARY_LENGTH(self) -> int:
        return self._MAX_SUMMARY_LENGTH

    @property
    def TEMPERATURE(self) -> float:
        return self._TEMPERATURE

    @property
    def TOP_P(self) -> float:
        return self._TOP_P

    @property
    def TOP_K(self) -> int:
        return self._TOP_K

    class Config:
        env_prefix = "LLM_"
        env_file = ".env"


mistral = LLMConfig()
