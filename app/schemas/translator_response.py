from pydantic import BaseModel


class TranslateTextResponse(BaseModel):
    text: str


class TranslateFileResponse(BaseModel):
    file: str
