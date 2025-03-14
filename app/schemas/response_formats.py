from pydantic import BaseModel

class TranslateResponseFormat(BaseModel):
    text: str

class IsPositiveResponseFormat(BaseModel):
    is_positive: bool
    
class ToPositiveResponseFormat(BaseModel):
    text: str
    
class OrthographyCheckResponseFormat(BaseModel):
    text: str
    
# TODO: "errors": [
# {
# "word": "wrong_word",
# "suggestions": [
# "correct_word"
# ]
# }
# ]