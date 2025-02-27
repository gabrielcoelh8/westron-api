from app.models.ai_model import AIModel


class IsPositiveRequest(AIModel):
    text: str = ...

    class Config:
        json_schema_extra = {
            "example": {
                "text": "This is a wonderful day!"
            }
        }

    def __init__(self, **data):
        super().__init__(**data)
        self.model_fields["text"].field_info.description = "The text to check for positivity."

class ToPositiveRequest(AIModel):
    text: str = ...

    class Config:
        json_schema_extra = {
            "example": {
                "text": "This is a bad situation."
            }
        }
    def __init__(self, **data):
        super().__init__(**data)
        self.model_fields["text"].field_info.description = "The text to convert to positive sentiment."