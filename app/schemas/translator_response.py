from app.models.ai_model import AIModel


class TranslateTextResponse(AIModel):
    text: str


class TranslateFileResponse(AIModel):
    file: str
