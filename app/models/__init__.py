from pydantic import BaseModel


class ExtratoBancarioModel(BaseModel):
    id: int
    tipo: str
    instituicao_financeira_id: int

    class Config:
        from_attributes = True
