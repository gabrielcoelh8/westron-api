from typing import List, Type, Dict, Any, Optional

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import and_, func, String

from app.database.impl.postgres_connection import PostgresConnection
from app.database.meta.declarative_base import postgres_base
from app.database.meta.database_service import DatabaseService
from app.utils.functions import notnone_hasattr, format_string_for_query
from app.schemas.requests_instituicao_financeira import InsertResponse


class SqlAlchemyDatabaseService(DatabaseService):
    def __init__(self):
        self.postgres = PostgresConnection()
        self.session = self.postgres.session

    def add(self, entity: Type[postgres_base], data: Dict) -> InsertResponse:
        try:
            data_f = notnone_hasattr(entity, data)
            if not data_f:
                print("Nenhum dado válido para inserir.")
                return InsertResponse(
                    success=False,
                    message="Nenhum dado válido para inserir.",
                    id=None,
                    status_code=400
                )

            record = entity(**data_f)
            self.session.add(record)
            self.session.commit()
            return InsertResponse(
                success=True,
                message=f"Registro adicionado com sucesso, ID: {record.id}",
                id=record.id,
                status_code=201
            )

        except SQLAlchemyError as e:
            self.session.rollback()
            return InsertResponse(
                success=False,
                message=f"Erro ao realizar operação: {str(e)}",
                id=None,
                status_code=500
            )

    def get_all(self, entity: Type[postgres_base]) -> Optional[List[Type[postgres_base]]]:
        try:
            return self.session.query(entity).all()
        except SQLAlchemyError as e:
            print(f'Erro ao realizar operação: {e}')
            return None

    def get_by(self, entity: Type[postgres_base], filters) -> Optional[List[Type[postgres_base]]]:
        try:
            return self.session.query(entity).filter_by(**filters).all()
        except SQLAlchemyError as e:
            print(f'Erro ao realizar operação: {e}')
            return None

    def get_one_by(self, entity: Type[postgres_base], filters) -> Optional[Type[postgres_base]]:
        try:
            return self.session.query(entity).filter_by(**filters).one_or_none()
        except SQLAlchemyError as e:
            print(f'Erro ao realizar operação: {e}')
            return None

    def get_or_add(self, entity: Type[postgres_base], data: Dict) -> Optional[int]:
        try:
            data_f = notnone_hasattr(entity, data)
            if not data_f:
                print("Nenhum dado válido para inserir.")
                return None
            item = self.get_one_by(entity, data_f)
            if item:
                print("Registro já existe.")
                return item.id

            record = entity(**data_f)
            self.session.add(record)
            self.session.commit()

            return record.id

        except SQLAlchemyError as e:
            self.session.rollback()
            print(f'Erro ao realizar operação: {e}')
            return None

    def update(self, entity: Type[postgres_base], entity_id: int, updates: Dict[str, Any]) -> bool:
        try:
            entity = self.session.query(entity).get(entity_id)
            if not entity:
                return False

            for key, value in updates.items():
                if hasattr(entity, key):
                    setattr(entity, key, value)
                else:
                    raise ValueError(f'Campo {key} não encontrado na entidade.')

            self.session.commit()
            return True
        except (SQLAlchemyError, ValueError) as e:
            self.session.rollback()
            print(f'Erro ao realizar operação: {e}')
            return False

    def delete(self, entity: Type[postgres_base], entity_id: int) -> bool:
        try:
            entity_instance = self.session.query(entity).get(entity_id)
            if not entity_instance:
                return False

            self.session.delete(entity_instance)
            self.session.commit()
            return True
        except SQLAlchemyError as e:
            self.session.rollback()
            print(f'Erro ao realizar operação: {e}')
            return False

    def join(self, entities: List[Type[postgres_base]], filters: Dict[str, Any]) -> Optional[List[Type[postgres_base]]]:
        # TODO: não funciona
        pass
