# Plano de Implementação — Analisador SISCOAF

## Visão Geral

Plataforma desktop para análise de comunicações ao SISCOAF/COAF por notários e registradores, conforme o Provimento CN n. 149/2023 (alterado pelo Provimento CN n. 161/2024). O sistema coleta dados de atos notariais e registrais, consulta base de PEP, aplica regras de pontuação e gera relatórios PDF com a decisão de comunicar ou não.

---

## Sprint 1 — Fundação do Projeto

**Objetivo:** Estrutura inicial do projeto e CLI funcional.

**Tarefas:**
- [x] Criar repositório git e `.gitignore`
- [x] Definir arquitetura do projeto (módulos: `interface`, `regras`, `config`, `database`, `relatorio`, `utils`, `pep_consulta`)
- [x] Implementar `utils.py` — funções auxiliares (`validar_valor`, `formatar_moeda`)
- [x] Implementar `config.py` — classes de configuração (`ScoringConfig`, `SituacaoItem`) e listas de opções (tipos de ato, formas de pagamento, estados)
- [x] Implementar `database.py` — inicialização SQLite, CRUD de análises
- [x] Implementar `main.py` — ponto de entrada da aplicação
- [x] Criar `LICENSE` (MIT)

**Entregáveis:** CLI funcional, módulo de banco de dados, configurações centralizadas.

---

## Sprint 2 — Motor de Regras

**Objetivo:** Implementar o sistema de scoring e decisão baseado nas situações suspeitas do Provimento CN n. 149/2023.

**Tarefas:**
- [x] Mapear todos os 37 indicadores de suspeita (códigos 1356 a 1397) em `config.py`
- [x] Implementar `regras.py` — função `aplicar_regras()`
  - Pontuação por situação suspeita marcada
  - Pontuação por PEP identificado
  - Pontuação por documentação de partes incompleta
  - Decisão final: COMUNICAR vs NAO_COMUNICAR
- [x] Definir pesos no `ScoringConfig`

**Entregáveis:** Motor de regras com 37 indicadores, 3 critérios de pontuação, decisão automatizada.

---

## Sprint 3 — Interface Gráfica — Formulário Principal

**Objetivo:** Construir a interface desktop com customtkinter para entrada de dados do ato.

**Tarefas:**
- [x] Criar `interface.py` com classe `AnalisadorSISCOAF` (CTk)
- [x] Implementar toolbar (título, botões Histórico e Limpar)
- [x] Implementar seção **Identificação do atendimento** (funcionário, protocolo, OS, livro, folha)
- [x] Implementar seção **Partes do ato**
  - [x] Adicionar/remover partes dinamicamente
  - [x] Seleção PF/PJ com campos de documento e documentação distintos
  - [x] Seleção de papel (Outorgante, Outorgado, Devedor, Credor, Anuente, ~~Cedente~~)
  - [x] Checkbox "Rep. Procuração" com campos de procurador
  - [x] Lista de verificação documental por tipo (PF: 7 itens, PJ: 6 itens)
- [x] Implementar seção **PEP** (declaração manual com nome/cargo/cidade)
- [x] Implementar seção **Dados do ato**
  - [x] Tipo do ato com subcategorias (Escritura, Procuração, Protesto, PJ)
  - [x] Valor, forma de pagamento, cidade, estado, data
  - [x] Poderes da procuração (visível condicionalmente)
- [x] Implementar seção **Forma de pagamento**
- [x] Implementar seção **Indícios de suspeita** (37 itens com Sim/Não)
- [x] Implementar seção **Observações**
- [x] Botão ANALISAR com validação
- [x] Status bar

**Entregáveis:** Interface completa para preenchimento de todos os dados do ato notarial/registral.

---

## Sprint 4 — Consulta Automática de PEP

**Objetivo:** Integrar consulta automática à base oficial de PEP (Pessoas Expostas Politicamente).

