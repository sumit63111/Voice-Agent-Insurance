import logging
from livekit.plugins import openai
import os

logger = logging.getLogger(__name__)


def get_llm():
    if not os.getenv("OPENAI_API_KEY"):
        raise ValueError("OPENAI_API_KEY is required")
    
    logger.info("Using standard OpenAI")
    llm = openai.LLM(
        model="gpt-4o-mini",
        api_key=os.getenv("OPENAI_API_KEY"),
    )
    
    return llm