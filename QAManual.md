# QA Manual — Analisador SISCOAF

## Erros encontrados

### Erro 1 — Conexão com Firestore (Firebase)

**Data:** 03/08/2026 20:20

**Fonte:** Console do navegador (`logger.ts:115`)

**Mensagem:**
```
@firebase/firestore: Firestore (10.8.1): WebChannelConnection RPC 'Listen' stream errored: [object Object]
@firebase/firestore: Firestore (10.8.1): Could not reach Cloud Firestore backend. Connection failed 1 times.
Most recent error: FirebaseError: [code=unavailable]: The operation could not be completed.
This typically indicates that your device does not have a healthy Internet connection at the moment.
The client will operate in offline mode until it is able to successfully connect to the backend.
```

**Observação:** O projeto não utiliza Firebase; erro provavelmente vindo de outra ferramenta/aba do navegador.

### Erro 2 — Barra de scroll ultrapassa o conteúdo

**Data:** 03/08/2026

**Plataforma:** Web (`index.html`)

**Descrição:** A barra de scroll vertical vai muito além do ponto onde as informações terminam, deixando um espaço em branco extenso no final da página.

**Área suspeita:** Layout CSS — `body { display: flex; min-height: 100vh; }`, `.main { flex: 1; display: flex; flex-direction: column; }` e `.content { flex: 1; overflow-y: auto; }` (linhas 28, 58-60, 76-78 do `index.html`). O elemento `.content` com `flex: 1` pode estar esticando o container além do conteúdo real.

### Erro 3 — Busca PEP por CPF em vez de nome completo

**Data:** 03/08/2026

**Plataforma:** Web (`index.html`)

**Descrição:** Ao buscar uma pessoa na base PEP, a consulta retorna resultado apenas quando há correspondência de CPF (6 dígitos centrais); buscar apenas pelo nome completo não retorna o PEP esperado.

**Área suspeita:** Função `consultarPEPLocal(nome, cpf)` (linhas 920-945 do `index.html`) — o filtro exigia `r.cpfFull` e, quando havia CPF com 6+ dígitos, comparava os dígitos centrais (`cpfLimpo.substring(3,9)`) com `r.cpfFull`, condicionando o resultado ao CPF. Na versão desktop, `pep_consulta.py` (`consultar_pep`, linhas 94-118) seguia padrão semelhante.

**Status:** CORRIGIDO em 03/08/2026.

**Regra esperada:** A busca deve priorizar o nome completo. O CPF deve ser usado apenas como filtro adicional quando informado — nunca como critério obrigatório/exclusivo. Ajustado em:
- `index.html` — `consultarPEPLocal`: filtro por nome agora é opcional-condicional (aplicado só quando o nome é informado) e a busca funciona também só com CPF.
- `pep_consulta.py` — `consultar_pep`: idem (aceita busca só por nome ou só por CPF, sem exigir ambos).

### Erro 4 — Tipos de escritura não aparecem ao abrir a página

**Data:** 03/08/2026

**Plataforma:** Web (`index.html`)

**Descrição:** Ao abrir a página "Nova Análise", os tipos de escritura (compra e venda, doação, permuta, etc.) não aparecem de imediato. É preciso trocar o tipo do ato para outra opção (Procuração, Protesto ou Pessoa Jurídica) e voltar para "Escritura" para que as opções apareçam.

**Área suspeita:** Função `init()` (linhas 640-650 do `index.html`) não chama `onTipoAtoChange()`. A seção `escrituraSection` inicia com `display:none` no HTML (linha 327) e a lista de checkboxes só é populada dentro de `onTipoAtoChange()` (linhas 690-730), que só dispara via evento `onchange` do select.


