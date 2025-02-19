from typing import Dict

from app.database.service.sqlalchemy_service import SqlAlchemyDatabaseService

from app.database.models.user_model import User
from app.schemas.database_response import InsertResponse
from app.schemas.user_request import CreateRequest


class UserRepository(SqlAlchemyDatabaseService):
    def add_user(self, data: Dict) -> InsertResponse:
        try:
            insert_response = self.add(User, data)
        except ValueError as e:
            mensagem = str(e)
            insert_response = InsertResponse(
                success=False, 
                message=mensagem, 
                id=None, 
                status_code=402
            )
        except Exception as e:
            mensagem = f'Exceção não mapeada: {str(e)}'
            insert_response = InsertResponse(
                success=False, 
                message=mensagem, 
                id=None, 
                status_code=400
            )
        return insert_response
