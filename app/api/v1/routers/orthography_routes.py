from fastapi import APIRouter, Depends
from typing import Optional

from app.api.v1.modules.orthography import check_process
from app.schemas.orthography_request import OrthographyCheckRequest
from app.schemas.orthography_response import OrthographyCheckResponse
from app.api.v1.modules.auth import get_current_active_user


router = APIRouter()


@router.post(
    path='/orthography/check',
    response_model=Optional[OrthographyCheckResponse],
    dependencies=[Depends(get_current_active_user)]
)
def check(request: OrthographyCheckRequest):
    return check_process(request)