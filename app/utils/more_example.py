import re
import json
from typing import Dict, Optional, Tuple


def _clean_text(text: str) -> str:
    """
    Limpa e normaliza o texto OCR.
    """
    return re.sub(r'\s+', ' ', text).strip()


class BankStatementParser:
    """
    Processa textos OCR para identificar o nome do banco e o tipo de extrato.
    """

    def __init__(self, _mappings: str | dict):
        """
        Inicializa o parser com configurações JSON ou dicionário.
        """
        self.mappings = json.loads(_mappings) if isinstance(_mappings, str) else _mappings

    @staticmethod
    def _create_pattern(text: str) -> re.Pattern:
        """
        Gera um padrão regex flexível a partir de um texto.
        """
        escaped = re.escape(text).replace(r"\ ", r"\s+")
        return re.compile(f"(?i){escaped}")

    def _find_bank(self, cleaned_text: str) -> Optional[str]:
        """
        Identifica o banco no texto limpo.
        """
        for bank_name, bank_data in self.mappings.items():
            bank_patterns = bank_data.get("bank_patterns", [])
            for pattern in bank_patterns:
                if re.search(self._create_pattern(pattern), cleaned_text):
                    return bank_name
        return None

    def _find_statement_type(self, bank_name: str, cleaned_text: str) -> Optional[str]:
        """
        Identifica o tipo de extrato com base no nome do banco.
        """
        bank_data = self.mappings.get(bank_name, {})
        statement_types = bank_data.get("statements", {})

        for statement_type, patterns in statement_types.items():
            for pattern in patterns:
                if re.search(self._create_pattern(pattern), cleaned_text):
                    return statement_type
        return None

    def extract_info(self, _ocr_text: str) -> Dict[str, Optional[str]]:
        """
        Extrai o nome do banco e o tipo de extrato do texto OCR.
        """
        cleaned_text = _clean_text(_ocr_text)

        # Identificar o banco
        bank_name = self._find_bank(cleaned_text)
        if not bank_name:
            return {"bank_name": None, "statement_type": None}

        # Identificar o tipo de extrato
        statement_type = self._find_statement_type(bank_name, cleaned_text)
        return {"bank_name": bank_name, "statement_type": statement_type}


# Exemplo de uso
if __name__ == "__main__":
    # Configurações de exemplo
    mappings = {
        "Banco Daycoval": {
            "bank_patterns": [
                "Banco Daycoval",
                "Dayconnect",
                "Dayco Serviços"
            ],
            "statements": {
                "Extrato Detalhado": [
                    "Extrato Detalhado",
                    "Resumo de Movimentações Detalhado"
                ],
                "Relatório de Investimentos": [
                    "Relatório de Investimentos",
                    "Investimentos Atualizados"
                ]
            }
        },
        "Banco do Brasil": {
            "bank_patterns": [
                "Banco do Brasil",
                "BB Seguros"
            ],
            "statements": {
                "Extrato Mensal": [
                    "Extrato Mensal",
                    "Resumo Mensal de Conta"
                ],
                "Extrato Simplificado": [
                    "Extrato Simplificado",
                    "Resumo Simplificado"
                ]
            }
        }
    }

    # Texto OCR gerado por IA
    ocr_text = """
        Data: 03/01/2022 12:45
        Dayconnect - Banco Daycoval
        Aqui está o seu Resumo de Movimentações Detalhado
    """

    parser = BankStatementParser(mappings)
    result = parser.extract_info(ocr_text)
    print(f"Banco: {result.get('bank_name')}, Tipo de Extrato: {result.get('statement_type')}")
