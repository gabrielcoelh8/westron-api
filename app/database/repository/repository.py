from typing import List, Dict, Optional

from sqlalchemy import or_, func, and_
from sqlalchemy.exc import SQLAlchemyError

from app.database.impl.sqlalchemy_database_service import SqlAlchemyDatabaseService

from app.database.models import ExtratoBancario, InstituicaoFinanceira, ExtratoBancarioAlias
from app.schemas.requests import InsertResponse


class ExtratoBancarioRepository(SqlAlchemyDatabaseService):
    def add_extrato_bancario(self, data: Dict) -> InsertResponse:
        try:
            insert_response = self.add(ExtratoBancario, data)
        except ValueError as e:
            mensagem = str(e)
            insert_response = InsertResponse(success=False, message=mensagem, id=None, status_code=402)
        except Exception as e:
            mensagem = f'Exceção não mapeada: {str(e)}'
            insert_response = InsertResponse(success=False, message=mensagem, id=None, status_code=400)
        return insert_response

    # TODO: usado em outros locais. Refatorar se possível.
    def get_extrato_bancario_by_tipo(self, tipo: str, id_instituicao: int) -> Optional[ExtratoBancario]:
        try:
            tipo_extrato = (tipo.replace(" ", "").replace("_", "").upper())

            query = (
                self.session.query(ExtratoBancario)
                .join(ExtratoBancarioAlias)
                .join(InstituicaoFinanceira)
                .filter(
                    or_(
                        func.upper(func.replace(func.replace(ExtratoBancario.tipo, " ", ""), "_",
                                                "")) == tipo_extrato,
                        func.upper(func.replace(func.replace(ExtratoBancarioAlias.tipo, " ", ""), "_",
                                                "")) == tipo_extrato
                    ),
                    and_(
                        InstituicaoFinanceira.id == id_instituicao
                    )
                )
            )
            results = query.first()
            return results

        except SQLAlchemyError as e:
            print(f'Erro ao realizar a junção: {e}')
            return None

    def get_extratos_bancarios_by_instituicao_id(
            self, _instituicao_financeira_id: int
    ) -> Optional[List[ExtratoBancario]]:
        return self.session.query(ExtratoBancario).filter(
            ExtratoBancario.instituicao_financeira_id == _instituicao_financeira_id
        )

    def exists_extrato_bancario(self, id_instituicao: int, tipo: str) -> bool:
        result = (
            self.session.query(ExtratoBancarioAlias)
            .join(ExtratoBancario, ExtratoBancarioAlias.extrato_bancario_id == ExtratoBancario.id)
            .filter(
                and_(
                    ExtratoBancario.instituicao_financeira_id == id_instituicao,
                    ExtratoBancarioAlias.tipo == tipo
                )
            )
            .one_or_none()
        )
        return result is not None
