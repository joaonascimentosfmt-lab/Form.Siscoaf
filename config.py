from dataclasses import dataclass, field
from typing import Dict, List, Optional
import json
import os


CONFIG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "siscoaf_config.json")


def _carregar_config_json() -> dict:
    padrao = {
        "servicos": {
            "Escritura": ["Compra e venda", "Doação", "Permuta", "Constituição de garantia", "Alienação fiduciária", "Integralização de capital", "Ata Notarial"],
            "Procuração": ["Amplos Poderes", "Gestão e Movimentação Bancária", "Compra, Venda e Administração de Imóveis", "Representação em Inventário e Partilha"],
            "Protesto": [],
            "Pessoa Jurídica": [],
            "FormaPagamento": ["Não especificado", "PIX", "TED", "Dinheiro", "Cheque", "Boleto bancário", "Mista"],
        }
    }
    try:
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                dados = json.load(f)
                if "servicos" in dados:
                    for cat in padrao["servicos"]:
                        if cat in dados["servicos"]:
                            padrao["servicos"][cat] = dados["servicos"][cat]
    except Exception:
        pass
    return padrao


def obter_tipos_servico(categoria: str) -> List[str]:
    config = _carregar_config_json()
    return config.get("servicos", {}).get(categoria, [])


def salvar_tipos_servico(categoria: str, tipos: List[str]):
    config = _carregar_config_json()
    config["servicos"][categoria] = tipos
    try:
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
    except Exception:
        pass


SETOR_GERAL = "Disposições Gerais"
SETOR_PROTESTO = "Tabelionato de Protesto"
SETOR_RCPJ = "Registro Civil das Pessoas Jurídicas (RCPJ)"
SETOR_NOTAS = "Tabelionato de Notas"
SETOR_IMOVEIS = "Registro de Imóveis"

CATEGORIA_SETORES = {
    "Escritura": [SETOR_GERAL, SETOR_NOTAS],
    "Procuração": [SETOR_GERAL, SETOR_NOTAS],
    "Protesto": [SETOR_GERAL, SETOR_PROTESTO],
    "Pessoa Jurídica": [SETOR_GERAL, SETOR_RCPJ],
    "Registro de Imóveis": [SETOR_GERAL, SETOR_IMOVEIS],
}

DECISAO_COMUNICAR = "comunicar_objetiva"
DECISAO_ATENCAO = "atencao_especial"
DECISAO_SUSPEITA = "indicio_suspeita"

TIPO_DECISAO_POR_CODIGO = {
    "1376": DECISAO_COMUNICAR, "1379": DECISAO_COMUNICAR, "1386": DECISAO_COMUNICAR, "1391": DECISAO_COMUNICAR,
    "1377": DECISAO_ATENCAO, "1378": DECISAO_ATENCAO,
    "1380": DECISAO_ATENCAO, "1381": DECISAO_ATENCAO, "1382": DECISAO_ATENCAO, "1383": DECISAO_ATENCAO, "1384": DECISAO_ATENCAO, "1385": DECISAO_ATENCAO,
    "1387": DECISAO_ATENCAO, "1388": DECISAO_ATENCAO, "1389": DECISAO_ATENCAO, "1390": DECISAO_ATENCAO,
    "1392": DECISAO_ATENCAO, "1393": DECISAO_ATENCAO, "1394": DECISAO_ATENCAO, "1395": DECISAO_ATENCAO, "1396": DECISAO_ATENCAO, "1397": DECISAO_ATENCAO,
}

CODIGOS_POR_SETOR = {
    SETOR_GERAL: {"1356","1357","1358","1359","1360","1361","1362","1363","1364","1365","1366","1367","1368","1369","1370","1372","1373","1374","1375"},
    SETOR_PROTESTO: {"1376","1377","1378"},
    SETOR_RCPJ: {"1386","1387","1388","1389","1390"},
    SETOR_NOTAS: {"1371","1391","1392","1393","1394","1395","1396","1397"},
    SETOR_IMOVEIS: {"1379","1380","1381","1382","1383","1384","1385"},
}

