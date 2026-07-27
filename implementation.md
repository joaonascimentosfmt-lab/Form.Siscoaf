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

## Sprint 10 — Autenticação e Serventia

**Objetivo:** Adicionar controle de acesso e configuração de serventia ao sistema.

**Tarefas realizadas:**

### 10.1. Tela de Login (Web)
- [x] Criar `login.html` com formulário de autenticação (usuário + senha)
- [x] Implementar sistema de sessão mockada via `sessionStorage`
- [x] Redirecionar usuários não autenticados para a tela de login
- [x] Proteger rotas: `admin.html`, `historico.html`, `configuracoes.html`, `usuarios.html` exigem login
- [x] `index.html` (nova análise) permanece acessível sem autenticação
- [x] Botão de logout na topbar dos painéis protegidos
- [x] Indicar usuário logado na topbar (nome, avatar)

### 10.2. Tela de Login (Desktop)
- [x] Implementar `LoginWindow` (CTkToplevel) no `interface.py`
- [x] Autenticação local (usuário/senha em config)
- [x] Abrir formulário principal somente após autenticação

### 10.3. Seleção de Serventia
- [x] Adicionar campo "Serventia" no formulário (seleção entre duas opções):
  - **Cartório Coxipó do Ouro**
  - **Cartório 2º Ofício de Várzea Grande**
- [x] Persistir serventia selecionada nas análises salvas
- [x] Exibir serventia no relatório PDF e no histórico
- [x] Tornar serventia um campo obrigatório na validação
- [x] Adicionar "Serventia" como filtro no histórico

**Entregáveis:** Autenticação funcional (web + desktop), seleção de serventia integrada ao fluxo de análise.

---

## Sprint 11 — Qualificação "Cedente" nas Partes

**Objetivo:** Adicionar a qualificação "Cedente" à lista de papéis das partes do ato.

**Tarefas realizadas:**

### 11.1. Desktop (`interface.py`)
- [x] Adicionar "Cedente" na lista de papéis do `CTkOptionMenu` de cada parte
- [x] Posicionar "Cedente" abaixo de "Anuente" na ordem do seletor

### 11.2. Web (`index.html`)
- [x] Adicionar `<option value="Cedente">Cedente</option>` no `<select>` de papel de cada parte
- [x] Posicionar "Cedente" abaixo de "Anuente"

### 11.3. Relatório (`relatorio.py`)
- [x] Garantir que "Cedente" seja exibido corretamente no PDF (já funciona genericamente, apenas verificar)

### 11.4. Modelo de dados
- [x] Nenhuma alteração estrutural necessária — "Cedente" já é coberto pelo campo `papel` (string livre)

**Entregáveis:** Qualificação "Cedente" disponível em todas as interfaces (desktop, web, PDF).

---

## Sprint 12 — Consulta PEP por Nome Completo

**Objetivo:** Melhorar o algoritmo de consulta PEP para identificar correspondências por nome completo, não apenas por CPF.

**Tarefas realizadas:**

### 12.1. Desktop (`pep_consulta.py`)
- [x] Substituir lógica atual de consulta por CPF (6 dígitos centrais) por busca por nome completo
  - Comparação exata do nome completo (case-insensitive, sem acentos)
  - Fallback para substring do nome completo quando não houver match exato
- [x] Manter consulta por CPF como fallback secundário (não primário)
- [x] Atualizar `consultar_pep()` para priorizar nome completo sobre CPF
- [x] Atualizar `consultar_por_nome()` para suportar match de nome completo (nome + sobrenome)

### 12.2. Web (`index.html`)
- [x] Atualizar `consultarPEPLocal()` para priorizar nome completo
- [x] Match exato do nome completo (case-insensitive) antes de substring

### 12.3. Testes
- [ ] Verificar casos de homônimos (mesmo nome, pessoas diferentes)
- [ ] Verificar falsos positivos com substring parcial (ex.: "Maria" não deve match "Maria José" se nome completo for diferente)

