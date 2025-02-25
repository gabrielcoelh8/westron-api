from pydantic import BaseModel, Field
from enum import Enum


class AIModelEnum(str, Enum):
    CHATGPT = "chatgpt"
    GEMINI = "gemini"


class AIModel(BaseModel):
    ai_model: AIModelEnum = Field(..., description="Modelos de IA suportados: chatgpt, gemini")