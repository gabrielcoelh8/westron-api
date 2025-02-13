from os import environ
from typing import Optional

from app.services.chat_gpt.chat_gpt import ChatGPT
from app.services.rebuild_ocr_document.utils.json_utils import load_json
from app.database.impl.repository_instituicao_financeira import InstituicaoFinanceiraRepository
from app.database.impl.repository_extrato_bancario import ExtratoBancarioRepository
from app.database.impl.repository_prompt_extrato_bancario import PromptExtratoBancarioRepository
from app.schemas.gpt_responses import ExtratoBancario, InformacoesDetalhadas
from app.schemas.requests_ocr import DadosBancarios

repo_instituicao = InstituicaoFinanceiraRepository()
repo_extrato = ExtratoBancarioRepository()
repo_prompt = PromptExtratoBancarioRepository()


def obter_nome_de_banco_e_tipo_de_extrato(texto: str) -> dict:
    dados_cadastrados = repo_instituicao.get_all_instituicoes_infomation()
    complemento = obter_prompt(tipo_de_prompt='dados_bancarios').format(dados_cadastrados)
    prompt = obter_prompt(tipo_de_prompt='default').format(complemento)
    chat_gpt = ChatGPT(prompt, texto, response_format=ExtratoBancario)
    resposta = chat_gpt.get_parsed_response()
    return resposta


def obter_prompt(tipo_de_prompt: str):
    arquivo_de_prompts = environ.get('BASE_PROMPT')
    prompts = load_json(arquivo_de_prompts)
    prompt = prompts.get(tipo_de_prompt)
    if prompt is None:
        raise ValueError(f'O tipo de prompt informado {tipo_de_prompt!r} não existe')
    return prompt


def obter_instrucoes_prompt(instituicao_financeira: str, tipo_de_extrato: str) -> Optional[str]:
    if not (bank := repo_instituicao.get_instituicao_financeira_by_nome(instituicao_financeira)):
        print(f"Erro: Instituição financeira não encontrada - {instituicao_financeira}")
        return None
    
    if not (extract := repo_extrato.get_extrato_bancario_by_tipo(tipo_de_extrato, bank.id)):
        print(f"Erro: Tipo de extrato não encontrado - {tipo_de_extrato}")
        return None
    
    if not (prompt_item := repo_prompt.get_last_prompt_by_extrato_bancario_id(extract.id)):
        print(f"Erro: Prompt não encontrado para extrato - {tipo_de_extrato}")
        return None

    instrucoes = prompt_item.prompt
    return "\n".join(instrucoes) if instrucoes else None


def obter_saldo_detalhado_por_gpt(texto: str, dados: DadosBancarios, instrucoes: str = None) -> dict:
    banco = dados.nome_da_instituicao_financeira
    extrato = dados.tipo_de_extrato
    instrucoes = obter_instrucoes_prompt(banco, extrato) if instrucoes is None else instrucoes
    if instrucoes:
        complemento = obter_prompt(tipo_de_prompt='saldo_detalhado').format(banco, extrato, instrucoes)
        prompt = obter_prompt(tipo_de_prompt='default').format(complemento)
    else:
        prompt = obter_prompt(tipo_de_prompt='default')
    
    chat_gpt = ChatGPT(prompt, texto, response_format=InformacoesDetalhadas)
    resposta = chat_gpt.get_parsed_response()
    return resposta


def obter_registros_bancarios(texto: str) -> dict:
    dados = obter_nome_de_banco_e_tipo_de_extrato(texto)
    registros_bancarios = obter_saldo_detalhado_por_gpt(texto, dados)
    registros_bancarios.update(dados)
    return registros_bancarios
