from json import load
from os import environ
from typing import Type, Dict, Union

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

def load_json(file_path: str) -> Union[dict, list]:
    with open(file_path, 'r', encoding='utf_8') as file:
        data = load(file)
    return data

def obter_prompt(tipo_de_prompt: str):
    arquivo_de_prompts = environ.get('PROMPTS_PATH')
    prompts = load_json(arquivo_de_prompts)
    prompt = prompts.get(tipo_de_prompt)
    if prompt is None:
        raise ValueError(f'O tipo de prompt informado {tipo_de_prompt!r} não existe')
    return prompt