**Entregáveis:** Consulta PEP mais precisa, baseada em nome completo como critério principal.

---

## Sprint 13 — Artigos por Setor/Serventia

**Objetivo:** Separar os 37 indicadores de suspeita por setor/serventia, exibindo apenas os artigos aplicáveis conforme o tipo de ato selecionado, mais os artigos de disposições gerais.

**Tarefas realizadas:**

### 13.1. Modelo de Dados — Setores no `config.py`
- [x] Adicionar enum ou constante `SETORES` com as categorias:
  - `Tabelionato de Protesto`
  - `Registro Civil das Pessoas Jurídicas (RCPJ)`
  - `Tabelionato de Notas`
  - `Registro de Imóveis`
- [x] Adicionar campo `setor` em `SituacaoItem` para indicar a quais setores cada artigo pertence
- [x] Mapear cada código aos seus setores conforme abaixo:

#### Tabelionato de Protesto (códigos exclusivos)
| Código | Artigo | Descrição resumida |
|---|---|---|
| 1376 | Art. 159 | Pagamento/recebimento em espécie ou título ao portador ≥ R$ 100.000,00 |
| 1377 | Art. 160, I | Devedor PF ≥ R$ 100.000,00 |
| 1378 | Art. 160, II | Devedor PJ ≥ R$ 500.000,00 |

#### Registro Civil das Pessoas Jurídicas — RCPJ (códigos exclusivos)
| Código | Artigo | Descrição resumida |
|---|---|---|
| 1386 | Art. 163 | Pagamento/recebimento em espécie ou título ao portador ≥ R$ 100.000,00 |
| 1387 | Art. 164, I | Transferência de cotas/participações ou bens móveis > R$ 100.000,00 |
| 1388 | Art. 164, II | Mútuos ou doações > R$ 100.000,00 |
| 1389 | Art. 164, III | Participações em entidades estrangeiras (trusts, fundações) |
| 1390 | Art. 164, IV | Cessão de títulos de crédito/públicos ≥ R$ 500.000,00 |

#### Tabelionato de Notas (códigos exclusivos)
| Código | Artigo | Descrição resumida |
|---|---|---|
| 1371 | Art. 155-A, XVI | Procurações com amplos poderes de gestão/administração |
| 1391 | Art. 171 | Pagamento/recebimento em espécie ou título ao portador ≥ R$ 100.000,00 |
| 1392 | Art. 172 c/c 162, I | Doação de imóvel ≥ R$ 100.000,00 a terceiro sem vínculo |
| 1393 | Art. 172 c/c 162, II | Empréstimo hipotecário/alienação fiduciária entre particulares |
| 1394 | Art. 172 c/c 162, III | Negócios de sociedade dissolvida que retornou à atividade |
| 1395 | Art. 172 c/c 162, IV | Aquisição de imóveis por fundações/associações fora da finalidade |
| 1396 | Art. 172 c/c 162, V | Transmissões sucessivas do mesmo bem com diferença anormal |
| 1397 | Art. 172 c/c 162, VI | Valor declarado com diferença anormal da avaliação fiscal |

#### Registro de Imóveis (códigos exclusivos)
| Código | Artigo | Descrição resumida |
|---|---|---|
| 1379 | Art. 161 | Pagamento em espécie ou título ao portador ≥ R$ 100.000,00 |
| 1380 | Art. 162, I | Doação de imóvel ≥ R$ 100.000,00 a terceiro sem vínculo |
| 1381 | Art. 162, II | Empréstimo hipotecário/alienação fiduciária entre particulares |
| 1382 | Art. 162, III | Negócios de sociedade dissolvida que retornou à atividade |
| 1383 | Art. 162, IV | Aquisição de imóveis por fundações/associações fora da finalidade |
| 1384 | Art. 162, V | Transmissões sucessivas do mesmo bem com diferença anormal |
| 1385 | Art. 162, VI | Valor declarado com diferença anormal da avaliação fiscal |

