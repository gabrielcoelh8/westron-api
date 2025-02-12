import os
from typing import Optional

from app.database.models.extrato_bancario import ExtratoBancario
from app.database.models.instituicao_financeira import InstituicaoFinanceira
from app.database.models.extrato_bancario_alias import ExtratoBancarioAlias
from app.database.models.instituicao_financeira_alias import InstituicaoFinanceiraAlias
from app.database.models.prompt_extrato_bancario import PromptExtratoBancario
from app.database.impl.sqlalchemy_database_service import SqlAlchemyDatabaseService

instuicoes_financeiras_alias = {
    'banco_bradesco': [
        'Bradesco',
        'bradesco net empresa',
        'BRADESCO S/A',
        'FUNDACAO BRADESCO',
        'Banco Bradesco S.A.',
        'FUNDACAO HOSPITALAR DE COSTA RICA',
    ],
    'banco_do_brasil': [
        'BANCO DO BRASIL',
        'BB',
        'EMPRESA',
        'EMPRESARIAL',
        'BB RENDE FÁCIL',
        'FUNDACAO M S C - FUMAGROS',
        'FUNDACAO E CRISTO REI'
    ],
    'banco_daycoval': [
        'BancoDaycoval'
    ],
    'caixa_economica': [
        'Caixa',
        'CAIXA FACIL RENDA FIXA SIMPLES',
        'Caixa Econômica Federal',
    ],
    'banco_sicredi': [
        'Sicredi',
        'COOP.CRED.POUP INV UNIAO MS/TO OESTE BA',
        'SISTEMA SICREDI',
    ],
    'banco_itau': [
        'itaú',
        'ItaúEmpresas',
        'itaúBBA'
    ],
    'banco_stone': [
        'stone'
    ],
    'banco_santander': [
        'Santander'
    ],
    'banco_sicoob': [
        'SICOOB'
    ]
}

tipos_de_extratos_alias = {
    'lancamentos_periodo': [
        'lançamentos período'
    ],
    'consultas_extrato_de_conta_corrente': [
        'Consultas - Extrato de conta corrente'
    ],
    'conta_corrente': [
        'Conta Corrente'
    ],
    'extrato': [
        'Extrato'
    ],
    'extrato_de_aplicacao_deposito_a_prazo_detalhado_por_data_de_aplicacao': [
        'Extrato de Aplicação - Depósito a Prazo - Detalhado - por Data de Aplicação'
    ],
    'extrato_de_aplicacao_deposito_a_prazo_detalhado_consolidado': [
        'Extrato de Aplicação - Depósito a Prazo - Detalhado - Consolidado'
    ],
    'extrato_de_aplicacao_deposito_a_prazo_simplificado_consolidado': [
        'Extrato de Aplicação - Depósito a Prazo - Simplificado - Consolidado'
    ],
    'extrato_de_apropriacao_diaria': [
        'Extrato de Apropriação Diária'
    ],
    'extrato_de_cdbs_letras_investplus_para_simples_conferencia': [
        'Extrato de CDBs / LETRAS / INVESTPLUS - Para Simples Conferência'
    ],
    'extrato_de_investimentos': [
        'Extrato de Investimentos'
    ],
    'extrato_do_cliente': [
        'Extrato do Cliente'
    ],
    'extrato_para_simples_verificacao': [
        'Extrato para simples verificação',
        'EXTRATO PARA SIMPLES VERIFICACAO'
    ],
    'extrato_conta_corrente': [
        'Extrato Conta Corrente'
    ],
    'extrato_deposito_a_prazo': [
        'Extrato Depósito a Prazo'
    ],
    'extrato_detalhado': [
        'Extrato Detalhado'
    ],
    'extrato_fundo_de_investimento': [
        'Extrato Fundo de Investimento'
    ],
    'extrato_fundo_de_investimento_para_simples_verificacao': [
        'Extrato Fundo de Investimento Para simples verificação'
    ],
    'extrato_mensal': [
        'Extrato Mensal'
    ],
    'extrato_mensal_por_periodo': [
        'Extrato Mensal / Por Período'
    ],
    'extrato_por_periodo': [
        'Extrato por período'
    ],
    'extratos_compromissada_bb_aplic': [
        'Extratos - Compromissada BB Aplic'
    ],
    'extratos_cdb_rdb_e_bb_reaplic': [
        'Extratos - CDB / RDB e BB Reaplic'
    ],
    'extratos_investimentos_fundos_mensal': [
        'Extratos - Investimentos Fundos - Mensal'
    ],
    'extrato_de_conta_corrente': [
        'EXTRATO DE CONTA CORRENTE'
    ],
    'extrato_de_deposito_a_prazo_detalhado': [
        'EXTRATO DE DEPOSITO A PRAZO DETALHADO'
    ],
    'extrato_mensal_de_poupanca': [
        'EXTRATO MENSAL DE POUPANÇA'
    ],
    'extrato_movimentacoes_detalhado': [
        'EXTRATO MOVIMENTACOES DETALHADO'
    ],
    'informe_de_rendimentos_financeiros': [
        'Informe de Rendimentos Financeiros'
    ],
    'informativo_mensal_cdb_flex_empresarial': [
        'INFORMATIVO MENSAL CDB FLEX EMPRESARIAL'
    ],
    'resumo_de_movimentacao': [
        'Resumo de Movimentação'
    ],
    'resumo_do_mes': [
        'Resumo do mês'
    ]
}


