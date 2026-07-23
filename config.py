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
    codigo: str
    artigo: str
    texto: str
    pontuacao: int

def obter_situacoes() -> List[SituacaoItem]:
    return [
        SituacaoItem(chave="cod_1356", codigo="1356", artigo="Art. 155-A, I", texto="Art. 155-A, I - aparentem não decorrer de atividades ou negócios usuais do cliente, de outros envolvidos ou do seu ramo de atuação;", pontuacao=2),
        SituacaoItem(chave="cod_1357", codigo="1357", artigo="Art. 155-A, II", texto="Art. 155-A, II - tenham origem ou fundamentação econômica ou legal não claramente aferíveis;", pontuacao=2),
        SituacaoItem(chave="cod_1358", codigo="1358", artigo="Art. 155-A, III", texto="Art. 155-A, III - se mostrem incompatíveis com o patrimônio ou com a capacidade econômico-financeira do cliente ou de outros envolvidos;", pontuacao=2),
        SituacaoItem(chave="cod_1359", codigo="1359", artigo="Art. 155-A, IV", texto="Art. 155-A, IV - envolvam difícil ou inviável identificação de beneficiário(s) final(is);", pontuacao=2),
        SituacaoItem(chave="cod_1360", codigo="1360", artigo="Art. 155-A, V", texto="Art. 155-A, V - se relacionem a pessoa jurídica domiciliada em jurisdição listada pelo Grupo de Ação Financeira (Gafi) como de alto risco ou com deficiências estratégicas em matéria de PLD/FTP;", pontuacao=2),
        SituacaoItem(chave="cod_1361", codigo="1361", artigo="Art. 155-A, VI", texto="Art. 155-A, VI - envolvam países ou dependências listados pela RFB como de tributação favorecida e/ou regime fiscal privilegiado;", pontuacao=2),
        SituacaoItem(chave="cod_1362", codigo="1362", artigo="Art. 155-A, VII", texto="Art. 155-A, VII - se relacionem a pessoa jurídica cujos sócios, administradores, beneficiários finais, procuradores ou representantes legais mantenham domicílio em jurisdições consideradas pelo Gafi de alto risco ou com deficiências estratégicas em matéria de PLD/FTP;", pontuacao=2),
        SituacaoItem(chave="cod_1363", codigo="1363", artigo="Art. 155-A, VIII", texto="Art. 155-A, VIII - apresentem, por parte de cliente ou demais envolvidos, resistência ao fornecimento de informação ou documentação solicitada para fins relacionados ao disposto neste Capítulo;", pontuacao=2),
        SituacaoItem(chave="cod_1364", codigo="1364", artigo="Art. 155-A, IX", texto="Art. 155-A, IX - envolvam a prestação, por parte de cliente ou demais envolvidos, de informação ou documentação falsa ou de difícil ou onerosa verificação;", pontuacao=2),
        SituacaoItem(chave="cod_1365", codigo="1365", artigo="Art. 155-A, X", texto="Art. 155-A, X - se mostrem injustificadamente mais complexas ou onerosas que de ordinário, mormente se isso puder dificultar o rastreamento de recursos ou a identificação de real propósito;", pontuacao=2),
        SituacaoItem(chave="cod_1366", codigo="1366", artigo="Art. 155-A, XI", texto="Art. 155-A, XI - apresentem sinais de caráter fictício ou de relação com valores incompatíveis com os de mercado;", pontuacao=2),
        SituacaoItem(chave="cod_1367", codigo="1367", artigo="Art. 155-A, XII", texto="Art. 155-A, XII - envolvam cláusulas que estabeleçam condições incompatíveis com as praticadas no mercado;", pontuacao=2),
        SituacaoItem(chave="cod_1368", codigo="1368", artigo="Art. 155-A, XIII", texto="Art. 155-A, XIII - aparentem tentativa de burlar controles e registros exigidos pela legislação de PLD/FTP, inclusive mediante fracionamento ou pagamento em espécie, com título emitido ao portador ou por outros meios que dificultem a rastreabilidade;", pontuacao=2),
        SituacaoItem(chave="cod_1369", codigo="1369", artigo="Art. 155-A, XIV", texto="Art. 155-A, XIV - envolvam o registro de documento de procedência estrangeira, nos termos do art. 129, 6º, combinado com o art. 148 da Lei n. 6.015, de 31 de dezembro de 1973, que ofereçam dificuldade significativa para a compreensão do seu sentido jurídico no contexto da atividade notarial ou registral de que se trate;", pontuacao=2),
        SituacaoItem(chave="cod_1370", codigo="1370", artigo="Art. 155-A, XV", texto="Art. 155-A, XV - revelem substancial ganho de capital em curto período;", pontuacao=2),
        SituacaoItem(chave="cod_1371", codigo="1371", artigo="Art. 155-A, XVI", texto="Art. 155-A, XVI - envolvam lavratura ou utilização de instrumento de procuração que outorgue amplos poderes de administração de pessoa jurídica ou de gestão empresarial, de gerência de negócios ou de movimentação de conta bancária, de pagamento ou de natureza semelhante, especialmente quando conferidos em caráter irrevogável ou irretratável ou isento de prestação de contas, independentemente de se tratar, ou não, de procuração em causa própria ou por prazo indeterminado;", pontuacao=2),
        SituacaoItem(chave="cod_1372", codigo="1372", artigo="Art. 155-A, XVII", texto="Art. 155-A, XVII - revelem operações de aumento de capital social que pareçam destoar dos efetivos atributos de valor, patrimônio ou outros aspectos relacionados às condições econômico-financeiras da sociedade, diante de circunstâncias como, por exemplo, partes envolvidas no ato ou características do empreendimento;", pontuacao=2),
        SituacaoItem(chave="cod_1373", codigo="1373", artigo="Art. 155-A, XVIII", texto="Art. 155-A, XVIII - quaisquer outras operações, propostas de operação ou situações que, considerando suas características, especialmente partes, demais envolvidos, valores, modo de realização, meios e formas de pagamento, falta de fundamento econômico ou legal ou, ainda, incompatibilidade com práticas de mercado, possam configurar sérios indícios de práticas de LD/FTP ou de infrações que com elas se relacionem.", pontuacao=2),
        SituacaoItem(chave="cod_1374", codigo="1374", artigo="Art. 155-A [...] Parágrafo único, I: Parágrafo único", texto="Art. 155-A [...] Parágrafo único, I: Parágrafo único - Na hipótese do caput deste artigo, o notário e o registrador também atentarão para operações, propostas de operação ou situações que: I - revelem emprego não usual de meio ou forma de pagamento que possa viabilizar anonimato ou dificultar a rastreabilidade de movimentação de valores ou a identificação de quem a tenha realizado, como o uso de valores anormalmente elevados em espécie ou na forma de título emitido ao portador ou, ainda, de ativo virtual não vinculado nominalmente a quem o movimente;", pontuacao=2),
        SituacaoItem(chave="cod_1375", codigo="1375", artigo="Art. 155-A [...] Parágrafo único, II: Parágrafo único", texto="Art. 155-A [...] Parágrafo único, II: Parágrafo único - Na hipótese do caput deste artigo, o notário e o registrador também atentarão para operações, propostas de operação ou situações que: II - apresentem algum sinal de possível relação, direta ou indireta, com práticas de terrorismo ou proliferação de armas de destruição em massa ou com seus financiamentos, inclusive em hipóteses correlatas eventualmente contempladas em atos normativos da UIF.", pontuacao=2),
        SituacaoItem(chave="cod_1376", codigo="1376", artigo="Art. 159", texto="Art. 159. O tabelião de protesto, ou seu oficial de cumprimento, comunicará à UIF, na forma do art. 151, II, qualquer operação que envolva pagamento ou recebimento em espécie, ou por título ao portador, de valor igual ou superior a R$ 100.000,00 (cem mil reais) ou ao equivalente em outra moeda, desde que perante o tabelião ou seu preposto.", pontuacao=2),
        SituacaoItem(chave="cod_1377", codigo="1377", artigo="Art. 160, I", texto="Art. 160, I - em valor igual ou superior a R$ 100.000,00 (cem mil reais), quando o devedor for pessoa física;", pontuacao=2),
        SituacaoItem(chave="cod_1378", codigo="1378", artigo="Art. 160, II", texto="Art. 160, II - em valor igual ou superior a R$ 500.000,00 (quinhentos mil reais), quando o devedor for pessoa jurídica, salvo quando se tratar de instituição do mercado financeiro, do mercado de capitais ou de órgãos e entes públicos.", pontuacao=2),
        SituacaoItem(chave="cod_1379", codigo="1379", artigo="Art. 161", texto="Art. 161. O oficial de registro de imóveis, ou seu oficial de cumprimento, comunicará à UIF, na forma do art. 151, II, registro de documento ou título em que conste declaração das partes de que foi realizado pagamento em espécie, ou por título ao portador, de valor igual ou superior a R$ 100.000,00 (cem mil reais) ou ao equivalente em outra moeda.", pontuacao=2),
        SituacaoItem(chave="cod_1380", codigo="1380", artigo="Art. 162, I", texto="Art. 162, I - doações de bens imóveis ou direitos reais sobre bens imóveis para terceiros sem vínculo familiar aparente com o doador, referente a bem imóvel que tenha valor venal atribuído pelo município igual ou superior a R$ 100.000,00 (cem mil reais);", pontuacao=2),
        SituacaoItem(chave="cod_1381", codigo="1381", artigo="Art. 162, II", texto="Art. 162, II - concessão de empréstimos hipotecários ou com alienação fiduciária entre particulares;", pontuacao=2),
        SituacaoItem(chave="cod_1382", codigo="1382", artigo="Art. 162, III", texto="Art. 162, III - registro de negócios celebrados por sociedades que tenham sido dissolvidas e tenham regressado à atividade;", pontuacao=2),
        SituacaoItem(chave="cod_1383", codigo="1383", artigo="Art. 162, IV", texto="Art. 162, IV - registro de aquisição de imóveis por fundações e associações, quando as características do negócio não se coadunem com suas finalidades;", pontuacao=2),
        SituacaoItem(chave="cod_1384", codigo="1384", artigo="Art. 162, V", texto="Art. 162, V - registro de transmissões sucessivas do mesmo bem em período e com diferença de valor anormais;", pontuacao=2),
        SituacaoItem(chave="cod_1385", codigo="1385", artigo="Art. 162, VI", texto="Art. 162, VI - registro de título no qual conste valor declarado de bem com diferença anormal em relação a outros valores a ele associados, como o de sua avaliação fiscal ou o valor patrimonial pelo qual tenha sido considerado para fins sucessórios ou de integralização de capital de sociedade, por exemplo.", pontuacao=2),
        SituacaoItem(chave="cod_1386", codigo="1386", artigo="Art. 163", texto="Art. 163. O oficial de registro de títulos e documentos e de registro civil das pessoas jurídicas, ou seu oficial de cumprimento, comunicará à UIF, na forma do art. 151, II, qualquer operação que envolva pagamento ou recebimento em espécie, ou por título ao portador, de valor igual ou superior a R$ 100.000,00 (cem mil reais) ou ao equivalente em outra moeda, inclusive quando se relacionar à compra ou venda de bens móveis ou imóveis.", pontuacao=2),
        SituacaoItem(chave="cod_1387", codigo="1387", artigo="Art. 164, I", texto="Art. 164, I - transferências de bens imóveis de qualquer valor, de cotas ou participações societárias ou de bens móveis de valor superior a R$ 100.000,00 (cem mil reais);", pontuacao=2),
        SituacaoItem(chave="cod_1388", codigo="1388", artigo="Art. 164, II", texto="Art. 164, II - mútuos concedidos ou contraídos ou doações concedidas ou recebidas de valor superior ao equivalente a R$ 100.000,00 (cem mil reais);", pontuacao=2),
        SituacaoItem(chave="cod_1389", codigo="1389", artigo="Art. 164, III", texto="Art. 164, III - participações, investimentos ou representações de pessoas naturais ou jurídicas brasileiras em entidades estrangeiras, especialmente trusts, arranjos semelhantes ou fundações;", pontuacao=2),
        SituacaoItem(chave="cod_1390", codigo="1390", artigo="Art. 164, IV", texto="Art. 164, IV - cessão de direito de títulos de créditos ou de títulos públicos de valor igual ou superior a R$ 500.000,00 (quinhentos mil reais).", pontuacao=2),
        SituacaoItem(chave="cod_1391", codigo="1391", artigo="Art. 171", texto="Art. 171. O tabelião de notas, ou seu oficial de cumprimento, comunicará à UIF, na forma do art. 151, II, qualquer operação que envolva pagamento ou recebimento em espécie, ou por título ao portador, de valor igual ou superior a R$ 100.000,00 (cem mil reais) ou ao equivalente em outra moeda, inclusive quando se relacionar à compra ou venda de bens móveis ou imóveis.", pontuacao=2),
        SituacaoItem(chave="cod_1392", codigo="1392", artigo="Art. 172 c/c art. 162, I", texto="Art. 172 c/c art. 162, I: Art. 172. O tabelião de notas, ou seu oficial de cumprimento, deve analisar com especial atenção, para fins de eventual comunicação à UIF na forma do art. 151, I, operações, propostas de operação ou situações relacionadas a quaisquer das hipóteses listadas no art. 162, quando envolverem escritura pública. Art. 162. [...] I - doações de bens imóveis ou direitos reais sobre bens imóveis para terceiros sem vínculo familiar aparente com o doador, referente a bem imóvel que tenha valor venal atribuído pelo município igual ou superior a R$ 100.000,00 (cem mil reais);", pontuacao=2),
        SituacaoItem(chave="cod_1393", codigo="1393", artigo="Art. 172 c/c art. 162, II", texto="Art. 172 c/c art. 162, II: Art. 172. O tabelião de notas, ou seu oficial de cumprimento, deve analisar com especial atenção, para fins de eventual comunicação à UIF na forma do art. 151, I, operações, propostas de operação ou situações relacionadas a quaisquer das hipóteses listadas no art. 162, quando envolverem escritura pública. Art. 162. [...] II - concessão de empréstimos hipotecários ou com alienação fiduciária entre particulares;", pontuacao=2),
        SituacaoItem(chave="cod_1394", codigo="1394", artigo="Art. 172 c/c art. 162, III", texto="Art. 172 c/c art. 162, III: Art. 172. O tabelião de notas, ou seu oficial de cumprimento, deve analisar com especial atenção, para fins de eventual comunicação à UIF na forma do art. 151, I, operações, propostas de operação ou situações relacionadas a quaisquer das hipóteses listadas no art. 162, quando envolverem escritura pública. Art. 162. [...] III - registro de negócios celebrados por sociedades que tenham sido dissolvidas e tenham regressado à atividade;", pontuacao=2),
        SituacaoItem(chave="cod_1395", codigo="1395", artigo="Art. 172 c/c art. 162, IV", texto="Art. 172 c/c art. 162, IV: Art. 172. O tabelião de notas, ou seu oficial de cumprimento, deve analisar com especial atenção, para fins de eventual comunicação à UIF na forma do art. 151, I, operações, propostas de operação ou situações relacionadas a quaisquer das hipóteses listadas no art. 162, quando envolverem escritura pública. Art. 162. [...] IV - registro de aquisição de imóveis por fundações e associações, quando as características do negócio não se coadunem com suas finalidades;", pontuacao=2),
        SituacaoItem(chave="cod_1396", codigo="1396", artigo="Art. 172 c/c art. 162, V", texto="Art. 172 c/c art. 162, V: Art. 172. O tabelião de notas, ou seu oficial de cumprimento, deve analisar com especial atenção, para fins de eventual comunicação à UIF na forma do art. 151, I, operações, propostas de operação ou situações relacionadas a quaisquer das hipóteses listadas no art. 162, quando envolverem escritura pública. Art. 162. [...] V - registro de transmissões sucessivas do mesmo bem em período e com diferença de valor anormais;", pontuacao=2),
        SituacaoItem(chave="cod_1397", codigo="1397", artigo="Art. 172 c/c art. 162, VI", texto="Art. 172 c/c art. 162, VI: Art. 172. O tabelião de notas, ou seu oficial de cumprimento, deve analisar com especial atenção, para fins de eventual comunicação à UIF na forma do art. 151, I, operações, propostas de operação ou situações relacionadas a quaisquer das hipóteses listadas no art. 162, quando envolverem escritura pública. Art. 162. [...] VI - registro de título no qual conste valor declarado de bem com diferença anormal em relação a outros valores a ele associados, como o de sua avaliação fiscal ou o valor patrimonial pelo qual tenha sido considerado para fins sucessórios ou de integralização de capital de sociedade, por exemplo.", pontuacao=2),
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
