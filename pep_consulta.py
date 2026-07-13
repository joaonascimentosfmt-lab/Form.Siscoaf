import csv
import os
import re
from typing import Dict, List, Optional, Tuple

CSV_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "pep_db", "202605_PEP.csv")

_pep_cache: Optional[List[Dict]] = None


def _nome_coluna(keys: List[str], *alternativas: str) -> str:
    for alt in alternativas:
        for k in keys:
            if k.strip().lower() == alt.lower():
                return k
    return keys[0] if keys else ""


def _carregar_pep() -> List[Dict]:
    global _pep_cache
    if _pep_cache is not None:
        return _pep_cache

    if not os.path.exists(CSV_PATH):
        _pep_cache = []
        return _pep_cache

    registros = []
    with open(CSV_PATH, encoding="latin-1") as f:
        reader = csv.DictReader(f, delimiter=";")
        keys = reader.fieldnames or []
        col_cpf = _nome_coluna(keys, "CPF")
        col_nome = _nome_coluna(keys, "Nome_PEP")
        col_funcao = _nome_coluna(keys, "Descricao_Funcao", "Descrição_Função", "Descri��o_Fun��o")
        col_orgao = _nome_coluna(keys, "Nome_Orgao", "Nome_Órgão", "Nome_�rg�o")

        for row in reader:
            cpf_raw = row.get(col_cpf, "").strip()
            nome = row.get(col_nome, "").strip()
            funcao = row.get(col_funcao, "").strip()
            orgao = row.get(col_orgao, "").strip()
            cpf_digits = _extrair_digitos_visiveis(cpf_raw)
            registros.append({
                "cpf_raw": cpf_raw,
                "cpf_digitos": cpf_digits,
                "nome": nome.upper(),
                "funcao": funcao,
                "orgao": orgao,
            })
    _pep_cache = registros
    return registros


def _extrair_digitos_visiveis(cpf_raw: str) -> str:
    partes = cpf_raw.split(".")
    if len(partes) >= 3:
        dig1 = re.sub(r"\D", "", partes[1])
        dig2 = re.sub(r"\D", "", partes[2].split("-")[0])
        return dig1 + dig2
    return ""


def _normalizar_cpf(cpf: str) -> str:
    return re.sub(r"\D", "", cpf)


def consultar_por_cpf(cpf: str) -> List[Dict]:
    registros = _carregar_pep()
    if not registros:
        return []
    cpf_limpo = _normalizar_cpf(cpf)
    if len(cpf_limpo) < 6:
        return []
    if len(cpf_limpo) >= 9:
        digitos_informados = cpf_limpo[3:9]
    else:
        digitos_informados = cpf_limpo
    return [r for r in registros if r["cpf_digitos"] == digitos_informados]


def consultar_por_nome(nome: str) -> List[Dict]:
    registros = _carregar_pep()
    if not registros or not nome.strip():
        return []
    termo = nome.strip().upper()
    return [r for r in registros if termo in r["nome"]]


def consultar_pep(nome: str = "", cpf: str = "") -> Tuple[bool, List[Dict]]:
    if cpf:
        resultados = consultar_por_cpf(cpf)
        if resultados:
            return True, resultados
    if nome:
        resultados = consultar_por_nome(nome)
        if resultados:
            return True, resultados
    return False, []


def obter_resumo_pep(resultados: List[Dict]) -> str:
    if not resultados:
        return ""
    cargos = set()
    orgaos = set()
    for r in resultados:
        if r.get("funcao"):
            cargos.add(r["funcao"])
        if r.get("orgao"):
            orgaos.add(r["orgao"])
    partes = []
    if cargos:
        partes.append("Cargo(s): " + ", ".join(sorted(cargos)[:3]))
    if orgaos:
        partes.append("Órgão(s): " + ", ".join(sorted(orgaos)[:3]))
    return " | ".join(partes)


def total_registros() -> int:
    return len(_carregar_pep())
