from fastapi import APIRouter
from typing import Optional

from app.schemas.positivity_response import IsPositiveResponse, ToPositiveResponse
from app.schemas.positivity_request import IsPositiveRequest, ToPositiveRequest


router = APIRouter()


@router.post(
    path='/positivity/is_positive',
    response_model=Optional[IsPositiveResponse]
)
def is_positive(request: IsPositiveRequest):
    return IsPositiveResponse(
        is_positive=True
    )


@router.post(
    path='/positivity/to_positive',
    response_model=Optional[ToPositiveResponse]
)
def to_positive(request: ToPositiveRequest):
    return ToPositiveResponse(
        text=""
    )

