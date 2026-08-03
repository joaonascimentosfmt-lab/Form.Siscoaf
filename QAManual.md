# QA Manual — Analisador SISCOAF

Este documento descreve o checklist de teste manual da aplicação Analisador SISCOAF (desktop e web). Cada item deve ser validado nas duas plataformas quando aplicável.

## 1. Identificação do Atendimento

- [ ] Campo Funcionário é preenchido automaticamente com o nome do usuário logado
- [ ] Campos Protocolo, Ordem de serviço, Livro, Folha aceitam texto livre
- [ ] Campo "Data do Ato" preenchido no formato dd/mm/aaaa (se aplicável)

## 2. Partes

- [ ] Adicionar/remover partes dinamicamente
- [ ] Alternar PF/PJ altera a lista de documentações
- [ ] PF requer 7 docs; PJ 6 docs
- [ ] Consulta PEP automatizada com debounce (600ms)
- [ ] Campo representado/procuração funciona

## 3. PEP

- [ ] Selecionar Sim/Não
- [ ] Consulta PEP por Nome completo (partial match)

## 4. Dados do Ato

- [ ] Tipo do ato (Escritura/Procuração/Protesto/PJ)
- [ ] Subtipo e campo "outro" aparece quando aplicável
- [ ] Valor, forma de pagamento, cidade-estado e data do ato

## 5. Pagamento

- [ ] Forma de pagamento selecionável (PIX/TED/Dinheiro/Cheque/Boleto/outro)

## 6. Suspeitas

- [ ] 30 indicadores listados
- [ ] Marcação Sim/Não e contador de suspeitas atualizado

## 7. Resultado da análise

- [ ] Pontuação calculada corretamente segundo critérios
- [ ] Resultado da decisão: COMUNICAR / ANALISAR / NÃO COMUNICAR

## 8. Lógica de decisão

- Aplicação da lógica:
  - Qualquer item objetiva marcado -> COMUNICAR
  - Item de atenção/suspeita marcado -> ANALISAR
  - Nenhum -> NÃO COMUNICAR / ISENTA

## 9. Histórico

- [ ] Salvar análise no banco
- [ ] Buscar/listar análises
- [ ] Carregar restaura formulário

## 10. Relatório PDF

- [ ] Geração PDF via ReportLab/print-to-PDF
- [ ] Seções: identificação, partes, PEP, características, pagamento, suspeitas, justificativa

## 11. Configurações

- [ ] Scoring/limites configuráveis
- [ ] Export/Import JSON
- [ ] Cadastro de tipo de serviço e regras

## 12. Web

- [ ] admin.html dashboard KPIs/gráficos
- [ ] index.html formulário opera sobre localStorage
- [ ] Regras JavaScript web equivalentes às do backend Python

---
