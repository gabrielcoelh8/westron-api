from typing import List, Type, Dict, Any, Optional

from sqlalchemy.exc import SQLAlchemyError

from app.database.service.postgres_connection import PostgresConnection
from app.database.meta.declarative import Base
from app.database.meta.database_service import DatabaseService
from app.utils.functions import notnone_hasattr
from app.schemas.database_response import InsertResponse


class SqlAlchemyDatabaseService(DatabaseService):
    def __init__(self):
        self.postgres = PostgresConnection()
        self.session = self.postgres.session

    def add(self, entity: Type[Base], data: Dict) -> InsertResponse:
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

    def get_all(self, entity: Type[Base]) -> Optional[List[Type[Base]]]:
        try:
            return self.session.query(entity).all()
        except SQLAlchemyError as e:
            print(f'Erro ao realizar operação: {e}')
            return None

    def get_by(self, entity: Type[Base], filters) -> Optional[List[Type[Base]]]:
        try:
            return self.session.query(entity).filter_by(**filters).all()
        except SQLAlchemyError as e:
            print(f'Erro ao realizar operação: {e}')
            return None

    def get_one_by(self, entity: Type[Base], filters) -> Optional[Type[Base]]:
        try:
            return self.session.query(entity).filter_by(**filters).one_or_none()
        except SQLAlchemyError as e:
            print(f'Erro ao realizar operação: {e}')
            return None

    def get_or_add(self, entity: Type[Base], data: Dict) -> Optional[int]:
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

    def update(self, entity: Type[Base], entity_id: int, updates: Dict[str, Any]) -> bool:
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

    def delete(self, entity: Type[Base], entity_id: int) -> bool:
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
