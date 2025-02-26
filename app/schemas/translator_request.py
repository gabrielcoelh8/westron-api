from app.models.ai_model import AIModel
from app.models.language import LanguageEnum


class TranslateTextRequest(AIModel):
    text: str
    language_in: LanguageEnum
    language_out: LanguageEnum
