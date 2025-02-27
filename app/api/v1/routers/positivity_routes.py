from fastapi import APIRouter, Depends, status, HTTPException
from typing import Optional

from app.schemas.positivity_response import IsPositiveResponse, ToPositiveResponse
from app.schemas.positivity_request import IsPositiveRequest, ToPositiveRequest
from app.api.v1.modules.positivity import is_positive_text_process, to_positive_text_process
from app.api.v1.modules.auth import get_current_active_user


router = APIRouter(tags=["Positivity"])


@router.post(
    path='/positivity/is_positive',
    summary="Check positivity of text",
    description="Determines if the provided text is positive or negative.",
    response_model=Optional[IsPositiveResponse],
    responses={
        200: {"description": "Positivity check successful", "content": {"application/json": {"example": {"is_positive": True}}}},
        401: {"description": "Unauthorized", "content": {"application/json": {"example": {"detail": "Not authenticated"}}}},
        422: {"description": "Validation Error", "content": {"application/json": {"example": {"detail": [{"loc": ["body", "text"], "msg": "field required", "type": "value_error.missing"}]}}}},
        500: {"description": "Internal server error", "content": {"application/json": {"example": {"detail": "Internal server error"}}}}
    },
    dependencies=[Depends(get_current_active_user)],
)
def is_positive(request: IsPositiveRequest):
    try:
        return is_positive_text_process(request)
    except HTTPException as http_exception:
        raise http_exception
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


@router.post(
    path='/positivity/to_positive',
    summary="Convert text to positive",
    description="Transforms the provided text into a positive version.",
    response_model=Optional[ToPositiveResponse],
    responses={
        200: {"description": "Text converted to positive", "content": {"application/json": {"example": {"text": "Positive text here"}}}},
        401: {"description": "Unauthorized", "content": {"application/json": {"example": {"detail": "Not authenticated"}}}},
        422: {"description": "Validation Error", "content": {"application/json": {"example": {"detail": [{"loc": ["body", "text"], "msg": "field required", "type": "value_error.missing"}]}}}},
        500: {"description": "Internal server error", "content": {"application/json": {"example": {"detail": "Internal server error"}}}}
    },
    dependencies=[Depends(get_current_active_user)],
)
def to_positive(request: ToPositiveRequest):
    try:
        return to_positive_text_process(request)
    except HTTPException as http_exception:
        raise http_exception
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")
    