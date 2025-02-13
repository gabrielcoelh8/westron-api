from pydantic import BaseModel


class TranslateTextRequest(BaseModel):
    text: str
    language_in: str
    language_out: str


class TranslateFileRequest(BaseModel):
    file: str
    language_in: str
    language_out: str
