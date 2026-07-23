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
    docs_incompletas: int = 2
    limite_comunicacao: int = 8

@dataclass
class SituacaoItem:
    chave: str
    texto: str
    pontuacao: int

def obter_situacoes() -> List[SituacaoItem]:
    return [
        SituacaoItem(chave="nao_decorrer_ativ_usuais", texto="Art. 155-A, I - Aparentem não decorrer de atividades ou negócios usuais do cliente, de outros envolvidos ou do seu ramo de atuação", pontuacao=3),
        SituacaoItem(chave="origem_fundamentacao_nao_aferivel", texto="Art. 155-A, II - Tenham origem ou fundamentação econômica ou legal não claramente aferíveis", pontuacao=3),
        SituacaoItem(chave="incompativeis_patrimonio", texto="Art. 155-A, III - Se mostrem incompatíveis com o patrimônio ou com a capacidade econômico-financeira do cliente ou de outros envolvidos", pontuacao=3),
        SituacaoItem(chave="dificil_identificacao_beneficiario", texto="Art. 155-A, IV - Envolvam difícil ou inviável identificação de beneficiário(s) final(is)", pontuacao=3),
        SituacaoItem(chave="pessoa_juridica_gafi_alto_risco", texto="Art. 155-A, V - Se relacionem a pessoa jurídica domiciliada em jurisdição listada pelo Gafi como de alto risco ou com deficiências estratégicas em matéria de PLD/FTP", pontuacao=3),
        SituacaoItem(chave="paises_rfb_tributacao_favorecida", texto="Art. 155-A, VI - Envolvam países ou dependências listados pela RFB como de tributação favorecida e/ou regime fiscal privilegiado", pontuacao=3),
        SituacaoItem(chave="pj_socios_gafi", texto="Art. 155-A, VII - Se relacionem a pessoa jurídica cujos sócios, administradores, beneficiários finais, procuradores ou representantes legais mantenham domicílio em jurisdições consideradas pelo Gafi de alto risco", pontuacao=3),
        SituacaoItem(chave="resistencia_fornecimento_info", texto="Art. 155-A, VIII - Apresentem, por parte de cliente ou demais envolvidos, resistência ao fornecimento de informação ou documentação solicitada", pontuacao=3),
        SituacaoItem(chave="informacao_documentacao_falsa", texto="Art. 155-A, IX - Envolvam a prestação, por parte de cliente ou demais envolvidos, de informação ou documentação falsa ou de difícil ou onerosa verificação", pontuacao=4),
        SituacaoItem(chave="complexas_onerosas_injustificadas", texto="Art. 155-A, X - Se mostrem injustificadamente mais complexas ou onerosas que de ordinário, mormente se isso puder dificultar o rastreamento de recursos ou a identificação de real propósito", pontuacao=3),
        SituacaoItem(chave="sinais_carater_ficticio", texto="Art. 155-A, XI - Apresentem sinais de caráter fictício ou de relação com valores incompatíveis com os de mercado", pontuacao=4),
        SituacaoItem(chave="clausulas_incompativeis_mercado", texto="Art. 155-A, XII - Envolvam cláusulas que estabeleçam condições incompatíveis com as praticadas no mercado", pontuacao=3),
        SituacaoItem(chave="tentativa_burlar_controles", texto="Art. 155-A, XIII - Aparentem tentativa de burlar controles e registros exigidos pela legislação de PLD/FTP, inclusive mediante fracionamento ou pagamento em espécie, com título emitido ao portador ou por outros meios que dificultem a rastreabilidade", pontuacao=5),
        SituacaoItem(chave="documento_estrangeiro_dificuldade", texto="Art. 155-A, XIV - Envolvam o registro de documento de procedência estrangeira que ofereçam dificuldade significativa para a compreensão do seu sentido jurídico no contexto da atividade notarial ou registral", pontuacao=3),
        SituacaoItem(chave="substancial_ganho_capital", texto="Art. 155-A, XV - Revelem substancial ganho de capital em curto período", pontuacao=3),
        SituacaoItem(chave="procuracao_amplos_poderes", texto="Art. 155-A, XVI - Envolvam lavratura ou utilização de instrumento de procuração que outorgue amplos poderes de administração, especialmente quando conferidos em caráter irrevogável ou irretratável ou isento de prestação de contas", pontuacao=4),
        SituacaoItem(chave="aumento_capital_destoante", texto="Art. 155-A, XVII - Revelem operações de aumento de capital social que pareçam destoar dos efetivos atributos de valor, patrimônio ou outros aspectos relacionados às condições econômico-financeiras da sociedade", pontuacao=3),
        SituacaoItem(chave="outras_operacoes_indicios_ldftp", texto="Art. 155-A, XVIII - Quaisquer outras operações, propostas de operação ou situações que possam configurar sérios indícios de práticas de LD/FTP ou de infrações que com elas se relacionem", pontuacao=4),
        SituacaoItem(chave="emprego_nao_usual_pagamento_anonimo", texto="Art. 155-A, Parágrafo único, I - Revelem emprego não usual de meio ou forma de pagamento que possa viabilizar anonimato ou dificultar a rastreabilidade, como uso de valores anormalmente elevados em espécie, título ao portador ou ativo virtual não vinculado nominalmente", pontuacao=4),
        SituacaoItem(chave="relacao_terrorismo", texto="Art. 155-A, Parágrafo único, II - Apresentem algum sinal de possível relação com práticas de terrorismo ou proliferação de armas de destruição em massa ou com seus financiamentos", pontuacao=5),
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
