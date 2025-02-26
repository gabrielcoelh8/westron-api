from app.models.ai_model import AIModel
from app.models.language import LanguageEnum


class OrthographyCheckRequest(AIModel):
    language: LanguageEnum
    text: str