def get_index_interval(text: str, start_string: str, end_string: Optional[str] = None) -> str:
    """
    Retorna o trecho de uma string delimitado pelas sub-strings `start_string` e `end_string`.

    :param text: String completa na qual a busca será realizada.
    :param start_string: Sub-string que marca o início.
    :param end_string: (Opcional) Sub-string que marca o final, se indefinida, será o último index de `text`.

    :return: `text` entre `start_string` e `end_string`.
    """
    start_index = text.find(start_string)  # retorna -1 ao falhar
    # Verifica se start_string foi encontrado
    if start_index == -1:
        return ""  # valor padrão
    start_index += len(start_string)  # apartir do index inicial
    if end_string is None:
        end_index = len(text)
    else:
        end_index = text.find(end_string, start_index)
        # Verifica se end_string foi encontrado
        if end_index == -1:
            end_index = len(text)  # pode causar erro se a string completa não estiver padronizada
    return text[start_index:end_index].strip()


def split_textfile_to_dict(arquivo_path: str) -> list:
    """
    Abre o arquivo .txt e divide em um dict.

    :param arquivo_path: caminho do arquivo.
    """
    dict_result = {}
    # campo:chave
    campos = {
        "instrucao_agencia": "numero_da_agencia:",
        "instrucao_conta": "numero_da_conta:",
        "instrucao_periodo": "periodo:",
        "instrucao_data_saldo": "data_do_saldo:",
        "instrucao_saldo": "\nsaldo:",  # pode ser confundido com o data_do_saldo
        "instrucao_outras": "Observações:"
    }
    with open(arquivo_path, 'r') as arquivo:
        text = arquivo.read()
        # Itera sobre as linhas do arquivo separando a string em um dict
        for i, (chave, campo) in enumerate(campos.items()):
            campo_start = campo
            campo_end = list(campos.values())[i + 1] if i + 1 < len(campos) else None
            dict_result[chave] = get_index_interval(
                text=text,
                start_string=campo_start,
                end_string=campo_end
            )
    return [dict_result]

def get_prompt_from_file(arquivo_path: str) -> list:
    with open(arquivo_path, 'r') as arquivo:
        text = arquivo.read()
    return [dict(prompt=text, espacamento=1)]

class Prompt(SqlAlchemyDatabaseService):
    def __init__(self):
        super().__init__()
        self.base_path = os.environ.get('PROMPTS_DE_EXTRATOS_BANCARIOS')

    def dirs_to_list(self) -> list:
        """
        Captura informações de txt's de um diretorio e seus subdiretorios, afim de formar uma list padronizada.
        """
        records = []
        for instituicao_financeira in os.listdir(self.base_path):
            pasta_path = os.path.join(self.base_path, instituicao_financeira)
            if os.path.isdir(pasta_path):
                aliases = [dict(nome=alias) for alias in instuicoes_financeiras_alias.get(instituicao_financeira, [])]

                extratos_bancarios = []
                for extrato_bancario in os.listdir(pasta_path):
                    arquivo_path = os.path.join(pasta_path, extrato_bancario)
                    if extrato_bancario.endswith('.txt'):
                        tipo_extrato = extrato_bancario[:-4]

                        alias_extrato = [dict(tipo=alias) for alias in
                                         tipos_de_extratos_alias.get(tipo_extrato, [])]
                        prompts_data = get_prompt_from_file(arquivo_path)
                        prompts = [dict(**data) for data in prompts_data]

                        extrato = dict(tipo=tipo_extrato.replace('_', ' ').title(),
                                       aliases_extrato_bancario=alias_extrato,
                                       prompts_extrato_bancario=prompts)
                        extratos_bancarios.append(extrato)

                instituicao = dict(nome=instituicao_financeira.replace('_', ' ').title(),
                                   aliases_instituicao_financeira=aliases,
                                   extratos_bancarios=extratos_bancarios)
                records.append(instituicao)
        return records

    def create(self, records: list[dict]):
        """
        Organiza registros e salva as entidades no banco de dados.

        :param records: lista de dicionarios de registros
        """
        for record in records:
            # criação da instituição financeira
            instituicao_dict = dict(nome=record['nome'])
            id_inst = self.get_or_add(InstituicaoFinanceira, instituicao_dict)
            # criação dos aliases da instituição financeira
            aliases_inst_list = [dict(nome=alias['nome'], instituicao_financeira_id=id_inst)
                                 for alias in record['aliases_instituicao_financeira']]
            for alias in aliases_inst_list:
                self.add(InstituicaoFinanceiraAlias, alias)
            # criação de extratos
            for extrato in record['extratos_bancarios']:
                extrato_dict = dict(tipo=extrato['tipo'], instituicao_financeira_id=id_inst)
                id_extrato = self.get_or_add(ExtratoBancario, extrato_dict)
                # criação dos aliases dos extratos
                aliases_ext_list = [dict(tipo=alias['tipo'], extrato_bancario_id=id_extrato)
                                    for alias in extrato['aliases_extrato_bancario']]
                for alias in aliases_ext_list:
                    self.add(ExtratoBancarioAlias, alias)
                # criação dos prompts
                prompt_list = extrato['prompts_extrato_bancario']
                prompts = [dict(instituicao_financeira_id=id_inst, extrato_bancario_id=id_extrato, **_prompt)
                           for _prompt in prompt_list]
                for item in prompts:
                    self.add(PromptExtratoBancario, item)

    def initialize(self):
        list_of_prompts = self.dirs_to_list()
        self.create(list_of_prompts)
        return


if __name__ == '__main__':
    prompt = Prompt()
    prompt.initialize()
