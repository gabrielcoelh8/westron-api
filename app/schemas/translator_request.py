from app.models.ai_model import AIModel
from app.models.language import LanguageEnum


class TranslateTextRequest(AIModel):
    text: str = ...
    language_in: LanguageEnum = ...
    language_out: LanguageEnum = ...

    class Config:
        json_schema_extra = {
            "example": {
                "text": "Hello, world!",
                "language_in": "en",
                "language_out": "es"
            }
        }

    def __init__(self, **data):
        super().__init__(**data)
        self.model_fields["text"].field_info.description = "The text to translate."
        self.model_fields["language_in"].field_info.description = "The source language. Use ISO 639-1 language codes (e.g., 'en' for English)."
        self.model_fields["language_out"].field_info.description = "The target language. Use ISO 639-1 language codes (e.g., 'es' for Spanish)."