#### Disposições Gerais (aplicam-se a TODOS os setores)
| Código | Artigo | Descrição resumida |
|---|---|---|
| 1356 | Art. 155-A, I | Operações fora dos negócios usuais do cliente |
| 1357 | Art. 155-A, II | Origem/fundamentação econômica não aferível |
| 1358 | Art. 155-A, III | Incompatibilidade com patrimônio/capacidade financeira |
| 1359 | Art. 155-A, IV | Difícil identificação de beneficiário final |
| 1360 | Art. 155-A, V | PJ em jurisdição de alto risco (Gafi) |
| 1361 | Art. 155-A, VI | Países de tributação favorecida/regime fiscal privilegiado |
| 1362 | Art. 155-A, VII | Sócios/administradores em jurisdição de alto risco |
| 1363 | Art. 155-A, VIII | Resistência ao fornecimento de documentação |
| 1364 | Art. 155-A, IX | Informação/documentação falsa ou de difícil verificação |
| 1365 | Art. 155-A, X | Operações mais complexas/onerosas que o ordinário |
| 1366 | Art. 155-A, XI | Sinais de caráter fictício ou valores fora do mercado |
| 1367 | Art. 155-A, XII | Cláusulas com condições fora do mercado |
| 1368 | Art. 155-A, XIII | Tentativa de burlar controles (fracionamento, espécie) |
| 1369 | Art. 155-A, XIV | Documento estrangeiro de difícil compreensão jurídica |
| 1370 | Art. 155-A, XV | Ganho de capital substancial em curto período |
| 1373 | Art. 155-A, XVIII | Outras operações com sérios indícios de LD/FTP |
| 1374 | Art. 155-A, Par. único, I | Emprego não usual de meio de pagamento (ativo virtual, espécie) |
| 1375 | Art. 155-A, Par. único, II | Possível relação com terrorismo ou armas de destruição em massa |

### 13.2. Filtro por Tipo de Ato na Interface Desktop (`interface.py`)
- [x] Ao selecionar o tipo de ato (Escritura, Procuração, Protesto, PJ), filtrar automaticamente os artigos exibidos:
  - **Escritura** → Disposições Gerais + Tabelionato de Notas
  - **Procuração** → Disposições Gerais + Tabelionato de Notas
  - **Protesto** → Disposições Gerais + Tabelionato de Protesto
  - **Pessoa Jurídica** → Disposições Gerais + RCPJ
- [ ] Adicionar seção "Registro de Imóveis" como tipo de ato ou associar a um subtipo
- [x] Atualizar `_secao_situacoes_suspeitas()` para renderizar apenas os artigos do setor ativo
- [x] Manter agrupamento visual por setor com cabeçalho separador (ex.: "Disposições Gerais", "Artigos específicos - Tabelionato de Notas")

### 13.3. Filtro por Tipo de Ato na Interface Web (`index.html`)
- [x] Atualizar `onTipoAtoChange()` para também filtrar os artigos exibidos
- [x] Re-renderizar lista de suspeitas dinamicamente ao trocar o tipo de ato

### 13.4. Motor de Regras (`regras.py`)
- [x] Atualizar `aplicar_regras()` para considerar apenas os artigos visíveis no setor atual

### 13.5. Relatório PDF (`relatorio.py`)
- [x] Exibir apenas os artigos do setor selecionado no relatório
- [x] Adicionar seção "Setor/Serventia" no cabeçalho do relatório

### 13.6. Histórico
- [x] Garantir que análises salvas anteriormente (sem setor) continuem funcionando
- [x] Adicionar fallback: se não houver setor salvo, exibir todos os artigos (comportamento legado)

**Entregáveis:** Artigos filtrados dinamicamente por setor/serventia, exibindo apenas os relevantes + disposições gerais.
