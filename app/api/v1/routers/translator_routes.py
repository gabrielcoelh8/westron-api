from fastapi import APIRouter, Depends
from typing import Optional

from app.api.v1.modules.translator import translate_process
from app.schemas.translator_request import TranslateTextRequest, TranslateFileRequest
from app.schemas.translator_response import TranslateFileResponse, TranslateTextResponse
from app.api.v1.routers.auth_routes import get_current_active_user


router = APIRouter()


@router.post(
    path='/translator/translate_text',
    response_model=Optional[TranslateTextResponse],
    dependencies=[Depends(get_current_active_user)]
)
def translate_text(request: TranslateTextRequest):
    return translate_process(request)


# @router.post(
#     path='/translator/translate_file',
#     response_model=Optional[TranslateFileResponse]
# )
# def translate_file(request: TranslateFileRequest):
#     return TranslateFileResponse(
#         file="Coming soon..."
#     )

