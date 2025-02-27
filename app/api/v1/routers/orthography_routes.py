from fastapi import APIRouter, Depends, status, HTTPException
from typing import Optional

from app.api.v1.modules.orthography import check_process
from app.schemas.orthography_request import OrthographyCheckRequest
from app.schemas.orthography_response import OrthographyCheckResponse
from app.api.v1.modules.auth import get_current_active_user


router = APIRouter(tags=["Orthography"])


@router.post(
    path='/orthography/check',
    summary="Check orthography",
    description="Checks the orthography of the provided text.",
    response_model=Optional[OrthographyCheckResponse],
    responses={
        200: {"description": "Orthography check successful", "content": {"application/json": {"example": {"text": "Corrected text here"}}}},
        401: {"description": "Unauthorized", "content": {"application/json": {"example": {"detail": "Not authenticated"}}}},
        422: {"description": "Validation Error", "content": {"application/json": {"example": {"detail": [{"loc": ["body", "text"], "msg": "field required", "type": "value_error.missing"}]}}}},
        500: {"description": "Internal server error", "content": {"application/json": {"example": {"detail": "Internal server error"}}}}
    },
    dependencies=[Depends(get_current_active_user)],
)
def check(request: OrthographyCheckRequest):
    try:
        return check_process(request)
    except HTTPException as http_exception:
        raise http_exception
    except Exception as e: 
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")
    