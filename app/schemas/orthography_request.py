from app.models.ai_model import AIModel
from app.models.language import LanguageEnum


class OrthographyCheckRequest(AIModel):
    language: LanguageEnum = ...
    text: str = ...

    class Config:
        json_schema_extra = {
            "example": {
                "language": "en",
                "text": "Thsi are an testt."
            }
        }

    def __init__(self, **data):
        super().__init__(**data)
        self.model_fields["language"].field_info.description = "The language for orthography check (e.g., 'en' for English)."
        self.model_fields["text"].field_info.description = "The text to check for orthography errors."
        