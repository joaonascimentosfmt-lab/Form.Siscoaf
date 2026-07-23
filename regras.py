from typing import Dict, List, Tuple

from config import ScoringConfig, LIMITE_ESPECIE, obter_situacoes, SituacaoItem

PONTOS = ScoringConfig()


def aplicar_regras(dados: Dict) -> Tuple[str, List[str], int]:
    motivos: List[str] = []
    pontuacao_total = 0

    for situacao in obter_situacoes():
        if dados.get(f"suspeita_{situacao.chave}") == "Sim":
            pontuacao_total += situacao.pontuacao

    if dados.get("pep", False):
        pontuacao_total += PONTOS.pep

    comunicar, motivo, pontos = _regra_especie_acima_limite(dados)
    if comunicar:
        motivos.append(motivo)
    pontuacao_total += pontos

    comunicar, motivo, pontos = _regra_tres_ou_mais_situacoes(dados)
    if comunicar:
        motivos.append(motivo)

    comunicar, motivo, pontos = _regra_docs_partes(dados)
    if comunicar:
        motivos.append(motivo)
    pontuacao_total += pontos

    if pontuacao_total >= PONTOS.limite_comunicacao:
        motivo = f"Pontuação total ({pontuacao_total}) atingiu o limite mínimo ({PONTOS.limite_comunicacao})"
        if motivo not in motivos:
            motivos.append(motivo)

    if motivos:
        resultado = "COMUNICAR"
    else:
        resultado = "NAO_COMUNICAR"

    return resultado, motivos, pontuacao_total


def _regra_especie_acima_limite(dados: Dict) -> Tuple[bool, str, int]:
    especie = dados.get("pagamento_especie", False)
    valor_especie = dados.get("valor_especie", 0.0) or 0.0
    if especie and valor_especie > LIMITE_ESPECIE:
        pontos = PONTOS.especie
        return True, f"Pagamento em espécie de R$ {valor_especie:,.2f} acima do limite de R$ {LIMITE_ESPECIE:,.2f}", pontos
    return False, "", 0


def _regra_tres_ou_mais_situacoes(dados: Dict) -> Tuple[bool, str, int]:
    situacoes = obter_situacoes()
    marcadas = sum(1 for s in situacoes if dados.get(f"suspeita_{s.chave}") == "Sim")
    if marcadas >= 3:
        return True, f"{marcadas} situações suspeitas identificadas (mínimo: 3)", 0
    return False, "", 0


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
