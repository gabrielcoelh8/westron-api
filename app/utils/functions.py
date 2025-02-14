from typing import Type, Dict

from pydantic import BaseModel

from app.database.meta.declarative import Base


def notnone_hasattr(model: Type[Base], data: Dict) -> Dict:
    """Remove valores None e verifica se model possui atributos"""
    return {key: value for key, value in data.items() if value is not None and hasattr(model, key)}


def to_pydantic(entity: Type[Base], model: Type[BaseModel]):
    return model.model_validate(entity)


def format_string_for_query(value: str) -> str:
    """
    Formata uma string para ser usada na consulta:
    - Remove espaços e underscores
    - Converte para uppercase
    """
    return value.replace(" ", "").replace("_", "").upper()
