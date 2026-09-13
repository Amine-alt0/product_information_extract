import logging

from langchain_openai import ChatOpenAI

from config import (
    OPENROUTER_API_KEY,
    OPENROUTER_BASE_URL,
    OPENROUTER_MODEL,
)

logger = logging.getLogger(__name__)

class LLMService:

    def __init__(self):
        self.llm = ChatOpenAI(
            api_key=OPENROUTER_API_KEY,
            base_url=OPENROUTER_BASE_URL,
            model=OPENROUTER_MODEL,
            timeout=30
        )

        logger.info("LLM service initialized")

    def invoke(self, prompt: str) -> str:
        logger.info("Sending request to LLM")

        response = self.llm.invoke(prompt)

        logger.info("Received response from LLM")

        return response.content