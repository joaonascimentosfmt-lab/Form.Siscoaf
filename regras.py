from typing import Dict, List, Tuple

from config import ScoringConfig, LIMITE_ESPECIE, obter_situacoes, SituacaoItem

PONTOS = ScoringConfig()


def aplicar_regras(dados: Dict) -> Tuple[str, List[str], int]:
    """
    Aplica todas as regras de decisão e retorna:
    - resultado: "COMUNICAR" ou "NAO_COMUNICAR"
    - motivos: lista de strings com justificativas
    - pontuacao_total: inteiro com a soma dos pontos
    """
    motivos: List[str] = []
    pontuacao_total = 0

    # Soma pontos das situações suspeitas marcadas
    for situacao in obter_situacoes():
        if dados.get(f"suspeita_{situacao.chave}", False):
            pontuacao_total += situacao.pontuacao

    if dados.get("pep", False):
        pontuacao_total += PONTOS.pep

    comunicar, motivo, pontos = _regra_indicios_lavagem(dados)
    if comunicar:
        motivos.append(motivo)
    pontuacao_total += pontos

    comunicar, motivo, pontos = _regra_especie_acima_limite(dados)
    if comunicar:
        motivos.append(motivo)
    pontuacao_total += pontos

    comunicar, motivo, pontos = _regra_pep_inconsistencia(dados)
    if comunicar:
        motivos.append(motivo)
    pontuacao_total += pontos

    comunicar, motivo, pontos = _regra_tres_ou_mais_situacoes(dados)
    if comunicar:
        motivos.append(motivo)

    comunicar, motivo, pontos = _regra_origem_nao_comprovada(dados)
    if comunicar:
        motivos.append(motivo)
    pontuacao_total += pontos

    comunicar, motivo, pontos = _regra_operacoes_fracionadas(dados)
    if comunicar:
        motivos.append(motivo)
    pontuacao_total += pontos

    comunicar, motivo, pontos = _regra_operacoes_relacionadas(dados)
    if comunicar:
        motivos.append(motivo)
    pontuacao_total += pontos

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


def _regra_indicios_lavagem(dados: Dict) -> Tuple[bool, str, int]:
    """
    Regra 1: Se houver indícios de lavagem de dinheiro -> COMUNICAR
    Pontuação já contabilizada via situacao.indicios_lavagem
    """
    if dados.get("suspeita_indicios_lavagem", False):
        return True, "Indícios de lavagem de dinheiro identificados", 0
    return False, "", 0


def _regra_especie_acima_limite(dados: Dict) -> Tuple[bool, str, int]:
    """
    Regra 2: Pagamento em espécie acima do limite interno -> COMUNICAR
    """
    especie = dados.get("pagamento_especie", False)
    valor_especie = dados.get("valor_especie", 0.0) or 0.0
    if especie and valor_especie > LIMITE_ESPECIE:
        pontos = PONTOS.especie
        return True, f"Pagamento em espécie de R$ {valor_especie:,.2f} acima do limite de R$ {LIMITE_ESPECIE:,.2f}", pontos
    return False, "", 0


def _regra_pep_inconsistencia(dados: Dict) -> Tuple[bool, str, int]:
    """
    Regra 3: PEP + inconsistência documental -> COMUNICAR
    Pontuação já contabilizada via situacoes (documentacao_inconsistente, resistencia_documentos)
    """
    pep = dados.get("pep", False)
    doc_inconsistente = dados.get("suspeita_documentacao_inconsistente", False)
    resistencia = dados.get("suspeita_resistencia_documentos", False)
    if pep and (doc_inconsistente or resistencia):
        return True, "PEP identificado com inconsistência documental", 0
    return False, "", 0


def _regra_tres_ou_mais_situacoes(dados: Dict) -> Tuple[bool, str, int]:
    """
    Regra 4: Três ou mais situações suspeitas marcadas -> COMUNICAR
    """
    situacoes = obter_situacoes()
    marcadas = sum(1 for s in situacoes if dados.get(f"suspeita_{s.chave}", False))
    if marcadas >= 3:
        return True, f"{marcadas} situações suspeitas identificadas (mínimo: 3)", 0
    return False, "", 0


def _regra_origem_nao_comprovada(dados: Dict) -> Tuple[bool, str, int]:
    """
    Regra 5: Origem dos recursos não comprovada -> COMUNICAR
    """
    if not dados.get("origem_identificada", False) or not dados.get("doc_comprobatoria", False):
        return True, "Origem dos recursos não comprovada", PONTOS.sem_origem
    return False, "", 0


def _regra_operacoes_fracionadas(dados: Dict) -> Tuple[bool, str, int]:
    """
    Regra 6: Operações fracionadas -> COMUNICAR
    """
    if dados.get("pagamento_fracionado", False):
        return True, "Pagamento fracionado identificado", PONTOS.fracionamento
    return False, "", 0


def _regra_operacoes_relacionadas(dados: Dict) -> Tuple[bool, str, int]:
    """
    Regra 7: Operações relacionadas -> COMUNICAR
    """
    if dados.get("operacoes_relacionadas", False):
        return True, "Operações relacionadas identificadas", PONTOS.operacoes_relacionadas
    return False, "", 0


def _regra_docs_partes(dados: Dict) -> Tuple[bool, str, int]:
    """
    Regra 8: Documentação das partes incompleta -> COMUNICAR
    Se todas as partes têm toda a documentação, é fator para não comunicação.
    Verifica por tipo (PF/PJ) de cada parte.
    """
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