**Tarefas:**
- [x] Implementar `pep_consulta.py`
  - [x] Carregar base CSV de PEP (cache em memória)
  - [x] Consulta por CPF (correspondência de dígitos centrais)
  - [x] Consulta por nome (substring case-insensitive)
  - [x] Destacar PEP na interface (label vermelha "PEP: ...")
  - [x] Consulta automática com debounce de 600ms ao digitar nome/CPF
  - [x] ~~Comparação por CPF (exclusivamente)~~
- [x] Integrar consulta no formulário de partes

**Entregáveis:** Consulta em tempo real à base de PEP com feedback visual.

---

## Sprint 5 — Janela de Resultado

**Objetivo:** Exibir o resultado da análise em uma janela dedicada.

**Tarefas:**
- [x] Implementar `ResultadoWindow` (CTkToplevel)
  - [x] Exibir resultado (COMUNICAR / NÃO COMUNICAR) com cor distinta
  - [x] Exibir pontuação total
  - [x] Listar motivos encontrados
  - [x] Botão "Gerar Relatório PDF"
  - [x] Botão "Fechar"

**Entregáveis:** Janela de resultado com feedback visual claro da decisão.

---

## Sprint 6 — Histórico de Análises

**Objetivo:** Persistir e recuperar análises realizadas.

**Tarefas:**
- [x] Implementar `HistoricoWindow` (CTkToplevel)
  - [x] Listar últimas 50 análises (data, resultado, pontuação)
  - [x] Campo de busca textual
  - [x] Botão "Carregar" para preencher formulário com dados salvos
- [x] Aperfeiçoar `database.py` — busca por termo, carregamento completo com JSON
- [x] Implementar `_preencher_formulario()` em `AnalisadorSISCOAF` — restauração completa do estado

**Entregáveis:** Histórico persistente com busca e carregamento de análises anteriores.

---

## Sprint 7 — Geração de Relatório PDF

**Objetivo:** Gerar relatório PDF profissional com plano de fundo personalizado.

**Tarefas:**
- [x] Implementar `relatorio.py` com ReportLab
  - [x] Template A4 com margens
  - [x] Plano de fundo customizado (`Plano de Ofício 1.png`)
  - [x] Seções: identificação, dados do ato, partes (com documentação), PEP, forma de pagamento, indícios de suspeita, observações, justificativa
  - [x] Formatação condicional (poderes, doações, etc.)
- [x] Abrir PDF automaticamente ao gerar

**Entregáveis:** Relatório PDF completo com branding institucional.

---

## Sprint 8 — Polimento e Finalização

**Objetivo:** Correções finais, build e distribuição.

**Tarefas:**
- [x] Implementar `_limpar_formulario()` — reset completo do formulário
- [x] Validação robusta em `_validar()`
- [x] Ícone da aplicação (`assets/icon.ico`)
- [x] Tratamento de erros (banco de dados, arquivos não encontrados)
- [x] Criar `AnalisadorSISCOAF.spec` — configuração do PyInstaller
- [x] Script `push.bat` para deploy
- [x] Otimizar cores e layout (paleta verde institucional)
- [x] Testes manuais de fluxo completo

**Entregáveis:** Aplicação empacotada, pronta para distribuição.

---

## Sprint 9 — Páginas Web de Administração

**Objetivo:** Expandir para interface web com funcionalidades administrativas.

**Tarefas planejadas:**
- [x] `index.html` — página de nova análise com formulário completo
- [x] `admin.html` — painel administrativo com KPIs, gráficos, timeline
- [x] `configuracoes.html` — configuração de regras, pesos e limites
- [x] `usuarios.html` — gestão de usuários mockada com filtros e gráficos
- [x] `historico.html` — histórico com filtros avançados e tabela
- [ ] Adaptar `relatorio.py` para servir relatórios via web
- [ ] Unificar motor de regras web com backend Python (evitar duplicação)

**Entregáveis:** Conjunto de páginas web estáticas com funcionalidades administrativas.

---

## Sprint 10 (Futuro) — Autenticação e Serventia

