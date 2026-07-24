# Contexto da Arquitetura — Analisador SISCOAF

## 1. Visão Geral do Produto

**Analisador SISCOAF** é uma plataforma desktop e web para auxiliar notários e registradores na análise de comunicações obrigatórias ao SISCOAF/COAF (Conselho de Controle de Atividades Financeiras), conforme o Provimento CN n. 149/2023 (incluído pelo Provimento CN n. 161/2024).

### Problema resolvido
Notários e registradores precisam avaliar cada ato notarial/registral contra 37 indicadores de suspeita de lavagem de dinheiro, consultar bases de PEP, calcular pontuação de risco e decidir se devem comunicar ao COAF. O sistema automatiza esse fluxo.

### Usuários-alvo
- Tabeliães de notas
- Oficiais de registro de imóveis
- Oficiais de protesto
- Oficiais de registro de títulos e documentos
- Analistas de PLD/FTP em cartórios

---

## 2. Stack Tecnológica

| Camada | Tecnologia | Versão |
|---|---|---|
| Linguagem | Python | 3.x |
| Interface Desktop | customtkinter | — |
| Interface Web | HTML5 + CSS3 + Vanilla JS | — |
| Banco de dados | SQLite (via sqlite3) / localStorage / IndexedDB | — |
| Relatórios PDF | ReportLab | — |
| Base PEP | CSV (latin-1) | — |
| Build | PyInstaller (via .spec) | — |
| Versionamento | Git | — |

---

## 3. Arquitetura do Sistema

### 3.1. Desktop (Python / customtkinter)

```
┌─────────────────────────────────────────────────────────┐
│                     main.py                              │
│  Ponto de entrada: inicializa DB + abre interface       │
├─────────────────────────────────────────────────────────┤
│                     interface.py                         │
│  AnalisadorSISCOAF (CTk) — formulário principal         │
│  HistoricoWindow (CTkToplevel) — histórico de análises   │
│  ResultadoWindow (CTkToplevel) — resultado da análise    │
├─────────────────────────────────────────────────────────┤
│  config.py         │  regras.py         │  database.py   │
│  ScoringConfig     │  aplicar_regras()  │  inicializar() │
│  SituacaoItem      │  _regra_docs()     │  salvar/ler    │
│  obter_situacoes() │                    │  buscar/listar │
├────────────────────┼────────────────────┼───────────────┤
│  pep_consulta.py   │  relatorio.py      │  utils.py      │
│  carregar PEP CSV  │  gerar_relatorio() │  validar_valor │
│  consultar_pep()   │  PDF via ReportLab │  formatar_moeda│
│  obter_resumo_pep()│  plano de fundo    │                │
└────────────────────┴────────────────────┴───────────────┘
```

### 3.2. Web (HTML/CSS/JS estático)

```
┌─────────────────────────────────────────────────────────────┐
│                    admin.html (Dashboard)                    │
│  KPIs, timeline, gráficos, alertas PEP (dados mockados)     │
├─────────────────────────────────────────────────────────────┤
│                    index.html (Nova Análise)                 │
│  Formulário completo com JS local, localStorage, IndexedDB   │
│  - Partes com consulta PEP automática                        │
│  - 37 situações suspeitas                                   │
│  - Motor de regras replicado em JS                          │
│  - Geração de relatório (print-to-PDF via janela)           │
├─────────────────────────────────────────────────────────────┤
│ configuracoes.html              │  historico.html           │
│ Scoring, limites, regras        │  Filtros, tabelas,        │
│ Export/Import JSON              │  gráficos, alertas PEP    │
├─────────────────────────────────┴───────────────────────────┤
│                    usuarios.html                             │
│  Gestão de usuários mockada, filtros, gráficos, paginação   │
└─────────────────────────────────────────────────────────────┘
```

### 3.3. Fluxo de Dados

```
Usuário → Preenche formulário (partes, PEP, suspeitas, etc.)
              ↓
         Coletar Dados (JSON)
              ↓
    ┌─────────────────────┐
    │ Aplicar Regras      │
    │ - Situações suspeitas│
    │ - PEP                │
    │ - Documentação docs  │
    └─────────┬───────────┘
              ↓
    Resultado (COMUNICAR / NAO_COMUNICAR)
    Pontuação + Motivos
              ↓
    ┌─────────────────────┐
    │ Salvar no histórico  │ → SQLite (desktop) / localStorage (web)
    │ Exibir resultado     │ → ResultadoWindow / Modal
    │ Gerar PDF            │ → ReportLab / print-to-PDF
    └─────────────────────┘
```

---

## 4. Módulos Detalhados

### 4.1. `config.py` — Configurações Centralizadas

