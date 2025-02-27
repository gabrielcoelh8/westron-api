from fastapi import APIRouter, Depends
from typing import Optional

from app.api.v1.modules.translator import translate_process
from app.schemas.translator_request import TranslateTextRequest
from app.schemas.translator_response import TranslateTextResponse
from app.api.v1.modules.auth import get_current_active_user


router = APIRouter()


@router.post(
    path='/translator/translate_text',
    response_model=Optional[TranslateTextResponse],
    dependencies=[Depends(get_current_active_user)]
)
def translate_text(request: TranslateTextRequest):
    return translate_process(request)
