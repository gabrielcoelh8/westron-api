from fastapi import APIRouter, Depends
from typing import Optional

from app.schemas.positivity_response import IsPositiveResponse, ToPositiveResponse
from app.schemas.positivity_request import IsPositiveRequest, ToPositiveRequest
from app.api.v1.modules.positivity import is_positive_text_process, to_positive_text_process
from app.api.v1.modules.auth import get_current_active_user


router = APIRouter()


@router.post(
    path='/positivity/is_positive',
    response_model=Optional[IsPositiveResponse],
    dependencies=[Depends(get_current_active_user)]
)
def is_positive(request: IsPositiveRequest):
    return is_positive_text_process(request)


@router.post(
    path='/positivity/to_positive',
    response_model=Optional[ToPositiveResponse],
    dependencies=[Depends(get_current_active_user)]
)
def to_positive(request: ToPositiveRequest):
    return to_positive_text_process(request)