@dataclass
class ScoringConfig:
    pep: int = 3
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
    codigo: str
    artigo: str
    texto: str
    pontuacao: int
    setor: str = SETOR_GERAL
    tipo: str = DECISAO_SUSPEITA
    pergunta: str = ""
    exemplo: str = ""

def _item(
    chave: str, codigo: str, artigo: str, texto_legal: str,
    pergunta: str, exemplo: str = "",
    pontuacao: int = 2, setor: str = SETOR_GERAL,
) -> SituacaoItem:
    return SituacaoItem(
        chave=chave, codigo=codigo, artigo=artigo,
        texto=texto_legal, pontuacao=pontuacao, setor=setor,
        tipo=TIPO_DECISAO_POR_CODIGO.get(codigo, DECISAO_SUSPEITA),
        pergunta=pergunta, exemplo=exemplo,
    )

def obter_setor_por_codigo(codigo: str) -> str:
    for setor, codigos in CODIGOS_POR_SETOR.items():
        if codigo in codigos:
            return setor
    return SETOR_GERAL

def obter_situacoes(categoria: Optional[str] = None) -> List[SituacaoItem]:
    todas = [
        # ── Art. 155-A, I a XVIII — Indícios de Suspeita (Gerais) ──
        _item("cod_1356", "1356", "Art. 155-A, I",
            "Art. 155-A, I - aparentem não decorrer de atividades ou negócios usuais do cliente, de outros envolvidos ou do seu ramo de atuação;",
            "A operação foge do que seria esperado para o cliente ou seu ramo de atividade?",
            "Ex: Advogado registrando compra de gado em seu nome"),
        _item("cod_1357", "1357", "Art. 155-A, II",
            "Art. 155-A, II - tenham origem ou fundamentação econômica ou legal não claramente aferíveis;",
            "A origem do dinheiro ou a razão do negócio não está clara?",
            "Ex: Parte diz \"ganhei em jogo\" sem qualquer comprovante"),
        _item("cod_1358", "1358", "Art. 155-A, III",
            "Art. 155-A, III - se mostrem incompatíveis com o patrimônio ou com a capacidade econômico-financeira do cliente ou de outros envolvidos;",
            "O valor do negócio é grande demais para o patrimônio ou a renda da parte?",
            "Ex: Aposentado de 1 salário mínimo comprando imóvel de R$ 800 mil à vista"),
        _item("cod_1359", "1359", "Art. 155-A, IV",
            "Art. 155-A, IV - envolvam difícil ou inviável identificação de beneficiário(s) final(is);",
            "É difícil identificar quem é o verdadeiro beneficiário do negócio?",
            "Ex: Pessoa jurídica com sócio oculto ou cadeia societária complexa"),
        _item("cod_1360", "1360", "Art. 155-A, V",
            "Art. 155-A, V - se relacionem a pessoa jurídica domiciliada em jurisdição listada pelo Grupo de Ação Financeira (Gafi) como de alto risco ou com deficiências estratégicas em matéria de PLD/FTP;",
            "A empresa envolvida fica em jurisdição considerada de alto risco pelo GAFI?",
            "Ex: Offshore nas Ilhas Cayman ou paraíso fiscal"),
        _item("cod_1361", "1361", "Art. 155-A, VI",
            "Art. 155-A, VI - envolvam países ou dependências listados pela RFB como de tributação favorecida e/ou regime fiscal privilegiado;",
            "O negócio envolve país com tributação favorecida (paraíso fiscal)?",
            "Ex: Empresa com sede em país de tributação privilegiada"),
        _item("cod_1362", "1362", "Art. 155-A, VII",
            "Art. 155-A, VII - se relacionem a pessoa jurídica cujos sócios, administradores, beneficiários finais, procuradores ou representantes legais mantenham domicílio em jurisdições consideradas pelo Gafi de alto risco ou com deficiências estratégicas em matéria de PLD/FTP;",
            "Sócios ou representantes da empresa moram em paraíso fiscal?",
            "Ex: Todos os sócios residem em jurisdição de alto risco"),
        _item("cod_1363", "1363", "Art. 155-A, VIII",
            "Art. 155-A, VIII - apresentem, por parte de cliente ou demais envolvidos, resistência ao fornecimento de informação ou documentação solicitada para fins relacionados ao disposto neste Capítulo;",
            "A parte dificulta ou se recusa a fornecer documentos ou informações?",
            "Ex: Cliente se recusa a apresentar comprovante de renda ou origem do dinheiro"),
        _item("cod_1364", "1364", "Art. 155-A, IX",
            "Art. 155-A, IX - envolvam a prestação, por parte de cliente ou demais envolvidos, de informação ou documentação falsa ou de difícil ou onerosa verificação;",
            "Há indícios de documento ou informação falsa?",
            "Ex: Declaração de renda incompatível, RG suspeito, certidão falsa"),
        _item("cod_1365", "1365", "Art. 155-A, X",
            "Art. 155-A, X - se mostrem injustificadamente mais complexas ou onerosas que de ordinário, mormente se isso puder dificultar o rastreamento de recursos ou a identificação de real propósito;",
            "A operação é mais complexa ou cara que o normal sem justificativa?",
            "Ex: Cadeia de procurações em cascata sem razão aparente"),
        _item("cod_1366", "1366", "Art. 155-A, XI",
            "Art. 155-A, XI - apresentem sinais de caráter fictício ou de relação com valores incompatíveis com os de mercado;",
            "Há sinais de que o negócio pode ser fictício ou com valor fora do mercado?",
            "Ex: Venda de imóvel por valor muito abaixo da avaliação fiscal"),
        _item("cod_1367", "1367", "Art. 155-A, XII",
            "Art. 155-A, XII - envolvam cláusulas que estabeleçam condições incompatíveis com as praticadas no mercado;",
            "As condições do negócio fogem das práticas normais de mercado?",
            "Ex: Juros zero em empréstimo entre particulares sem garantia"),
        _item("cod_1368", "1368", "Art. 155-A, XIII",
            "Art. 155-A, XIII - aparentem tentativa de burlar controles e registros exigidos pela legislação de PLD/FTP, inclusive mediante fracionamento ou pagamento em espécie, com título emitido ao portador ou por outros meios que dificultem a rastreabilidade;",
            "Há suspeita de tentativa de burlar controles (fracionamento, dinheiro em espécie)?",
            "Ex: Múltiplos depósitos fracionados no mesmo dia ou pagamento em espécie sem justificativa"),
        _item("cod_1369", "1369", "Art. 155-A, XIV",
            "Art. 155-A, XIV - envolvam o registro de documento de procedência estrangeira, nos termos do art. 129, 6º, combinado com o art. 148 da Lei n. 6.015, de 31 de dezembro de 1973, que ofereçam dificuldade significativa para a compreensão do seu sentido jurídico no contexto da atividade notarial ou registral de que se trate;",
            "O documento estrangeiro é de difícil compreensão jurídica?",
            "Ex: Trust agreement em inglês sem tradução juramentada ou parecer jurídico"),
        _item("cod_1370", "1370", "Art. 155-A, XV",
            "Art. 155-A, XV - revelem substancial ganho de capital em curto período;",
            "Houve ganho de capital muito grande em pouco tempo?",
            "Ex: Imóvel comprado há 3 meses revendido com lucro de 300%"),
        _item("cod_1371", "1371", "Art. 155-A, XVI",
            "Art. 155-A, XVI - envolvam lavratura ou utilização de instrumento de procuração que outorgue amplos poderes de administração de pessoa jurídica ou de gestão empresarial, de gerência de negócios ou de movimentação de conta bancária, de pagamento ou de natureza semelhante, especialmente quando conferidos em caráter irrevogável ou irretratável ou isento de prestação de contas, independentemente de se tratar, ou não, de procuração em causa própria ou por prazo indeterminado;",
            "A procuração dá poderes amplos demais (irrevogável, sem prestação de contas)?",
            "Ex: Procuração irrevogável para gerir empresa e movimentar contas bancárias",
            setor=SETOR_NOTAS),
        _item("cod_1372", "1372", "Art. 155-A, XVII",
            "Art. 155-A, XVII - revelem operações de aumento de capital social que pareçam destoar dos efetivos atributos de valor, patrimônio ou outros aspectos relacionados às condições econômico-financeiras da sociedade, diante de circunstâncias como, por exemplo, partes envolvidas no ato ou características do empreendimento;",
            "O aumento de capital parece irreal para o porte da empresa?",
            "Ex: Microempresa aumentando capital em R$ 10 milhões sem lastro"),
        _item("cod_1373", "1373", "Art. 155-A, XVIII",
            "Art. 155-A, XVIII - quaisquer outras operações, propostas de operação ou situações que, considerando suas características, especialmente partes, demais envolvidos, valores, modo de realização, meios e formas de pagamento, falta de fundamento econômico ou legal ou, ainda, incompatibilidade com práticas de mercado, possam configurar sérios indícios de práticas de LD/FTP ou de infrações que com elas se relacionem.",
            "Outra situação incomum que gere suspeita de lavagem de dinheiro?",
            "Ex: Operação com múltiplos fatores atípicos sem justificativa"),
        _item("cod_1374", "1374", "Art. 155-A, Parágrafo único, I",
            "Art. 155-A [...] Parágrafo único, I: Parágrafo único - Na hipótese do caput deste artigo, o notário e o registrador também atentarão para operações, propostas de operação ou situações que: I - revelem emprego não usual de meio ou forma de pagamento que possa viabilizar anonimato ou dificultar a rastreabilidade de movimentação de valores ou a identificação de quem a tenha realizado, como o uso de valores anormalmente elevados em espécie ou na forma de título emitido ao portador ou, ainda, de ativo virtual não vinculado nominalmente a quem o movimente;",
            "O meio de pagamento usado pode dificultar a identificação de quem pagou?",
            "Ex: Pagamento em criptomoeda anônima ou título ao portador"),
        _item("cod_1375", "1375", "Art. 155-A, Parágrafo único, II",
            "Art. 155-A [...] Parágrafo único, II: Parágrafo único - Na hipótese do caput deste artigo, o notário e o registrador também atentarão para operações, propostas de operação ou situações que: II - apresentem algum sinal de possível relação, direta ou indireta, com práticas de terrorismo ou proliferação de armas de destruição em massa ou com seus financiamentos, inclusive em hipóteses correlatas eventualmente contempladas em atos normativos da UIF.",
            "A operação pode ter relação com terrorismo ou armas de destruição em massa?",
            "Ex: Envolvimento com país ou pessoa sob sanções internacionais"),

        # ── Art. 159 — Comunicação Objetiva (Protesto) ──
        _item("cod_1376", "1376", "Art. 159",
            "Art. 159. O tabelião de protesto, ou seu oficial de cumprimento, comunicará à UIF, na forma do art. 151, II, qualquer operação que envolva pagamento ou recebimento em espécie, ou por título ao portador, de valor igual ou superior a R$ 100.000,00 (cem mil reais) ou ao equivalente em outra moeda, desde que perante o tabelião ou seu preposto.",
            "O pagamento ou recebimento em espécie é igual ou superior a R$ 100 mil? (Protesto)",
            "Ex: Devedor pagando R$ 150 mil em dinheiro no balcão do cartório",
            setor=SETOR_PROTESTO),

        # ── Art. 160 — Atenção Especial (Protesto) ──
        _item("cod_1377", "1377", "Art. 160, I",
            "Art. 160, I - em valor igual ou superior a R$ 100.000,00 (cem mil reais), quando o devedor for pessoa física;",
            "O protesto tem valor igual ou superior a R$ 100 mil e o devedor é pessoa física?",
            "Ex: Título de R$ 150 mil protestado contra pessoa física",
            setor=SETOR_PROTESTO),
        _item("cod_1378", "1378", "Art. 160, II",
            "Art. 160, II - em valor igual ou superior a R$ 500.000,00 (quinhentos mil reais), quando o devedor for pessoa jurídica, salvo quando se tratar de instituição do mercado financeiro, do mercado de capitais ou de órgãos e entes públicos.",
            "O protesto tem valor igual ou superior a R$ 500 mil e o devedor é pessoa jurídica?",
            "Ex: Título de R$ 800 mil protestado contra empresa (exceto instituições financeiras)",
            setor=SETOR_PROTESTO),

        # ── Art. 161 — Comunicação Objetiva (Imóveis) ──
        _item("cod_1379", "1379", "Art. 161",
            "Art. 161. O oficial de registro de imóveis, ou seu oficial de cumprimento, comunicará à UIF, na forma do art. 151, II, registro de documento ou título em que conste declaração das partes de que foi realizado pagamento em espécie, ou por título ao portador, de valor igual ou superior a R$ 100.000,00 (cem mil reais) ou ao equivalente em outra moeda.",
            "O registro de imóveis declara pagamento em espécie igual ou superior a R$ 100 mil?",
            "Ex: Escritura declarando pagamento de R$ 200 mil em dinheiro",
            setor=SETOR_IMOVEIS),

        # ── Art. 162 — Atenção Especial (Imóveis) ──
        _item("cod_1380", "1380", "Art. 162, I",
            "Art. 162, I - doações de bens imóveis ou direitos reais sobre bens imóveis para terceiros sem vínculo familiar aparente com o doador, referente a bem imóvel que tenha valor venal atribuído pelo município igual ou superior a R$ 100.000,00 (cem mil reais);",
            "Doação de imóvel de valor igual ou superior a R$ 100 mil para terceiro sem vínculo familiar?",
            "Ex: Doação de casa avaliada em R$ 300 mil para \"amigo\" sem parentesco",
            setor=SETOR_IMOVEIS),
        _item("cod_1381", "1381", "Art. 162, II",
            "Art. 162, II - concessão de empréstimos hipotecários ou com alienação fiduciária entre particulares;",
            "Há empréstimo com garantia hipotecária ou alienação fiduciária entre particulares?",
            "Ex: Mútuo com garantia de imóvel sem participação de instituição financeira",
            setor=SETOR_IMOVEIS),
        _item("cod_1382", "1382", "Art. 162, III",
            "Art. 162, III - registro de negócios celebrados por sociedades que tenham sido dissolvidas e tenham regressado à atividade;",
            "Empresa dissolvida que voltou à atividade está registrando negócios?",
            "Ex: Sociedade inativa há 10 anos que reaparece comprando imóveis",
            setor=SETOR_IMOVEIS),
        _item("cod_1383", "1383", "Art. 162, IV",
            "Art. 162, IV - registro de aquisição de imóveis por fundações e associações, quando as características do negócio não se coadunem com suas finalidades;",
            "Fundação ou associação está adquirindo imóvel incompatível com sua finalidade?",
            "Ex: Associação cultural sem fins lucrativos comprando fazenda produtiva",
            setor=SETOR_IMOVEIS),
        _item("cod_1384", "1384", "Art. 162, V",
            "Art. 162, V - registro de transmissões sucessivas do mesmo bem em período e com diferença de valor anormais;",
            "O mesmo imóvel foi transmitido várias vezes em curto período com valores anormais?",
            "Ex: Mesmo apartamento vendido 3 vezes no mesmo ano com valor crescente",
            setor=SETOR_IMOVEIS),
        _item("cod_1385", "1385", "Art. 162, VI",
            "Art. 162, VI - registro de título no qual conste valor declarado de bem com diferença anormal em relação a outros valores a ele associados, como o de sua avaliação fiscal ou o valor patrimonial pelo qual tenha sido considerado para fins sucessórios ou de integralização de capital de sociedade, por exemplo.",
            "Diferença anormal entre o valor declarado do imóvel e o valor fiscal ou patrimonial?",
            "Ex: Declarado R$ 50 mil, mas valor venal é R$ 500 mil",
            setor=SETOR_IMOVEIS),

        # ── Art. 163 — Comunicação Objetiva (RCPJ) ──
        _item("cod_1386", "1386", "Art. 163",
            "Art. 163. O oficial de registro de títulos e documentos e de registro civil das pessoas jurídicas, ou seu oficial de cumprimento, comunicará à UIF, na forma do art. 151, II, qualquer operação que envolva pagamento ou recebimento em espécie, ou por título ao portador, de valor igual ou superior a R$ 100.000,00 (cem mil reais) ou ao equivalente em outra moeda, inclusive quando se relacionar à compra ou venda de bens móveis ou imóveis.",
            "O pagamento ou recebimento em espécie é igual ou superior a R$ 100 mil? (RCPJ)",
            "Ex: Integralização de capital em espécie no valor de R$ 200 mil",
            setor=SETOR_RCPJ),

        # ── Art. 164 — Atenção Especial (RCPJ) ──
        _item("cod_1387", "1387", "Art. 164, I",
            "Art. 164, I - transferências de bens imóveis de qualquer valor, de cotas ou participações societárias ou de bens móveis de valor superior a R$ 100.000,00 (cem mil reais);",
            "Transferência de cotas, participações ou bens móveis de valor superior a R$ 100 mil?",
            "Ex: Cessão de cotas de sociedade no valor de R$ 500 mil",
            setor=SETOR_RCPJ),
        _item("cod_1388", "1388", "Art. 164, II",
            "Art. 164, II - mútuos concedidos ou contraídos ou doações concedidas ou recebidas de valor superior ao equivalente a R$ 100.000,00 (cem mil reais);",
            "Mútuo ou doação de valor superior a R$ 100 mil?",
            "Ex: Empresa \"emprestando\" R$ 300 mil para sócio sem contrato formal",
            setor=SETOR_RCPJ),
        _item("cod_1389", "1389", "Art. 164, III",
            "Art. 164, III - participações, investimentos ou representações de pessoas naturais ou jurídicas brasileiras em entidades estrangeiras, especialmente trusts, arranjos semelhantes ou fundações;",
            "Há participação brasileira em entidade estrangeira (trust, fundação offshore)?",
            "Ex: Sócio oculto em trust nas Ilhas Virgens Britânicas",
            setor=SETOR_RCPJ),
        _item("cod_1390", "1390", "Art. 164, IV",
            "Art. 164, IV - cessão de direito de títulos de créditos ou de títulos públicos de valor igual ou superior a R$ 500.000,00 (quinhentos mil reais).",
            "Cessão de direito de títulos de crédito ou públicos de valor igual ou superior a R$ 500 mil?",
            "Ex: Cessão de título de crédito sem lastro aparente",
            setor=SETOR_RCPJ),

        # ── Art. 171 — Comunicação Objetiva (Notas) ──
        _item("cod_1391", "1391", "Art. 171",
            "Art. 171. O tabelião de notas, ou seu oficial de cumprimento, comunicará à UIF, na forma do art. 151, II, qualquer operação que envolva pagamento ou recebimento em espécie, ou por título ao portador, de valor igual ou superior a R$ 100.000,00 (cem mil reais) ou ao equivalente em outra moeda, inclusive quando se relacionar à compra ou venda de bens móveis ou imóveis.",
            "O pagamento ou recebimento em espécie é igual ou superior a R$ 100 mil? (Notas)",
            "Ex: Pagamento em dinheiro de R$ 200 mil em escritura de compra e venda",
            setor=SETOR_NOTAS),

        # ── Art. 172 c/c Art. 162 — Atenção Especial (Notas) ──
        _item("cod_1392", "1392", "Art. 172, I",
            "Art. 172 c/c art. 162, I: O tabelião de notas deve analisar com especial atenção, para fins de eventual comunicação à UIF, operações relacionadas a doações de bens imóveis para terceiros sem vínculo familiar, de valor venal igual ou superior a R$ 100.000,00.",
            "Escritura de doação de imóvel de valor ≥ R$ 100 mil para terceiro sem vínculo familiar?",
            "Ex: Escritura de doação de casa para \"amigo\" em outro estado",
            setor=SETOR_NOTAS),
        _item("cod_1393", "1393", "Art. 172, II",
            "Art. 172 c/c art. 162, II: O tabelião de notas deve analisar com especial atenção operações relacionadas a concessão de empréstimos hipotecários ou com alienação fiduciária entre particulares.",
            "Escritura de empréstimo com garantia hipotecária entre particulares?",
            "Ex: Escritura de confissão de dívida com alienação fiduciária de imóvel",
            setor=SETOR_NOTAS),
        _item("cod_1394", "1394", "Art. 172, III",
            "Art. 172 c/c art. 162, III: O tabelião de notas deve analisar com especial atenção operações relacionadas a negócios celebrados por sociedades dissolvidas que tenham regressado à atividade.",
            "Escritura envolvendo empresa dissolvida que voltou à atividade?",
            "Ex: Sociedade inativa há anos reaparecendo em escritura de compra e venda",
            setor=SETOR_NOTAS),
        _item("cod_1395", "1395", "Art. 172, IV",
            "Art. 172 c/c art. 162, IV: O tabelião de notas deve analisar com especial atenção operações relacionadas a aquisição de imóveis por fundações e associações quando as características do negócio não se coadunem com suas finalidades.",
            "Escritura de aquisição de imóvel por fundação/associação incompatível com sua finalidade?",
            "Ex: Associação cultural comprando fazenda produtiva em escritura",
            setor=SETOR_NOTAS),
        _item("cod_1396", "1396", "Art. 172, V",
            "Art. 172 c/c art. 162, V: O tabelião de notas deve analisar com especial atenção operações relacionadas a transmissões sucessivas do mesmo bem em período e com diferença de valor anormais.",
            "Escritura de transmissão de imóvel vendido várias vezes em curto período?",
            "Ex: Mesmo imóvel transmitido 3 vezes no mesmo ano com valores crescentes",
            setor=SETOR_NOTAS),
        _item("cod_1397", "1397", "Art. 172, VI",
            "Art. 172 c/c art. 162, VI: O tabelião de notas deve analisar com especial atenção operações relacionadas a títulos com diferença anormal entre valor declarado e valor fiscal.",
            "Escritura com diferença anormal entre valor declarado e valor fiscal do imóvel?",
            "Ex: Declarado R$ 60 mil em escritura, valor venal R$ 400 mil",
            setor=SETOR_NOTAS),
    ]
    if categoria:
        setores_permitidos = CATEGORIA_SETORES.get(categoria, [SETOR_GERAL])
        return [s for s in todas if s.setor in setores_permitidos]
    return todas

TIPO_ATO_CATEGORIAS = [
    "Escritura",
    "Procuração",
    "Protesto",
    "Pessoa Jurídica",
]

ESCRITURA_OPCOES = [
    "Compra e venda",
    "Doação",
    "Permuta",
    "Constituição de garantia",
    "Alienação fiduciária",
    "Integralização de capital",
    "Ata Notarial",
    "Outro",
]

FORMA_PAGAMENTO_OPCOES = [
    "Não especificado",
    "PIX",
    "TED",
    "Dinheiro",
    "Cheque",
    "Boleto bancário",
    "Mista",
    "Outro",
]

SERVENTIA_OPCOES = [
    "Cartório Coxipó do Ouro",
    "Cartório 2º Ofício de Várzea Grande",
]

ESTADOS = [
    "AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO",
    "MA", "MT", "MS", "MG", "PA", "PB", "PR", "PE", "PI",
    "RJ", "RN", "RS", "RO", "RR", "SC", "SP", "SE", "TO",
]
