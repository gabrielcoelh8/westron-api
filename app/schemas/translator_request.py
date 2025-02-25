from app.models.ai_model import AIModel


class TranslateTextRequest(AIModel):
    text: str
    language_in: str
    language_out: str


class TranslateFileRequest(AIModel):
    file: str
    language_in: str
    language_out: str
