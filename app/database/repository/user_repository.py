from typing import Dict, Optional

from app.database.service.sqlalchemy_service import SqlAlchemyDatabaseService

from app.database.models.user_model import User
from app.schemas.database_response import InsertResponse
from app.models.token import TokenData


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
    
    def get_user(self, data: TokenData) -> Optional[User]:
        return self.get_one_by(User, data.model_dump())
