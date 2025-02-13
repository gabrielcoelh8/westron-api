from fastapi import APIRouter
from typing import Optional

from app.schemas.translator_request import TranslateTextRequest, TranslateFileRequest
from app.schemas.translator_response import TranslateFileResponse, TranslateTextResponse


router = APIRouter()

@router.post(
    path='/translator/translate_text',
    response_model=Optional[TranslateTextResponse]
)
def translate_text(request: TranslateTextRequest):
    return TranslateTextResponse(
        text=""
    )


@router.post(
    path='/positivity/translate_file',
    response_model=Optional[TranslateFileResponse]
)
def translate_file(request: TranslateFileRequest):
    return TranslateFileResponse(
        file=""
    )