- **`ScoringConfig`**: dataclass com pesos para cada critério (pep=3, docs_incompletas=2, etc.)
- **`SituacaoItem`**: dataclass para cada indicador (chave, código, artigo, texto, pontuação)
- **`obter_situacoes()`**: lista com 37 itens dos Arts. 155-A a 172 do Provimento CN 149/2023
- Constantes: `TIPO_ATO_CATEGORIAS` (4), `ESCRITURA_OPCOES` (8), `FORMA_PAGAMENTO_OPCOES` (8), `ESTADOS` (27)

### 4.2. `regras.py` — Motor de Decisão

**Fluxo de decisão:**
1. Se qualquer situação suspeita marcada como "Sim" → **COMUNICAR** (soma pontos)
2. Se PEP declarado → soma 3 pontos
3. Se documentação de partes incompleta → soma 2 pontos + motivo
4. Se houver motivos → **COMUNICAR**, senão **NAO_COMUNICAR**

**Verificação documental por tipo:**
- **PF** (7 docs): doc_oficial, cpf_regular, estado_civil, regime_bens, endereco, profissao, contato
- **PJ** (6 docs): pj_cnpj, pj_contrato_social, pj_alteracoes, pj_representante, pj_poderes, pj_objeto_social

### 4.3. `database.py` — Persistência

- SQLite local (`historico.db`)
- Tabela `analises`: id, data_hora, resultado, pontuacao, motivos (JSON), dados_json (JSON), usuario
- Funções: `inicializar()`, `salvar_analise()`, `listar_analises()`, `buscar_analises()`, `carregar_analise()`

### 4.4. `pep_consulta.py` — Consulta PEP

- Carrega CSV oficial da base de PEP (caminho: `pep_db/202605_PEP.csv`)
- Cache em memória (`_pep_cache`)
- Busca por CPF (match de 6 dígitos centrais) ou nome (substring)
- Resumo consolidado: cargos e localizações

### 4.5. `relatorio.py` — Geração de PDF

- ReportLab com template A4
- Plano de fundo: `Plano de Ofício 1.png` (imagem institucional)
- Seções: identificação, partes, PEP, características, pagamento, suspeitas, justificativa
- Cores condicionais: vermelho para COMUNICAR, verde para NÃO COMUNICAR

### 4.6. `utils.py` — Utilitários

- `validar_valor()`: string → float (trata formato brasileiro)
- `formatar_moeda()`: float → string "R$ 1.234,56"
- `data_hora_atual()`: timestamp formatado

---

## 5. Interface Desktop (`interface.py`)

### 5.1. Classe `AnalisadorSISCOAF` (CTk)

Paleta de cores:
- `COR_CARD = "#F0F4F0"` (fundo dos cards)
- `COR_BG = "#FAFAFA"` (fundo geral)
- `COR_PRIMARIA = "#2E7D32"` (verde institucional)

**Seções do formulário:**

| Seção | Campos |
|---|---|
| Identificação | Funcionário, Protocolo, OS, Livro, Folha |
| Partes | Nome CPF/CNPJ, PF/PJ, Papel, Rep. Procuração, Documentação (7 ou 6 itens) |
| PEP | Sim/Não, Nome, Cargo, Cidade |
| Dados do ato | Tipo (Escritura/Procuração/Protesto/PJ), Subtipo, Valor, Pagamento, Cidade, Estado, Data |
| Pagamento | Forma (PIX/TED/Dinheiro/Cheque/Boleto/Mista/Outro) |
| Suspeitas | 37 indicadores com Sim/Não |
| Observações | Texto livre |

### 5.2. Classes auxiliares

- **`HistoricoWindow`**: lista análises com busca, botão "Carregar" restaura formulário
- **`ResultadoWindow`**: exibe decisão, pontuação, motivos, botões PDF/Fechar

### 5.3. Funcionalidades dinâmicas

- `_ao_tipo_ato()`: toggle visibilidade de seções conforme tipo selecionado
- `_adicionar_parte()`: adiciona dynamicamente linhas de parte com validação
- `_recriar_docs_parte()`: recria lista de docs ao alternar PF/PJ
- Consulta PEP automática com debounce de 600ms via `after()`

---

## 6. Interface Web (HTML/JS)

### 6.1. Páginas

| Arquivo | Rota | Descrição |
|---|---|---|
| `admin.html` | /admin | Dashboard com KPIs, gráficos, timeline |
| `index.html` | / | Formulário de análise completo |
| `historico.html` | /historico | Histórico com filtros e tabela |
| `configuracoes.html` | /config | Pontuações, limites, regras |
| `usuarios.html` | /usuarios | Gestão de usuários mockada |

### 6.2. Armazenamento Web

- **localStorage**: `siscoaf_config` (configurações), `siscoaf_historico` (últimas 100 análises)
- **IndexedDB**: base PEP persistida (`SiscoafDB` / `pep` store)

### 6.3. Motor de Regras Web

Replicado em JavaScript (`index.html:947-975`) com mesma lógica do backend Python:
- Situações suspeitas com pontuação
- PEP scoring
- Documentação incompleta
- Limite de comunicação configurável

---

