from fastapi import APIRouter
from typing import Optional

from app.schemas.positivity_response import IsPositiveResponse, ToPositiveResponse
from app.schemas.positivity_request import IsPositiveRequest, ToPositiveRequest
from app.api.v1.modules.positivity import is_positive_text_process, to_positive_text_process

router = APIRouter()


@router.post(
    path='/positivity/is_positive',
    response_model=Optional[IsPositiveResponse]
)
def is_positive(request: IsPositiveRequest):
    return is_positive_text_process(request)


@router.post(
    path='/positivity/to_positive',
    response_model=Optional[ToPositiveResponse]
)
def to_positive(request: ToPositiveRequest):
    return to_positive_text_process(request)

