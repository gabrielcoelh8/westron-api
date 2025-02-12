from pydantic import BaseModel


class ExtratoBancario(BaseModel):
    nome_da_instituicao_financeira: str
    tipo_de_extrato_bancario: str


class DataSaldo(BaseModel):
    dia: str
    mes: str
    ano: str


class PeriodoSaldo(BaseModel):
    data_inicial: DataSaldo
    data_final: DataSaldo


class InformacoesDetalhadas(BaseModel):
    numero_da_agencia: str
    numero_da_conta: str
    periodo_do_extrato: PeriodoSaldo
    data_do_saldo: str
    saldo: str
