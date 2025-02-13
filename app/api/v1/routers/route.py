from fastapi import APIRouter
from typing import List, Optional

from app.models import ExtratoBancarioModel
from app.database.repository.repository import Repository
from app.schemas.extrato_bancario_request import InsertRequest, \
    GetByInstituicaoIdRequest, ExistsExtratoRequest, GetByTipoRequest
from app.schemas.requests import InsertResponse


router = APIRouter()
extrato_bancario_repositorio = Repository()


@router.post(
    path='/extrato_bancario/get_by_instituicao_id',
    response_model=Optional[List[ExtratoBancarioModel]]
)
def get_by_instituicao_id(request: GetByInstituicaoIdRequest):
    return extrato_bancario_repositorio.get_extratos_bancarios_by_instituicao_id(request.id)


@router.post(
    path='/extrato_bancario/get_by_tipo',
    response_model=Optional[ExtratoBancarioModel]
)
def get_by_tipo(request: GetByTipoRequest):
    return extrato_bancario_repositorio.get_extrato_bancario_by_tipo(**request.model_dump())


@router.post(
    path='/extrato_bancario/add',
    response_model=InsertResponse
)
def add(request: InsertRequest):
    return extrato_bancario_repositorio.add_extrato_bancario(request.data.model_dump())


@router.post(
    path='/extrato_bancario/exists',
    response_model=bool
)
def exists(request: ExistsExtratoRequest):
    return extrato_bancario_repositorio.exists_extrato_bancario(**request.model_dump())
