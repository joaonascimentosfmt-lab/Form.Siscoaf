from dataclasses import dataclass, field
from typing import Dict, List

LIMITE_ESPECIE = 50000.0

@dataclass
class ScoringConfig:
    pep: int = 3
    especie: int = 2
    sem_origem: int = 3
    fraude: int = 5
    fracionamento: int = 3
    lavagem: int = 5
    ocultacao: int = 4
    terceiros_sem_justificativa: int = 2
    valor_incompativel: int = 2
    operacoes_relacionadas: int = 3
    limite_comunicacao: int = 8

@dataclass
class SituacaoItem:
    chave: str
    texto: str
    pontuacao: int

def obter_situacoes() -> List[SituacaoItem]:
    return [
        SituacaoItem(chave="sem_origem", texto="Cliente não soube explicar origem do dinheiro", pontuacao=3),
        SituacaoItem(chave="valor_incompativel", texto="Valor incompatível com patrimônio", pontuacao=2),
        SituacaoItem(chave="terceiros_sem_justificativa", texto="Uso de terceiros sem justificativa", pontuacao=2),
        SituacaoItem(chave="interpostas_pessoas", texto="Uso de interpostas pessoas", pontuacao=3),
        SituacaoItem(chave="movimentacao_especie", texto="Grande movimentação em espécie", pontuacao=2),
        SituacaoItem(chave="sem_finalidade", texto="Operação sem finalidade econômica aparente", pontuacao=2),
        SituacaoItem(chave="resistencia_documentos", texto="Resistência em fornecer documentos", pontuacao=3),
        SituacaoItem(chave="documentacao_inconsistente", texto="Documentação inconsistente", pontuacao=3),
        SituacaoItem(chave="operacoes_curto_periodo", texto="Diversas operações em curto período", pontuacao=2),
        SituacaoItem(chave="indicios_lavagem", texto="Indícios de lavagem de dinheiro", pontuacao=5),
        SituacaoItem(chave="indicios_ocultacao", texto="Indícios de ocultação patrimonial", pontuacao=4),
        SituacaoItem(chave="indicios_fraude", texto="Indícios de fraude", pontuacao=5),
        SituacaoItem(chave="outro_indicio", texto="Outro indício relevante", pontuacao=2),
    ]

TIPO_ATO_OPCOES = [
    "Compra e venda",
    "Doação",
    "Permuta",
    "Constituição de garantia",
    "Alienação fiduciária",
    "Integralização de capital",
    "Procuração",
    "Escritura diversa",
    "Ata Notarial",
    "Outro",
]

FORMA_PAGAMENTO_OPCOES = [
    "PIX",
    "TED",
    "Dinheiro",
    "Cheque",
    "Espécie",
    "Mista",
    "Outro",
]

ESTADOS = [
    "AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO",
    "MA", "MT", "MS", "MG", "PA", "PB", "PR", "PE", "PI",
    "RJ", "RN", "RS", "RO", "RR", "SC", "SP", "SE", "TO",
]
