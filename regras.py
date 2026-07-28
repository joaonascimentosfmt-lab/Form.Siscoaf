from typing import Dict, List, Tuple

from config import (
    ScoringConfig, obter_situacoes, SituacaoItem, CATEGORIA_SETORES,
    DECISAO_COMUNICAR, DECISAO_ATENCAO, DECISAO_SUSPEITA,
)

PONTOS = ScoringConfig()


def aplicar_regras(dados: Dict) -> Tuple[str, List[str], int]:
    motivos: List[str] = []
    pontuacao_total = 0

    categoria = dados.get("tipo_ato_categoria", "")
    situacoes = obter_situacoes(categoria) if categoria in CATEGORIA_SETORES else obter_situacoes()

    tem_comunicar_objetiva = False
    tem_atencao_especial = False
    pts_suspeita = 0
    marcadas_suspeita = 0

    for situacao in situacoes:
        if dados.get(f"suspeita_{situacao.chave}") != "Sim":
            continue
        if situacao.tipo == DECISAO_COMUNICAR:
            tem_comunicar_objetiva = True
            pergunta = situacao.pergunta or situacao.texto
            motivos.append(f"{situacao.codigo} — {pergunta}")
        elif situacao.tipo == DECISAO_ATENCAO:
            tem_atencao_especial = True
            pergunta = situacao.pergunta or situacao.texto
            motivos.append(f"{situacao.codigo} — {pergunta}")
        else:
            pts_suspeita += situacao.pontuacao
            marcadas_suspeita += 1
        pontuacao_total += situacao.pontuacao

    if tem_comunicar_objetiva:
        return "COMUNICAR", motivos, pontuacao_total

    if marcadas_suspeita > 0:
        motivos.append(f"{marcadas_suspeita} indicio(s) de suspeita assinalado(s)")

    if dados.get("pep", False):
        pontuacao_total += PONTOS.pep

    if tem_atencao_especial:
        return "ANALISAR", motivos, pontuacao_total

    if pts_suspeita >= 4 or marcadas_suspeita >= 2:
        return "COMUNICAR", motivos, pontuacao_total

    if motivos:
        return "COMUNICAR", motivos, pontuacao_total

    return "NAO_COMUNICAR", [], pontuacao_total


def _regra_docs_partes(dados: Dict) -> Tuple[bool, str, int]:
    partes = dados.get("partes", [])
    if not partes:
        return False, "", 0
    chaves_map = {
        "PF": ["doc_oficial", "cpf_regular", "estado_civil", "regime_bens", "endereco", "profissao", "contato"],
        "PJ": ["pj_cnpj", "pj_contrato_social", "pj_alteracoes", "pj_representante", "pj_poderes", "pj_objeto_social"],
    }
    todas_completas = all(
        all(p.get("docs", {}).get(chave, False) for chave in chaves_map.get(p.get("tipo", "PF"), chaves_map["PF"]))
        for p in partes
    )
    if todas_completas:
        return False, "", 0
    return True, "Documentação de parte(s) do ato incompleta", PONTOS.docs_incompletas
