from fastapi import APIRouter, Depends, status, HTTPException
from typing import Optional

from app.api.v1.modules.translator import translate_process
from app.schemas.translator_request import TranslateTextRequest
from app.schemas.translator_response import TranslateTextResponse
from app.api.v1.modules.auth import get_current_active_user


router = APIRouter(tags=["Translation"])


@router.post(
    path='/translator/translate_text',
    summary="Translate text",
    description="Translates the provided text from one language to another.",
    response_model=Optional[TranslateTextResponse],
    responses={
        200: {"description": "Translation successful", "content": {"application/json": {"example": {"text": "Translated text here"}}}},
        401: {"description": "Unauthorized", "content": {"application/json": {"example": {"detail": "Not authenticated"}}}},
        422: {"description": "Validation Error", "content": {"application/json": {"example": {"detail": [{"loc": ["body", "text"], "msg": "field required", "type": "value_error.missing"}]}}}},
        500: {"description": "Internal server error", "content": {"application/json": {"example": {"detail": "Internal server error"}}}}
    },
    dependencies=[Depends(get_current_active_user)],
)
def translate_text(request: TranslateTextRequest):
    try:
        return translate_process(request)
    except HTTPException as http_exception:
        raise http_exception
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")
