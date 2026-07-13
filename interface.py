from typing import Dict, List, Optional

import os
import customtkinter as ctk

from config import (
    obter_situacoes,
    TIPO_ATO_OPCOES,
    FORMA_PAGAMENTO_OPCOES,
    ESTADOS,
)
from regras import aplicar_regras
from relatorio import gerar_relatorio
from utils import validar_valor
from database import salvar_analise, listar_analises, carregar_analise, buscar_analises
from pep_consulta import consultar_pep, obter_resumo_pep

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("green")

COR_CARD = "#F0F4F0"
COR_BG = "#FAFAFA"
COR_PRIMARIA = "#2E7D32"
COR_TEXTO = "#1B1B1B"
COR_SUBTEXTO = "#555555"


def _aplicar_icon(widget):
    try:
        icon_path = os.path.join(os.path.dirname(__file__), "assets", "icon.ico")
        if os.path.exists(icon_path):
            widget.iconbitmap(icon_path)
    except Exception:
        pass


class AnalisadorSISCOAF(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Analisador SISCOAF")
        self.geometry("780x950")
        self.minsize(600, 650)
        self.configure(fg_color=COR_BG)

        self._carregando = False
        self._construir_tela()
        _aplicar_icon(self)

    def _construir_tela(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # toolbar
        toolbar = ctk.CTkFrame(self, fg_color=COR_CARD, corner_radius=0, height=50)
        toolbar.grid(row=0, column=0, sticky="ew", padx=0, pady=(0, 5))
        toolbar.grid_columnconfigure(2, weight=1)
        toolbar.grid_propagate(False)

        ctk.CTkLabel(
            toolbar,
            text="Análise de Comunicação ao SISCOAF",
            font=("Segoe UI", 18, "bold"),
            text_color=COR_PRIMARIA,
        ).grid(row=0, column=0, sticky="w", padx=(16, 10), pady=10)

        ctk.CTkButton(
            toolbar,
            text="Histórico",
            font=("Segoe UI", 12),
            fg_color="#5C6BC0",
            hover_color="#3F51B5",
            height=32,
            corner_radius=8,
            command=self._abrir_historico,
        ).grid(row=0, column=1, padx=4, pady=10)

        ctk.CTkButton(
            toolbar,
            text="Limpar",
            font=("Segoe UI", 12),
            fg_color="#888888",
            hover_color="#666666",
            height=32,
            corner_radius=8,
            command=self._limpar_formulario,
        ).grid(row=0, column=2, padx=4, pady=10, sticky="w")

        # scroll principal
        scroll = ctk.CTkScrollableFrame(self, fg_color="transparent")
        scroll.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0, 5))
        scroll.grid_columnconfigure(0, weight=1)

        linha = 0
        linha = self._secao_dados_ato(scroll, linha)
        linha = self._secao_participantes(scroll, linha)
        linha = self._secao_partes(scroll, linha)
        linha = self._secao_origem_recursos(scroll, linha)
        linha = self._secao_pagamento(scroll, linha)
        linha = self._secao_situacoes_suspeitas(scroll, linha)
        linha = self._secao_observacoes(scroll, linha)

        self._btn_analisar = ctk.CTkButton(
            scroll,
            text="ANALISAR",
            font=("Segoe UI", 16, "bold"),
            fg_color=COR_PRIMARIA,
            hover_color="#1B5E20",
            height=50,
            corner_radius=10,
            command=self._analisar,
        )
        self._btn_analisar.grid(row=linha, column=0, pady=(10, 5), sticky="ew")
        linha += 1

        ctk.CTkLabel(
            scroll,
            text="",
            font=("Segoe UI", 8),
        ).grid(row=linha, column=0)

        # status bar
        self._status_bar = ctk.CTkLabel(
            self,
            text="Pronto",
            font=("Segoe UI", 10),
            text_color=COR_SUBTEXTO,
            anchor="w",
            fg_color=COR_CARD,
        )
        self._status_bar.grid(row=2, column=0, sticky="ew", padx=0, pady=(0, 0))
        self._status_bar.grid_propagate(False)
        self._status_bar.configure(height=24)

    def _set_status(self, msg: str):
        self._status_bar.configure(text=msg)

    def _card(self, parent, titulo: str, linha_inicio: int) -> int:
        card = ctk.CTkFrame(parent, fg_color=COR_CARD, corner_radius=12)
        card.grid(row=linha_inicio, column=0, sticky="ew", pady=(0, 12))
        card.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(
            card,
            text=titulo,
            font=("Segoe UI", 15, "bold"),
            text_color=COR_TEXTO,
        ).grid(row=0, column=0, columnspan=4, sticky="w", padx=16, pady=(12, 8))

        return card

    def _ao_tipo_ato(self, escolha: str):
        if escolha == "Procuração":
            self._poderes_frame.grid()
        else:
            self._poderes_frame.grid_remove()

    def _secao_dados_ato(self, parent, linha: int) -> int:
        card = self._card(parent, "Dados do ato", linha)
        r = 1

        ctk.CTkLabel(card, text="Tipo do ato:", font=("Segoe UI", 12), text_color=COR_TEXTO).grid(row=r, column=0, sticky="w", padx=16, pady=(0, 2))
        r += 1
        self._tipo_ato = ctk.CTkComboBox(card, values=TIPO_ATO_OPCOES, state="readonly", width=300, command=self._ao_tipo_ato)
        self._tipo_ato.set("Compra e venda")
        self._tipo_ato.grid(row=r, column=0, columnspan=2, sticky="w", padx=16, pady=(0, 6))
        r += 1

        # Poderes (visivel apenas se "Procuração")
        self._poderes_frame = ctk.CTkFrame(card, fg_color="#f5faf5", corner_radius=8)
        self._poderes_frame.grid(row=r, column=0, columnspan=3, sticky="ew", padx=16, pady=(0, 8))
        self._poderes_frame.grid_remove()
        ctk.CTkLabel(self._poderes_frame, text="Poderes solicitados na procuração:", font=("Segoe UI", 12, "bold"), text_color="#2E7D32").grid(row=0, column=0, columnspan=2, sticky="w", padx=8, pady=(6, 4))
        self._poderes_vars = {}
        self._PODERES_OPCOES = ["Amplos Poderes", "Gestão e Movimentação Bancária", "Compra, Venda e Administração de Imóveis", "Representação em Inventário e Partilha"]
        for i, p in enumerate(self._PODERES_OPCOES):
            var = ctk.StringVar(value="")
            cb = ctk.CTkCheckBox(self._poderes_frame, text=p, variable=var, onvalue=p, offvalue="", fg_color=COR_PRIMARIA, font=("Segoe UI", 11))
            cb.grid(row=i+1, column=0, sticky="w", padx=8, pady=1)
            self._poderes_vars[p] = var
        ctk.CTkLabel(self._poderes_frame, text="Outros poderes (descreva):", font=("Segoe UI", 11), text_color=COR_TEXTO).grid(row=len(self._PODERES_OPCOES)+1, column=0, sticky="w", padx=8, pady=(6, 0))
        self._poderes_outros = ctk.CTkTextbox(self._poderes_frame, height=40, width=400, corner_radius=6)
        self._poderes_outros.grid(row=len(self._PODERES_OPCOES)+2, column=0, sticky="ew", padx=8, pady=(2, 6))
        r += 1

        ctk.CTkLabel(card, text="Valor do negócio (R$):", font=("Segoe UI", 12), text_color=COR_TEXTO).grid(row=r, column=0, sticky="w", padx=16, pady=(0, 2))
        r += 1
        self._valor = ctk.CTkEntry(card, placeholder_text="0,00", width=200)
        self._valor.grid(row=r, column=0, sticky="w", padx=16, pady=(0, 6))
        r += 1

        ctk.CTkLabel(card, text="Forma de pagamento:", font=("Segoe UI", 12), text_color=COR_TEXTO).grid(row=r, column=0, sticky="w", padx=16, pady=(0, 2))
        r += 1
        self._forma_pagamento = ctk.CTkComboBox(card, values=FORMA_PAGAMENTO_OPCOES, state="readonly", width=200)
        self._forma_pagamento.set("TED")
        self._forma_pagamento.grid(row=r, column=0, sticky="w", padx=16, pady=(0, 6))
        r += 1

        frm_local = ctk.CTkFrame(card, fg_color="transparent")
        frm_local.grid(row=r, column=0, columnspan=3, sticky="ew", padx=16, pady=(0, 10))
        frm_local.grid_columnconfigure((0, 1, 2), weight=1)

        ctk.CTkLabel(frm_local, text="Cidade:", font=("Segoe UI", 12), text_color=COR_TEXTO).grid(row=0, column=0, sticky="w")
        ctk.CTkLabel(frm_local, text="Estado:", font=("Segoe UI", 12), text_color=COR_TEXTO).grid(row=0, column=1, sticky="w")
        ctk.CTkLabel(frm_local, text="Data:", font=("Segoe UI", 12), text_color=COR_TEXTO).grid(row=0, column=2, sticky="w")

        self._cidade = ctk.CTkEntry(frm_local, placeholder_text="Cidade", width=180)
        self._cidade.grid(row=1, column=0, sticky="w")
        self._estado = ctk.CTkComboBox(frm_local, values=ESTADOS, state="readonly", width=100)
        self._estado.set("SP")
        self._estado.grid(row=1, column=1, sticky="w", padx=(10, 0))
        self._data = ctk.CTkEntry(frm_local, placeholder_text="dd/mm/aaaa", width=130)
        self._data.grid(row=1, column=2, sticky="w", padx=(10, 0))
        r += 1

        return linha + 1

    def _secao_participantes(self, parent, linha: int) -> int:
        card = self._card(parent, "Participantes", linha)
        r = 1

        frm_qtd = ctk.CTkFrame(card, fg_color="transparent")
        frm_qtd.grid(row=r, column=0, columnspan=3, sticky="ew", padx=16, pady=(0, 8))
        frm_qtd.grid_columnconfigure((0, 1), weight=1)

        ctk.CTkLabel(frm_qtd, text="Qtd. compradores:", font=("Segoe UI", 12), text_color=COR_TEXTO).grid(row=0, column=0, sticky="w")
        self._qtd_compradores = ctk.CTkEntry(frm_qtd, placeholder_text="0", width=100)
        self._qtd_compradores.grid(row=1, column=0, sticky="w")
        ctk.CTkLabel(frm_qtd, text="Qtd. vendedores:", font=("Segoe UI", 12), text_color=COR_TEXTO).grid(row=0, column=1, sticky="w")
        self._qtd_vendedores = ctk.CTkEntry(frm_qtd, placeholder_text="0", width=100)
        self._qtd_vendedores.grid(row=1, column=1, sticky="w")
        r += 1

        ctk.CTkLabel(card, text="Pessoa Politicamente Exposta (PEP)?", font=("Segoe UI", 12), text_color=COR_TEXTO).grid(row=r, column=0, sticky="w", padx=16, pady=(0, 2))
        r += 1
        self._pep_var = ctk.StringVar(value="Não")
        frm_pep = ctk.CTkFrame(card, fg_color="transparent")
        frm_pep.grid(row=r, column=0, columnspan=3, sticky="w", padx=16, pady=(0, 6))
        ctk.CTkRadioButton(frm_pep, text="Sim", variable=self._pep_var, value="Sim", command=self._toggle_pep).pack(side="left", padx=(0, 20))
        ctk.CTkRadioButton(frm_pep, text="Não", variable=self._pep_var, value="Não", command=self._toggle_pep).pack(side="left")
        r += 1

        self._pep_frame = ctk.CTkFrame(card, fg_color="transparent")
        self._pep_frame.grid(row=r, column=0, columnspan=3, sticky="ew", padx=16, pady=(0, 8))
        ctk.CTkLabel(self._pep_frame, text="Nome:", font=("Segoe UI", 12), text_color=COR_TEXTO).grid(row=0, column=0, sticky="w")
        self._pep_nome = ctk.CTkEntry(self._pep_frame, placeholder_text="Nome do PEP", width=220)
        self._pep_nome.grid(row=1, column=0, sticky="w", padx=(0, 10))
        ctk.CTkLabel(self._pep_frame, text="Cargo:", font=("Segoe UI", 12), text_color=COR_TEXTO).grid(row=0, column=1, sticky="w")
        self._pep_cargo = ctk.CTkEntry(self._pep_frame, placeholder_text="Cargo", width=180)
        self._pep_cargo.grid(row=1, column=1, sticky="w", padx=(0, 10))
        ctk.CTkLabel(self._pep_frame, text="Cidade:", font=("Segoe UI", 12), text_color=COR_TEXTO).grid(row=0, column=2, sticky="w")
        self._pep_cidade = ctk.CTkEntry(self._pep_frame, placeholder_text="Cidade", width=150)
        self._pep_cidade.grid(row=1, column=2, sticky="w")
        self._pep_frame.grid_remove()
        r += 1

        return linha + 1

    def _toggle_pep(self):
        if self._pep_var.get() == "Sim":
            self._pep_frame.grid()
        else:
            self._pep_frame.grid_remove()

    def _secao_partes(self, parent, linha: int) -> int:
        card = self._card(parent, "Partes do ato", linha)
        r = 1

        ctk.CTkLabel(
            card,
            text="Adicione as partes envolvidas e consulte se são PEP:",
            font=("Segoe UI", 11),
            text_color=COR_SUBTEXTO,
        ).grid(row=r, column=0, columnspan=4, sticky="w", padx=16, pady=(0, 6))
        r += 1

        self._partes_frame = ctk.CTkFrame(card, fg_color="transparent")
        self._partes_frame.grid(row=r, column=0, columnspan=4, sticky="ew", padx=8, pady=(0, 6))
        self._partes_frame.grid_columnconfigure(2, weight=1)
        r += 1

        self._partes: List[Dict] = []
        self._btn_add_parte = ctk.CTkButton(
            card,
            text="+ Adicionar parte",
            font=("Segoe UI", 12),
            fg_color=COR_PRIMARIA,
            hover_color="#1B5E20",
            height=30,
            corner_radius=8,
            command=self._adicionar_parte,
        )
        self._btn_add_parte.grid(row=r, column=0, sticky="w", padx=16, pady=(0, 12))

        self._adicionar_parte()
        self._adicionar_parte()

        return linha + 1

    def _adicionar_parte(self, dados: Optional[Dict] = None):
        idx = len(self._partes)
        frm = ctk.CTkFrame(self._partes_frame, fg_color="#fff", corner_radius=8, border_width=1, border_color="#DDD")
        frm.grid(row=idx, column=0, sticky="ew", padx=8, pady=3)
        frm.grid_columnconfigure((0, 1), weight=1)
        frm.grid_columnconfigure(2, weight=0)

        entry_nome = ctk.CTkEntry(frm, placeholder_text="Nome completo", width=200)
        entry_nome.grid(row=0, column=0, sticky="ew", padx=(8, 4), pady=6)
        if dados:
            entry_nome.insert(0, dados.get("nome", ""))

        entry_cpf = ctk.CTkEntry(frm, placeholder_text="CPF", width=130)
        entry_cpf.grid(row=0, column=1, sticky="ew", padx=4, pady=6)
        if dados:
            entry_cpf.insert(0, dados.get("cpf", ""))

        papel_var = ctk.StringVar(value=dados.get("papel", "Outorgante") if dados else "Outorgante")
        frm_papel = ctk.CTkFrame(frm, fg_color="transparent")
        frm_papel.grid(row=0, column=2, sticky="ew", padx=4, pady=6)
        ctk.CTkRadioButton(frm_papel, text="Outorgante", variable=papel_var, value="Outorgante", font=("Segoe UI", 10)).pack(side="left", padx=(0, 4))
        ctk.CTkRadioButton(frm_papel, text="Outorgado", variable=papel_var, value="Outorgado", font=("Segoe UI", 10)).pack(side="left")

        lbl_pep = ctk.CTkLabel(frm, text="", font=("Segoe UI", 10), text_color="#CC0000", width=160, anchor="w")
        lbl_pep.grid(row=0, column=3, sticky="w", padx=4, pady=6)

        btn_rm = ctk.CTkButton(
            frm, text="X",
            font=("Segoe UI", 10, "bold"),
            fg_color="#CC0000", hover_color="#990000",
            width=28, height=26, corner_radius=6,
            command=lambda f=frm: self._remover_parte(f),
        )
        btn_rm.grid(row=0, column=4, padx=(2, 8), pady=6)

        # Documentação (row 1, col 0-4)
        validacoes = [
            ("doc_oficial", "Doc. Oficial Válido"),
            ("cpf_regular", "CPF Regular"),
            ("estado_civil", "Estado Civil Comprovado"),
            ("regime_bens", "Regime de Bens Verificado"),
            ("endereco", "Endereço Atualizado"),
            ("profissao", "Profissão Informada"),
            ("contato", "Contato Atualizado"),
        ]
        docs_frame = ctk.CTkFrame(frm, fg_color="#f9faf9", corner_radius=6)
        docs_frame.grid(row=1, column=0, columnspan=5, sticky="ew", padx=8, pady=(0, 6))
        docs_vars = {}
        docs_dados = dados.get("docs", {}) if dados else {}
        for i, (chave, label) in enumerate(validacoes):
            var = ctk.StringVar(value="1" if docs_dados.get(chave) else "")
            cb = ctk.CTkCheckBox(docs_frame, text=label, variable=var, onvalue="1", offvalue="", fg_color=COR_PRIMARIA, font=("Segoe UI", 10))
            cb.grid(row=0, column=i, sticky="w", padx=(0, 8), pady=4)
            docs_vars[chave] = var

        # Timers para consulta automática
        timer_key = {"after_id": None}

        def _auto_consultar():
            nome = entry_nome.get().strip()
            cpf = entry_cpf.get().strip()
            if not nome and not cpf:
                lbl_pep.configure(text="")
                return
            encontrado, resultados = consultar_pep(nome=nome, cpf=cpf)
            if encontrado:
                resumo = obter_resumo_pep(resultados)
                lbl_pep.configure(text=f"PEP: {resumo[:90]}", text_color="#CC0000")
            else:
                lbl_pep.configure(text="Nao e PEP", text_color=COR_PRIMARIA)

        def _agendar_consulta(*args):
            if timer_key["after_id"]:
                self.after_cancel(timer_key["after_id"])
            timer_key["after_id"] = self.after(600, _auto_consultar)

        entry_nome.bind("<KeyRelease>", _agendar_consulta)
        entry_cpf.bind("<KeyRelease>", _agendar_consulta)

        self._partes.append({
            "frame": frm,
            "nome": entry_nome,
            "cpf": entry_cpf,
            "papel_var": papel_var,
            "lbl_pep": lbl_pep,
            "timer_key": timer_key,
            "docs_vars": docs_vars,
        })

        if (entry_nome.get().strip() or entry_cpf.get().strip()):
            self.after(100, _auto_consultar)

    def _remover_parte(self, frame):
        for i, p in enumerate(self._partes):
            if p["frame"] == frame:
                self._partes.pop(i)
                break
        frame.destroy()
        self._reorganizar_partes()

    def _reorganizar_partes(self):
        for i, p in enumerate(self._partes):
            p["frame"].grid(row=i, column=0, sticky="ew", padx=8, pady=3)

    def _coletar_partes(self) -> List[Dict]:
        partes = []
        for p in self._partes:
            item = {
                "nome": p["nome"].get().strip(),
                "cpf": p["cpf"].get().strip(),
                "papel": p["papel"].get(),
            }
            if item["nome"] or item["cpf"]:
                encontrado, resultados = consultar_pep(nome=item["nome"], cpf=item["cpf"])
                item["pep"] = encontrado
                item["pep_detalhe"] = obter_resumo_pep(resultados) if encontrado else ""
                item["docs"] = {chave: var.get() == "1" for chave, var in p["docs_vars"].items()}
                partes.append(item)
        return partes

    def _secao_origem_recursos(self, parent, linha: int) -> int:
        card = self._card(parent, "Origem dos recursos", linha)
        r = 1

        frm_origem = ctk.CTkFrame(card, fg_color="transparent")
        frm_origem.grid(row=r, column=0, columnspan=3, sticky="ew", padx=16, pady=(0, 8))
        frm_origem.grid_columnconfigure((0, 1), weight=1)

        ctk.CTkLabel(frm_origem, text="Origem identificada?", font=("Segoe UI", 12), text_color=COR_TEXTO).grid(row=0, column=0, sticky="w")
        self._origem_var = ctk.StringVar(value="Sim")
        frm_r1 = ctk.CTkFrame(frm_origem, fg_color="transparent")
        frm_r1.grid(row=1, column=0, sticky="w")
        ctk.CTkRadioButton(frm_r1, text="Sim", variable=self._origem_var, value="Sim").pack(side="left", padx=(0, 15))
        ctk.CTkRadioButton(frm_r1, text="Não", variable=self._origem_var, value="Não").pack(side="left")

        ctk.CTkLabel(frm_origem, text="Doc. comprobatória?", font=("Segoe UI", 12), text_color=COR_TEXTO).grid(row=0, column=1, sticky="w")
        self._doc_var = ctk.StringVar(value="Sim")
        frm_r2 = ctk.CTkFrame(frm_origem, fg_color="transparent")
        frm_r2.grid(row=1, column=1, sticky="w")
        ctk.CTkRadioButton(frm_r2, text="Sim", variable=self._doc_var, value="Sim").pack(side="left", padx=(0, 15))
        ctk.CTkRadioButton(frm_r2, text="Não", variable=self._doc_var, value="Não").pack(side="left")
        r += 1

        return linha + 1

    def _secao_pagamento(self, parent, linha: int) -> int:
        card = self._card(parent, "Forma de pagamento", linha)
        r = 1

        ctk.CTkLabel(card, text="Pagamento em espécie?", font=("Segoe UI", 12), text_color=COR_TEXTO).grid(row=r, column=0, sticky="w", padx=16, pady=(0, 2))
        r += 1
        self._especie_var = ctk.StringVar(value="Não")
        frm_esp = ctk.CTkFrame(card, fg_color="transparent")
        frm_esp.grid(row=r, column=0, sticky="w", padx=16, pady=(0, 2))
        ctk.CTkRadioButton(frm_esp, text="Sim", variable=self._especie_var, value="Sim", command=self._toggle_especie).pack(side="left", padx=(0, 20))
        ctk.CTkRadioButton(frm_esp, text="Não", variable=self._especie_var, value="Não", command=self._toggle_especie).pack(side="left")
        r += 1

        self._especie_frame = ctk.CTkFrame(card, fg_color="transparent")
        self._especie_frame.grid(row=r, column=0, columnspan=3, sticky="ew", padx=16, pady=(0, 8))
        ctk.CTkLabel(self._especie_frame, text="Valor pago em espécie (R$):", font=("Segoe UI", 12), text_color=COR_TEXTO).grid(row=0, column=0, sticky="w")
        self._valor_especie = ctk.CTkEntry(self._especie_frame, placeholder_text="0,00", width=200)
        self._valor_especie.grid(row=1, column=0, sticky="w")
        self._especie_frame.grid_remove()
        r += 1

        ctk.CTkLabel(card, text="Pagamento fracionado?", font=("Segoe UI", 12), text_color=COR_TEXTO).grid(row=r, column=0, sticky="w", padx=16, pady=(0, 2))
        r += 1
        self._fracionado_var = ctk.StringVar(value="Não")
        frm_frac = ctk.CTkFrame(card, fg_color="transparent")
        frm_frac.grid(row=r, column=0, sticky="w", padx=16, pady=(0, 6))
        ctk.CTkRadioButton(frm_frac, text="Sim", variable=self._fracionado_var, value="Sim").pack(side="left", padx=(0, 20))
        ctk.CTkRadioButton(frm_frac, text="Não", variable=self._fracionado_var, value="Não").pack(side="left")
        r += 1

        ctk.CTkLabel(card, text="Várias operações relacionadas?", font=("Segoe UI", 12), text_color=COR_TEXTO).grid(row=r, column=0, sticky="w", padx=16, pady=(0, 2))
        r += 1
        self._relacionadas_var = ctk.StringVar(value="Não")
        frm_rel = ctk.CTkFrame(card, fg_color="transparent")
        frm_rel.grid(row=r, column=0, sticky="w", padx=16, pady=(0, 6))
        ctk.CTkRadioButton(frm_rel, text="Sim", variable=self._relacionadas_var, value="Sim").pack(side="left", padx=(0, 20))
        ctk.CTkRadioButton(frm_rel, text="Não", variable=self._relacionadas_var, value="Não").pack(side="left")
        r += 1

        return linha + 1

    def _toggle_especie(self):
        if self._especie_var.get() == "Sim":
            self._especie_frame.grid()
        else:
            self._especie_frame.grid_remove()

    def _secao_situacoes_suspeitas(self, parent, linha: int) -> int:
        card = self._card(parent, "Situações suspeitas", linha)
        r = 1

        ctk.CTkLabel(
            card,
            text="Marque todas as situações identificadas:",
            font=("Segoe UI", 11),
            text_color=COR_SUBTEXTO,
        ).grid(row=r, column=0, columnspan=3, sticky="w", padx=16, pady=(0, 6))
        r += 1

        self._suspeitas_vars: Dict[str, ctk.BooleanVar] = {}
        for situacao in obter_situacoes():
            var = ctk.BooleanVar(value=False)
            self._suspeitas_vars[situacao.chave] = var
            cb = ctk.CTkCheckBox(
                card,
                text=situacao.texto,
                variable=var,
                font=("Segoe UI", 12),
                text_color=COR_TEXTO,
                fg_color=COR_PRIMARIA,
                hover_color="#1B5E20",
            )
            cb.grid(row=r, column=0, columnspan=3, sticky="w", padx=16, pady=1)
            r += 1

        return linha + 1

    def _secao_observacoes(self, parent, linha: int) -> int:
        card = self._card(parent, "Observações", linha)
        r = 1

        self._observacoes = ctk.CTkTextbox(card, height=70, width=600, corner_radius=8)
        self._observacoes.grid(row=r, column=0, columnspan=3, sticky="ew", padx=16, pady=(0, 12))

        return linha + 1

    def _coletar_dados(self) -> Dict:
        result = {
            "tipo_ato": self._tipo_ato.get(),
            "valor": validar_valor(self._valor.get()) or 0.0,
            "forma_pagamento": self._forma_pagamento.get(),
            "cidade": self._cidade.get(),
            "estado": self._estado.get(),
            "data": self._data.get(),
            "qtd_compradores": int(self._qtd_compradores.get()) if self._qtd_compradores.get().isdigit() else 0,
            "qtd_vendedores": int(self._qtd_vendedores.get()) if self._qtd_vendedores.get().isdigit() else 0,
            "pep": self._pep_var.get() == "Sim",
            "pep_nome": self._pep_nome.get(),
            "pep_cargo": self._pep_cargo.get(),
            "pep_cidade": self._pep_cidade.get(),
            "origem_identificada": self._origem_var.get() == "Sim",
            "doc_comprobatoria": self._doc_var.get() == "Sim",
            "pagamento_especie": self._especie_var.get() == "Sim",
            "valor_especie": validar_valor(self._valor_especie.get()) if self._especie_var.get() == "Sim" else 0.0,
            "pagamento_fracionado": self._fracionado_var.get() == "Sim",
            "operacoes_relacionadas": self._relacionadas_var.get() == "Sim",
            "observacoes": self._observacoes.get("1.0", "end-1c"),
        }
        if result["tipo_ato"] == "Procuração":
            result["poderes"] = [v.get() for v in self._poderes_vars.values() if v.get()]
            result["poderes_outros"] = self._poderes_outros.get("1.0", "end-1c").strip()
        for s in obter_situacoes():
            result[f"suspeita_{s.chave}"] = self._suspeitas_vars[s.chave].get()
        result["partes"] = self._coletar_partes()
        return result

    def _preencher_formulario(self, dados: Dict):
        self._carregando = True
        if "tipo_ato" in dados:
            self._tipo_ato.set(dados["tipo_ato"])
            self._ao_tipo_ato(dados["tipo_ato"])
        if "poderes" in dados and dados["tipo_ato"] == "Procuração":
            for p in self._PODERES_OPCOES:
                self._poderes_vars[p].set(p if p in dados.get("poderes", []) else "")
            self._poderes_outros.delete("1.0", "end")
            self._poderes_outros.insert("1.0", dados.get("poderes_outros", ""))
        if "valor" in dados and dados["valor"]:
            val = dados["valor"]
            self._valor.delete(0, "end")
            self._valor.insert(0, f"{val:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".") if isinstance(val, float) else str(val))
        if "forma_pagamento" in dados:
            self._forma_pagamento.set(dados["forma_pagamento"])
        if "cidade" in dados:
            self._cidade.delete(0, "end")
            self._cidade.insert(0, dados["cidade"])
        if "estado" in dados:
            self._estado.set(dados["estado"])
        if "data" in dados:
            self._data.delete(0, "end")
            self._data.insert(0, dados["data"])
        if "qtd_compradores" in dados:
            self._qtd_compradores.delete(0, "end")
            self._qtd_compradores.insert(0, str(dados["qtd_compradores"]))
        if "qtd_vendedores" in dados:
            self._qtd_vendedores.delete(0, "end")
            self._qtd_vendedores.insert(0, str(dados["qtd_vendedores"]))
        if "pep" in dados:
            self._pep_var.set("Sim" if dados["pep"] else "Não")
            self._toggle_pep()
        if "pep_nome" in dados:
            self._pep_nome.delete(0, "end")
            self._pep_nome.insert(0, dados["pep_nome"])
        if "pep_cargo" in dados:
            self._pep_cargo.delete(0, "end")
            self._pep_cargo.insert(0, dados["pep_cargo"])
        if "pep_cidade" in dados:
            self._pep_cidade.delete(0, "end")
            self._pep_cidade.insert(0, dados["pep_cidade"])
        if "origem_identificada" in dados:
            self._origem_var.set("Sim" if dados["origem_identificada"] else "Não")
        if "doc_comprobatoria" in dados:
            self._doc_var.set("Sim" if dados["doc_comprobatoria"] else "Não")
        if "pagamento_especie" in dados:
            self._especie_var.set("Sim" if dados["pagamento_especie"] else "Não")
            self._toggle_especie()
        if "valor_especie" in dados and dados["valor_especie"]:
            val = dados["valor_especie"]
            self._valor_especie.delete(0, "end")
            self._valor_especie.insert(0, f"{val:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
        if "pagamento_fracionado" in dados:
            self._fracionado_var.set("Sim" if dados["pagamento_fracionado"] else "Não")
        if "operacoes_relacionadas" in dados:
            self._relacionadas_var.set("Sim" if dados["operacoes_relacionadas"] else "Não")
        for s in obter_situacoes():
            chave = f"suspeita_{s.chave}"
            if chave in dados:
                self._suspeitas_vars[s.chave].set(dados[chave])
        if "observacoes" in dados:
            self._observacoes.delete("1.0", "end")
            self._observacoes.insert("1.0", dados["observacoes"])
        if "partes" in dados and isinstance(dados["partes"], list):
            while len(self._partes) > 0:
                p = self._partes.pop()
                p["frame"].destroy()
            for p in dados["partes"]:
                self._adicionar_parte(dados=p)
        self._carregando = False

    def _validar(self) -> Optional[str]:
        dados = self._coletar_dados()
        if not dados.get("cidade", "").strip():
            return "Informe a cidade do ato."
        if not dados.get("data", "").strip():
            return "Informe a data do ato."
        if dados["valor"] <= 0:
            return "Informe um valor válido para o negócio."
        if dados["pep"] and not dados.get("pep_nome", "").strip():
            return "Informe o nome do PEP."
        if dados["pagamento_especie"] and dados["valor_especie"] <= 0:
            return "Informe o valor pago em espécie."
        return None

    def _analisar(self):
        erro = self._validar()
        if erro:
            self._set_status(f"Erro: {erro}")
            return
        dados = self._coletar_dados()

        partes_pep = [p for p in dados.get("partes", []) if p.get("pep")]
        if partes_pep:
            if not dados.get("pep"):
                dados["pep"] = True
                dados["pep_nome"] = partes_pep[0]["nome"]
                dados["pep_cargo"] = partes_pep[0].get("pep_detalhe", "PEP")
                dados["pep_cidade"] = ""

        resultado, motivos, pontuacao = aplicar_regras(dados)
        try:
            analise_id = salvar_analise(dados, resultado, motivos, pontuacao)
            self._set_status(f"Análise #{analise_id} salva. {len(motivos)} motivo(s) encontrado(s).")
        except Exception as e:
            self._set_status(f"Análise realizada (erro ao salvar: {e})")
        ResultadoWindow(self, dados, resultado, motivos, pontuacao)

    def _limpar_formulario(self):
        self._tipo_ato.set("Compra e venda")
        self._valor.delete(0, "end")
        self._forma_pagamento.set("TED")
        self._cidade.delete(0, "end")
        self._estado.set("SP")
        self._data.delete(0, "end")
        self._qtd_compradores.delete(0, "end")
        self._qtd_vendedores.delete(0, "end")
        self._pep_var.set("Não")
        self._toggle_pep()
        self._pep_nome.delete(0, "end")
        self._pep_cargo.delete(0, "end")
        self._pep_cidade.delete(0, "end")
        self._origem_var.set("Sim")
        self._doc_var.set("Sim")
        self._especie_var.set("Não")
        self._toggle_especie()
        self._valor_especie.delete(0, "end")
        self._fracionado_var.set("Não")
        self._relacionadas_var.set("Não")
        for var in self._suspeitas_vars.values():
            var.set(False)
        while self._partes:
            p = self._partes.pop()
            p["frame"].destroy()
        self._adicionar_parte()
        self._adicionar_parte()
        self._observacoes.delete("1.0", "end")
        self._set_status("Formulário limpo.")

    def _abrir_historico(self):
        HistoricoWindow(self)


class HistoricoWindow(ctk.CTkToplevel):
    def __init__(self, parent: AnalisadorSISCOAF):
        super().__init__(parent)
        self._parent = parent

        self.title("Histórico de Análises")
        self.geometry("700x520")
        self.minsize(500, 400)
        self.configure(fg_color=COR_BG)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        ctk.CTkLabel(
            self,
            text="Histórico de Análises",
            font=("Segoe UI", 18, "bold"),
            text_color=COR_PRIMARIA,
        ).grid(row=0, column=0, sticky="w", padx=20, pady=(16, 8))

        frm_busca = ctk.CTkFrame(self, fg_color="transparent")
        frm_busca.grid(row=1, column=0, sticky="ew", padx=20, pady=(0, 10))
        frm_busca.grid_columnconfigure(0, weight=1)

        self._busca_entry = ctk.CTkEntry(frm_busca, placeholder_text="Buscar no histórico...")
        self._busca_entry.grid(row=0, column=0, sticky="ew", padx=(0, 8))
        self._busca_entry.bind("<Return>", lambda e: self._carregar_lista())

        ctk.CTkButton(
            frm_busca,
            text="Buscar",
            font=("Segoe UI", 12),
            fg_color="#5C6BC0",
            hover_color="#3F51B5",
            width=80,
            height=32,
            corner_radius=8,
            command=self._carregar_lista,
        ).grid(row=0, column=1, padx=(0, 4))

        ctk.CTkButton(
            frm_busca,
            text="Recarregar",
            font=("Segoe UI", 12),
            fg_color=COR_PRIMARIA,
            hover_color="#1B5E20",
            width=100,
            height=32,
            corner_radius=8,
            command=self._carregar_lista,
        ).grid(row=0, column=2)

        scroll = ctk.CTkScrollableFrame(self, fg_color=COR_CARD, corner_radius=10)
        scroll.grid(row=2, column=0, sticky="nsew", padx=20, pady=(0, 16))
        scroll.grid_columnconfigure(0, weight=1)

        self._scroll = scroll
        self._carregar_lista()

    def _carregar_lista(self):
        for w in self._scroll.winfo_children():
            w.destroy()

        termo = self._busca_entry.get().strip()
        analises = buscar_analises(termo) if termo else listar_analises(50)

        if not analises:
            ctk.CTkLabel(
                self._scroll,
                text="Nenhuma análise encontrada.",
                font=("Segoe UI", 13),
                text_color=COR_SUBTEXTO,
            ).grid(row=0, column=0, padx=16, pady=20)
            return

        for i, a in enumerate(analises):
            cor = "#CC0000" if a["resultado"] == "COMUNICAR" else "#006600"
            frm = ctk.CTkFrame(self._scroll, fg_color="transparent", border_width=1, border_color="#DDD", corner_radius=8)
            frm.grid(row=i, column=0, sticky="ew", padx=8, pady=3)
            frm.grid_columnconfigure(1, weight=1)

            lbl_data = ctk.CTkLabel(
                frm, text=a["data_hora"][:19].replace("T", " "),
                font=("Segoe UI", 11), text_color=COR_SUBTEXTO, width=150, anchor="w",
            )
            lbl_data.grid(row=0, column=0, sticky="w", padx=(12, 8), pady=6)

            lbl_res = ctk.CTkLabel(
                frm, text="COMUNICAR" if a["resultado"] == "COMUNICAR" else "NÃO COMUNICAR",
                font=("Segoe UI", 11, "bold"), text_color=cor, width=130, anchor="w",
            )
            lbl_res.grid(row=0, column=1, sticky="w", padx=4, pady=6)

            lbl_pts = ctk.CTkLabel(
                frm, text=f"{a['pontuacao']} pts",
                font=("Segoe UI", 10), text_color=COR_SUBTEXTO, width=50, anchor="w",
            )
            lbl_pts.grid(row=0, column=2, sticky="w", padx=4, pady=6)

            ctk.CTkButton(
                frm, text="Carregar",
                font=("Segoe UI", 11),
                fg_color=COR_PRIMARIA,
                hover_color="#1B5E20",
                width=80, height=28,
                corner_radius=6,
                command=lambda aid=a["id"]: self._carregar_analise(aid),
            ).grid(row=0, column=3, padx=(8, 12), pady=6)

    def _carregar_analise(self, analise_id: int):
        analise = carregar_analise(analise_id)
        if analise is None:
            return
        self._parent._preencher_formulario(analise["dados_json"])
        self._parent._set_status(f"Análise #{analise_id} carregada do histórico.")
        self.destroy()


class ResultadoWindow(ctk.CTkToplevel):
    def __init__(self, parent, dados: Dict, resultado: str, motivos: List[str], pontuacao: int):
        super().__init__(parent)

        self._dados = dados
        self._resultado = resultado
        self._motivos = motivos
        self._pontuacao = pontuacao

        self.title("Resultado da Análise")
        self.geometry("560x520")
        self.minsize(450, 400)
        self.configure(fg_color=COR_BG)
        _aplicar_icon(self)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=0)

        self._construir()

    def _construir(self):
        main = ctk.CTkFrame(self, fg_color=COR_CARD, corner_radius=16)
        main.grid(row=0, column=0, sticky="ew", padx=20, pady=(20, 10))
        main.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            main,
            text="Resultado da Análise",
            font=("Segoe UI", 18, "bold"),
            text_color=COR_TEXTO,
        ).grid(row=0, column=0, pady=(16, 8))

        texto_resultado = "COMUNICAR AO SISCOAF" if self._resultado == "COMUNICAR" else "NÃO COMUNICAR AO SISCOAF"
        cor_resultado = "#CC0000" if self._resultado == "COMUNICAR" else "#006600"
        ctk.CTkLabel(
            main,
            text=texto_resultado,
            font=("Segoe UI", 22, "bold"),
            text_color=cor_resultado,
        ).grid(row=1, column=0, pady=(0, 4))

        ctk.CTkLabel(
            main,
            text=f"Pontuação total: {self._pontuacao}",
            font=("Segoe UI", 12),
            text_color=COR_SUBTEXTO,
        ).grid(row=2, column=0, pady=(0, 16))

        frm_motivos = ctk.CTkFrame(self, fg_color="transparent")
        frm_motivos.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0, 10))
        frm_motivos.grid_columnconfigure(0, weight=1)
        frm_motivos.grid_rowconfigure(1, weight=1)

        ctk.CTkLabel(
            frm_motivos,
            text="Motivos encontrados:",
            font=("Segoe UI", 14, "bold"),
            text_color=COR_TEXTO,
        ).grid(row=0, column=0, sticky="w", pady=(0, 8))

        scroll_motivos = ctk.CTkScrollableFrame(frm_motivos, fg_color=COR_CARD, corner_radius=10)
        scroll_motivos.grid(row=1, column=0, sticky="nsew")
        scroll_motivos.grid_columnconfigure(0, weight=1)

        if self._motivos:
            for i, motivo in enumerate(self._motivos):
                ctk.CTkLabel(
                    scroll_motivos,
                    text=f"✔ {motivo}",
                    font=("Segoe UI", 12),
                    text_color=COR_TEXTO,
                    wraplength=480,
                    justify="left",
                ).grid(row=i, column=0, sticky="w", padx=12, pady=3)
        else:
            ctk.CTkLabel(
                scroll_motivos,
                text="Nenhum critério objetivo para comunicação foi identificado conforme as regras configuradas.",
                font=("Segoe UI", 12),
                text_color=COR_SUBTEXTO,
                wraplength=480,
                justify="left",
            ).grid(row=0, column=0, sticky="w", padx=12, pady=12)

        frm_botoes = ctk.CTkFrame(self, fg_color="transparent")
        frm_botoes.grid(row=2, column=0, sticky="ew", padx=20, pady=(0, 20))
        frm_botoes.grid_columnconfigure((0, 1), weight=1)

        ctk.CTkButton(
            frm_botoes,
            text="Gerar Relatório PDF",
            font=("Segoe UI", 13, "bold"),
            fg_color=COR_PRIMARIA,
            hover_color="#1B5E20",
            height=40,
            corner_radius=10,
            command=self._gerar_relatorio,
        ).grid(row=0, column=0, sticky="ew", padx=(0, 8))

        ctk.CTkButton(
            frm_botoes,
            text="Fechar",
            font=("Segoe UI", 13),
            fg_color="#888888",
            hover_color="#666666",
            height=40,
            corner_radius=10,
            command=self.destroy,
        ).grid(row=0, column=1, sticky="ew", padx=(8, 0))

    def _gerar_relatorio(self):
        import subprocess
        caminho = gerar_relatorio(
            dados=self._dados,
            resultado=self._resultado,
            motivos=self._motivos,
            pontuacao=self._pontuacao,
            usuario="Colaborador",
        )
        subprocess.Popen(["start", "", caminho], shell=True)
