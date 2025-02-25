from app.models.ai_model import AIModel


class IsPositiveRequest(AIModel):
    text: str


class ToPositiveRequest(AIModel):
    text: str
