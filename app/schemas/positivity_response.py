from app.models.ai_model import AIModel


class IsPositiveResponse(AIModel):
    is_positive: bool


class ToPositiveResponse(AIModel):
    text: str