## 7. Base de Dados PEP

### 7.1. Formato
- Arquivo CSV com delimitador `;`, encoding `latin-1`
- Localização: `pep_db/202605_PEP.csv`
- Colunas esperadas: CPF, Nome_PEP, Descricao_Funcao, Nome_Orgao

### 7.2. Algoritmo de busca
- Extrai 6 dígitos centrais do CPF (posições 3-8) para matching
- Busca por nome com `string.upper().includes(termo.upper())`
- Resultados consolidados: máx. 3 registros no resumo

---

## 8. Regras de Negócio (Provimento CN n. 149/2023)

### 8.1. Indícios de Suspeita (37 itens)
Cobrem:
- Arts. 155-A, I a XVIII (18 indicadores gerais)
- Art. 155-A, Parágrafo único, I e II (2 indicadores)
- Arts. 159 a 164 (13 indicadores específicos por tipo de oficial)
- Arts. 171 a 172 (4 indicadores para tabeliães de notas)

### 8.2. Critérios de Pontuação

| Critério | Pesos (padrão) |
|---|---|
| Cada situação suspeita | 2 pts |
| PEP identificado | 3 pts |
| Documentação incompleta | 2 pts |

### 8.3. Decisão
- Qualquer situação suspeita → COMUNICAR
- Pontuação total + motivos → COMUNICAR se > 0 motivos
- Sem motivos → NÃO COMUNICAR

---

## 9. Estrutura de Diretórios

```
Formulário Siscoaf/
├── main.py                 # Ponto de entrada desktop
├── interface.py            # Interface customtkinter
├── config.py               # Configurações e constantes
├── regras.py               # Motor de regras
├── database.py             # SQLite operations
├── relatorio.py            # Geração de PDF
├── utils.py                # Utilitários
├── pep_consulta.py         # Consulta PEP
├── AnalisadorSISCOAF.spec  # PyInstaller spec
├── push.bat                # Git push script
├── .gitignore
├── LICENSE                 # MIT
├── implementation.md       # Plano de sprints
├── context.md              # Este documento
│
├── assets/
│   ├── icon.ico            # Ícone da aplicação
│   └── icon.png            # Ícone PNG
│
├── pep_db/
│   └── 202605_PEP.csv      # Base oficial de PEP
│
├── dist/                   # Build output (gitignored)
├── build/                  # Build temp (gitignored)
│
├── *.html                  # Web pages (admin, index, historico, configuracoes, usuarios)
├── *.png / *.jpeg          # Imagens de plano de fundo
│
└── *.db                    # SQLite database (gitignored)
```

---

## 10. Modelo de Dados (Análise)

```json
{
  "funcionario": "string",
  "protocolo": "string",
  "ordem_servico": "string",
  "livro": "string",
  "folha": "string",
  "tipo_ato_categoria": "Escritura|Procuração|Protesto|Pessoa Jurídica",
  "tipo_ato": "string",
  "tipo_ato_outro": "string",
  "poderes": ["string"],
  "poderes_outros": "string",
  "valor": "float",
  "forma_pagamento": "string",
  "pagamento_outro": "string",
  "cidade": "string",
  "estado": "string",
  "data": "string",
  "pep": "boolean",
  "pep_nome": "string",
  "pep_cargo": "string",
  "pep_cidade": "string",
  "partes": [{
    "nome": "string",
    "cpf": "string",
    "tipo": "PF|PJ",
    "papel": "Outorgante|Outorgado|Devedor|Credor|Anuente",
    "representado": "boolean",
    "proc_nome": "string",
    "proc_cpf": "string",
    "pep": "boolean",
    "pep_detalhe": "string",
    "docs": { "chave": "boolean" }
  }],
  "suspeita_cod_####": "Sim|Não",
  "observacoes": "string"
}
```

---

## 11. Decisões Arquiteturais

| Decisão | Justificativa |
|---|---|
| Desktop + Web separados | Desktop para uso offline no cartório; Web para administração remota |
| SQLite (desktop) vs localStorage (web) | Simplicidade, sem necessidade de servidor |
| Regras duplicadas (Python + JS) | Independência entre as versões; regras são simples o suficiente |
| PEP em CSV local | Base oficial fornecida pela CGU/PEP; atualização manual |
| customtkinter em vez de tkinter puro | Aparência moderna nativa com temas |
| ReportLab em vez de WeasyPrint | Leve, sem dependências pesadas |
| IndexedDB para PEP na web | Persistência entre sessões sem backend |

---

## 12. Limitações Conhecidas

- Web pages usam dados mockados (exceto `index.html` que opera sobre localStorage)
- Sem autenticação real nas páginas web
- Base PEP precisa ser atualizada manualmente (CSV)
- Consulta PEP por CPF usa apenas 6 dígitos centrais (limitado)
- Sem testes automatizados
- Sem CI/CD
- `index.html` tem a seção "5. Resultado da análise" rotulada como "8." no HTML