**Objetivo:** Adicionar controle de acesso e configuração de serventia ao sistema.

**Tarefas planejadas:**

### 10.1. Tela de Login (Web)
- [ ] Criar `login.html` com formulário de autenticação (usuário + senha)
- [ ] Implementar sistema de sessão mockada via `localStorage` / `sessionStorage`
- [ ] Redirecionar usuários não autenticados para a tela de login
- [ ] Proteger rotas: `admin.html`, `historico.html`, `configuracoes.html`, `usuarios.html` exigem login
- [ ] `index.html` (nova análise) permanece acessível sem autenticação
- [ ] Botão de logout na topbar dos painéis protegidos
- [ ] Indicar usuário logado na topbar (nome, avatar)

### 10.2. Tela de Login (Desktop)
- [ ] Implementar `LoginWindow` (CTkToplevel) no `interface.py`
- [ ] Autenticação local (usuário/senha em config ou SQLite)
- [ ] Abrir formulário principal somente após autenticação

### 10.3. Seleção de Serventia
- [ ] Adicionar campo "Serventia" no formulário (seleção entre duas opções):
  - **Cartório Coxipó do Ouro**
  - **Cartório 2º Ofício de Várzea Grande**
- [ ] Persistir serventia selecionada nas análises salvas
- [ ] Exibir serventia no relatório PDF e no histórico
- [ ] Tornar serventia um campo obrigatório na validação
- [ ] Adicionar "Serventia" como filtro no histórico

**Entregáveis:** Autenticação funcional (web + desktop), seleção de serventia integrada ao fluxo de análise.

---

## Sprint 11 (Futuro) — Qualificação "Cedente" nas Partes

**Objetivo:** Adicionar a qualificação "Cedente" à lista de papéis das partes do ato.

**Tarefas planejadas:**

### 11.1. Desktop (`interface.py`)
- [ ] Adicionar "Cedente" na lista de papéis do `CTkOptionMenu` de cada parte
- [ ] Posicionar "Cedente" abaixo de "Anuente" na ordem do seletor

### 11.2. Web (`index.html`)
- [ ] Adicionar `<option value="Cedente">Cedente</option>` no `<select>` de papel de cada parte
- [ ] Posicionar "Cedente" abaixo de "Anuente"

### 11.3. Relatório (`relatorio.py`)
- [ ] Garantir que "Cedente" seja exibido corretamente no PDF (já funciona genericamente, apenas verificar)

### 11.4. Modelo de dados
- [ ] Nenhuma alteração estrutural necessária — "Cedente" já é coberto pelo campo `papel` (string livre)

**Entregáveis:** Qualificação "Cedente" disponível em todas as interfaces (desktop, web, PDF).

---

## Sprint 12 (Futuro) — Consulta PEP por Nome Completo

**Objetivo:** Melhorar o algoritmo de consulta PEP para identificar correspondências por nome completo, não apenas por CPF.

**Tarefas planejadas:**

### 12.1. Desktop (`pep_consulta.py`)
- [ ] Substituir lógica atual de consulta por CPF (6 dígitos centrais) por busca por nome completo
  - Comparação exata do nome completo (case-insensitive, sem acentos)
  - Fallback para substring do nome completo quando não houver match exato
- [ ] Manter consulta por CPF como fallback secundário (não primário)
- [ ] Atualizar `consultar_pep()` para priorizar nome completo sobre CPF
- [ ] Atualizar `consultar_por_nome()` para suportar match de nome completo (nome + sobrenome)

### 12.2. Web (`index.html`)
- [ ] Atualizar `consultarPEPLocal()` para priorizar nome completo
- [ ] Match exato do nome completo (case-insensitive) antes de substring

### 12.3. Testes
- [ ] Verificar casos de homônimos (mesmo nome, pessoas diferentes)
- [ ] Verificar falsos positivos com substring parcial (ex.: "Maria" não deve match "Maria José" se nome completo for diferente)

**Entregáveis:** Consulta PEP mais precisa, baseada em nome completo como critério principal.
