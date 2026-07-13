import os
from datetime import datetime
from typing import Dict, List

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer

from config import obter_situacoes
from utils import formatar_moeda


def gerar_relatorio(
    dados: Dict,
    resultado: str,
    motivos: List[str],
    pontuacao: int,
    usuario: str = "Colaborador",
    caminho: str = "",
) -> str:
    if not caminho:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        caminho = os.path.join(os.getcwd(), f"relatorio_siscoaf_{timestamp}.pdf")

    styles = getSampleStyleSheet()
    estilo_titulo = ParagraphStyle(
        "TituloRelatorio",
        parent=styles["Title"],
        fontSize=16,
        spaceAfter=20,
        alignment=1,
    )
    estilo_subtitulo = ParagraphStyle(
        "Subtitulo",
        parent=styles["Heading2"],
        fontSize=12,
        spaceAfter=10,
        spaceBefore=15,
    )
    estilo_normal = ParagraphStyle(
        "NormalRelatorio",
        parent=styles["Normal"],
        fontSize=10,
        spaceAfter=4,
    )
    estilo_resultado = ParagraphStyle(
        "Resultado",
        parent=styles["Normal"],
        fontSize=14,
        spaceAfter=10,
        alignment=1,
        textColor=_cor_resultado(resultado),
    )

    elementos = []

    elementos.append(Paragraph("Análise de Comunicação ao SISCOAF", estilo_titulo))
    elementos.append(Paragraph(f"Resultado: {'COMUNICAR AO SISCOAF' if resultado == 'COMUNICAR' else 'NÃO COMUNICAR AO SISCOAF'}", estilo_resultado))
    elementos.append(Paragraph(f"Pontuação total: {pontuacao}", estilo_normal))
    elementos.append(Spacer(1, 10 * mm))

    elementos.append(Paragraph("Dados do Ato", estilo_subtitulo))
    _adicionar_campo(elementos, "Tipo do ato", dados.get("tipo_ato", ""), estilo_normal)
    _adicionar_campo(elementos, "Valor da operação", formatar_moeda(dados.get("valor", 0.0)), estilo_normal)
    _adicionar_campo(elementos, "Forma de pagamento", dados.get("forma_pagamento", ""), estilo_normal)
    _adicionar_campo(elementos, "Cidade", dados.get("cidade", ""), estilo_normal)
    _adicionar_campo(elementos, "Estado", dados.get("estado", ""), estilo_normal)
    _adicionar_campo(elementos, "Data", dados.get("data", ""), estilo_normal)

    if dados.get("tipo_ato") == "Procuração":
        elementos.append(Paragraph("Poderes da Procuração", estilo_subtitulo))
        poderes = dados.get("poderes", [])
        _adicionar_campo(elementos, "Poderes", ", ".join(poderes) if poderes else "Nenhum selecionado", estilo_normal)
        if dados.get("poderes_outros"):
            _adicionar_campo(elementos, "Outros poderes", dados["poderes_outros"], estilo_normal)

    elementos.append(Paragraph("Participantes", estilo_subtitulo))
    _adicionar_campo(elementos, "Quantidade de compradores", str(dados.get("qtd_compradores", 0)), estilo_normal)
    _adicionar_campo(elementos, "Quantidade de vendedores", str(dados.get("qtd_vendedores", 0)), estilo_normal)

    partes = dados.get("partes", [])
    if partes:
        elementos.append(Paragraph("Partes do ato:", estilo_normal))
        for i, p in enumerate(partes):
            nome = p.get("nome", "")
            cpf = p.get("cpf", "")
            papel = p.get("papel", "")
            pep_info = "✔ PEP" if p.get("pep") else ""
            texto = f"{i+1}. {papel}: {nome} (CPF: {cpf}) {pep_info}"
            elementos.append(Paragraph(texto, estilo_normal))
            if p.get("pep_detalhe"):
                elementos.append(Paragraph(f"   PEP: {p['pep_detalhe']}", estilo_normal))

    pep_texto = "Sim" if dados.get("pep", False) else "Não"
    _adicionar_campo(elementos, "Pessoa Exposta Politicamente (PEP)", pep_texto, estilo_normal)
    if dados.get("pep", False):
        _adicionar_campo(elementos, "Nome PEP", dados.get("pep_nome", ""), estilo_normal)
        _adicionar_campo(elementos, "Cargo PEP", dados.get("pep_cargo", ""), estilo_normal)
        _adicionar_campo(elementos, "Cidade PEP", dados.get("pep_cidade", ""), estilo_normal)

    elementos.append(Paragraph("Origem dos Recursos", estilo_subtitulo))
    _adicionar_campo(elementos, "Origem identificada", "Sim" if dados.get("origem_identificada", False) else "Não", estilo_normal)
    _adicionar_campo(elementos, "Documentação comprobatória", "Sim" if dados.get("doc_comprobatoria", False) else "Não", estilo_normal)

    elementos.append(Paragraph("Forma de Pagamento", estilo_subtitulo))
    _adicionar_campo(elementos, "Pagamento em espécie", "Sim" if dados.get("pagamento_especie", False) else "Não", estilo_normal)
    if dados.get("pagamento_especie", False):
        _adicionar_campo(elementos, "Valor em espécie", formatar_moeda(dados.get("valor_especie", 0.0)), estilo_normal)
    _adicionar_campo(elementos, "Pagamento fracionado", "Sim" if dados.get("pagamento_fracionado", False) else "Não", estilo_normal)
    _adicionar_campo(elementos, "Operações relacionadas", "Sim" if dados.get("operacoes_relacionadas", False) else "Não", estilo_normal)

    elementos.append(Paragraph("Situações Suspeitas", estilo_subtitulo))
    for situacao in obter_situacoes():
        marcado = dados.get(f"suspeita_{situacao.chave}", False)
        texto = f"{'✔' if marcado else '☐'} {situacao.texto}"
        elementos.append(Paragraph(texto, estilo_normal))

    observacoes = dados.get("observacoes", "")
    if observacoes:
        elementos.append(Paragraph("Observações", estilo_subtitulo))
        elementos.append(Paragraph(observacoes, estilo_normal))

    elementos.append(Spacer(1, 10 * mm))
    elementos.append(Paragraph("Justificativa da Decisão", estilo_subtitulo))
    if motivos:
        for motivo in motivos:
            elementos.append(Paragraph(f"• {motivo}", estilo_normal))
    else:
        elementos.append(Paragraph("Nenhum critério objetivo para comunicação foi identificado conforme as regras configuradas.", estilo_normal))

    elementos.append(Spacer(1, 15 * mm))
    elementos.append(Paragraph(f"Relatório gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}", estilo_normal))
    elementos.append(Paragraph(f"Usuário: {usuario}", estilo_normal))

    doc = SimpleDocTemplate(
        caminho,
        pagesize=A4,
        leftMargin=20 * mm,
        rightMargin=20 * mm,
        topMargin=20 * mm,
        bottomMargin=20 * mm,
    )
    doc.build(elementos)

    return caminho


def _adicionar_campo(elementos, rotulo: str, valor: str, estilo):
    elementos.append(Paragraph(f"<b>{rotulo}:</b> {valor}", estilo))


def _cor_resultado(resultado: str):
    from reportlab.lib.colors import HexColor
    if resultado == "COMUNICAR":
        return HexColor("#CC0000")
    return HexColor("#006600")
