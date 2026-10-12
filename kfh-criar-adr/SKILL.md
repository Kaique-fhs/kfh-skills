---
name: kfh-criar-adr
description: Use quando o usuário pedir para criar, registrar ou escrever uma ADR (Architecture Decision Record), documentar uma decisão de arquitetura, ou emendar uma ADR existente com adendo, errata ou "emendada por". Também quando uma decisão com trade-off, risco, IA ou regra de negócio surgir na conversa e precisar ficar registrada.
---

# kfh-criar-adr — Versão 1.0

Você cria e emenda ADRs no padrão fixo deste usuário. O padrão é o de `references/TEMPLATE_ADR.md` e as regras são as de `references/README_ADR.md`. Leia os dois antes de escrever qualquer coisa. Você trabalha em duas fases: primeiro propõe o rascunho completo no chat, depois, só após confirmação explícita, grava os arquivos.

Idioma do ADR: português normal, com acentos, no título e no texto das seções. Ficam sem acento apenas três coisas: os títulos de seção, exatamente como no template (`Decisao`, `Consequencias`, `Referencias`); o nome do arquivo; e a linha da convenção de nome em Referencias, copiada do template.

## Antes de começar

1. **Localize a pasta de ADRs.** É sempre `docs/ams/adr/` a partir da raiz do projeto. Não procure outra pasta, não use `docs/adr/`, `adr/` nem `AMS/adr/`. Se a pasta não existe, você vai criá-la na Fase 2 junto com `README_ADR.md` e `TEMPLATE_ADR.md`, copiados sem alteração de `references/`.
2. **Liste os ADRs existentes** (`ADR-NNN-*.md`). O próximo número é o maior NNN existente mais um, sempre com três dígitos. Se a pasta está vazia ou não existe, o número é `001`. Ignore arquivos que não sigam `ADR-NNN-`; nunca renomeie nem renumere ADR existente, e nunca use a série `ADR-LOCAL-*`.
3. **Leia os ADRs que o assunto toca.** Se a decisão nova altera, contradiz ou estende um ADR existente, você precisa citá-lo em Referencias e, na Fase 2, marcar o antigo como emendado.
4. **Verifique o `CLAUDE.md` na raiz do projeto.** Se não existe, você vai criá-lo na Fase 2 só com a seção de "Seção do CLAUDE.md". Se existe, leia-o: se já contém um título `## ADRs`, não mexa; se não contém, você vai acrescentar a seção ao final na Fase 2. Nunca reescreva conteúdo existente do `CLAUDE.md`.
5. **Confirme que precisa de ADR.** Crie só se a decisão atende pelo menos um critério do README: decisão arquitetural relevante, trade-off, impacto no comportamento do sistema, ou risco / IA / regra de negócio. Se não atende a nenhum, diga qual critério falta e sugira outro destino (comentário no código, doc, issue). Se o usuário insistir, crie.

## Fase 1 — Rascunho

Monte o ADR a partir do que a conversa já tem. Para cada seção, se faltar o essencial, pergunte, uma pergunta por vez, e só o que falta:

- **Contexto:** qual é o problema, dor, risco ou limitação que forçou a decisão.
- **Decisao:** o que foi decidido. Se o usuário usou "estamos pensando", "talvez", pergunte se já é decisão fechada.
- **Alternativas consideradas:** quais opções foram descartadas e por quê. Se o usuário não citou nenhuma, pergunte. Não invente alternativas.
- **Consequencias:** impactos positivos e negativos. Se o usuário citou só positivos, pergunte pelos negativos ou custos. Não invente impactos; se o usuário disser que não há negativos, registre apenas os positivos.

Não pergunte o que já está na conversa. Não pergunte por título, número, nome de arquivo, status ou data: isso você propõe.

Apresente o rascunho neste formato, e pare:

```
Número: ADR-007
Arquivo: docs/ams/adr/ADR-007-usar-postgresql-no-modulo-de-pedidos.md
Emenda: ADR-003 (recebe `Emendada por: ADR-007`)   <- só se houver
Pasta docs/ams/adr/: existe | será criada com README_ADR.md e TEMPLATE_ADR.md
CLAUDE.md: já tem seção ADRs | será criado | receberá a seção ADRs

--- conteúdo do arquivo ---
<ADR completo, pronto para gravar>
--- fim ---

Posso gravar?
```

Regras do conteúdo:

- **Título:** `# ADR-NNN - <Frase verbal imperativa no presente>`. Verbo no imperativo primeiro: "Usar PostgreSQL no modulo de pedidos", "Centralizar o escopo de autenticacao no gateway". Nunca substantivo ("Banco de dados do modulo de pedidos") nem particípio ("PostgreSQL adotado").
- **Nome do arquivo:** `ADR-NNN-` seguido do título em minúsculas, sem acentos, palavras separadas por traço, sem outro caractere. Ex.: `ADR-007-usar-postgresql-no-modulo-de-pedidos.md`.
- **Cabeçalho:** duas linhas em negrito, nesta ordem, sem lista: `**Status:** Aceito` e `**Data:** DD/MM/AAAA` (data de hoje). Status é `Aceito` salvo o usuário pedir `Proposto`, `Substituido` ou `Depreciado`. Não inclua o comentário HTML do template no ADR gerado.
- **Seções e ordem:** `## Contexto`, `## Decisao`, `## Consequencias`, `## Alternativas consideradas`, `## Referencias`, todas presentes, separadas por uma linha `---`. Sem subseções `###` e sem seções extras.
- **Tamanho:** curto e direto. Contexto e Decisao em uma ou duas frases mais marcas; o resto em marcas de uma linha. Se o ADR passa de uma tela, está longo.
- **Decisao sem ambiguidade:** uma regra ou comportamento por marca. Se existe contrato, limite ou responsabilidade, nomeie.
- **Alternativas:** cada marca é `Alternativa - por que nao foi escolhida`.
- **Referencias:** outros ADRs citados por número e nome de arquivo (`ADR-003-...md`), docs e links da conversa. A última marca é sempre a linha da convenção de nome do template, copiada sem alteração.

## Fase 2 — Gravação

Só comece após o usuário confirmar o rascunho de forma explícita ("ok", "pode gravar", "sim"). Pedido de ajuste não é confirmação: ajuste, reapresente só o que mudou, e espere de novo.

1. Se `docs/ams/adr/` não existe, crie e copie `references/README_ADR.md` e `references/TEMPLATE_ADR.md` para lá, com o mesmo nome e conteúdo.
2. Releia a listagem da pasta. Se o número proposto já existe, use o próximo livre e avise.
3. Grave o ADR com o conteúdo confirmado.
4. Se o ADR emenda outro, abra o antigo e insira `**Emendada por:** ADR-NNN` na linha imediatamente acima de `**Status:**`. Se já existe uma linha `Emendada por`, acrescente o novo número separado por vírgula na mesma linha. Não altere mais nada no antigo.
5. Garanta o `CLAUDE.md` conforme o item 4 de "Antes de começar": crie, ou acrescente a seção ao final, ou não toque.
6. Reporte: caminho do ADR, ADR antigo alterado (se houve), e o que aconteceu com a pasta e com o `CLAUDE.md`.

### Seção do CLAUDE.md

Use exatamente este bloco, precedido de uma linha em branco quando acrescentado a um arquivo existente:

```markdown
## ADRs (Architecture Decision Records)

As decisões de arquitetura deste projeto ficam em `docs/ams/adr/`.

- Antes de propor ou implementar qualquer mudança de arquitetura, comportamento
  do sistema, regra de negócio ou uso de IA, leia os ADRs relevantes em
  `docs/ams/adr/` e respeite o que foi decidido.
- Não contrarie um ADR aceito sem registrar um novo ADR que o emende.
- Para criar ou emendar um ADR, use a skill `kfh-criar-adr`. O padrão está em
  `docs/ams/adr/README_ADR.md` e `docs/ams/adr/TEMPLATE_ADR.md`.
```

## Emendar um ADR existente

Quando o pedido é acrescentar algo a um ADR já gravado, sem decisão nova:

- **Adendo:** informação ou esclarecimento acrescentado depois, que não muda a decisão.
- **Errata:** correção de erro de fato ou de texto no ADR.

Se o pedido muda a decisão em si, não é adendo nem errata: é um ADR novo que emenda o antigo (fluxo acima).

Mesmo fluxo em duas fases. No rascunho, mostre o arquivo alvo e o bloco a acrescentar. Na gravação, acrescente ao final do arquivo, depois do último conteúdo, neste formato, com data na mesma convenção já usada no arquivo:

```markdown

---

## Adendo - DD/MM/AAAA
<texto curto do que foi acrescentado e por quê>
```

Errata é igual, com `## Errata - DD/MM/AAAA` e texto do que estava errado e a correção. O texto traz só o fato e a correção, em uma ou duas frases; nada sobre o processo ("o original permanece inalterado", "esta errata registra"). Um ADR pode ter vários adendos e erratas; cada um é uma seção nova ao final, em ordem cronológica. Nunca edite o texto original das seções do ADR para "corrigir" em vez de registrar errata.

## Checklist antes de gravar

- Arquivo em `docs/ams/adr/`, nome `ADR-NNN-frase-verbal-imperativa.md`, minúsculas, sem acento, só traços.
- Número com três dígitos, sem colisão com arquivo existente.
- Título com verbo no imperativo. `**Status:**` e `**Data:**` em DD/MM/AAAA.
- Cinco seções, nessa ordem, sem acento nos títulos, separadas por `---`.
- Nenhum placeholder do template sobrou (`XXX`, `DD/MM/AAAA`, `<...>`, "Alternativa 1").
- Nenhuma alternativa ou consequência inventada; cada uma veio da conversa ou de resposta do usuário.
- Última marca de Referencias é a linha da convenção de nome.
- `README_ADR.md`, `TEMPLATE_ADR.md` e seção do `CLAUDE.md` garantidos.

## Erros comuns

| Erro | Correto |
|------|---------|
| `docs/adr/0001-postgresql-pedidos.md` | `docs/ams/adr/ADR-001-usar-postgresql-no-modulo-de-pedidos.md` |
| `# ADR 0001: PostgreSQL para pedidos` | `# ADR-001 - Usar PostgreSQL no modulo de pedidos` |
| `- **Status:** Aceita` / `2026-10-12` | `**Status:** Aceito` / `**Data:** 12/10/2026` |
| `## Decisão`, `## Consequências` | `## Decisao`, `## Consequencias` |
| Alternativas antes de Consequencias, ou `### MongoDB` | Ordem do template, uma marca por alternativa |
| Gravar direto porque "o pedido já tinha tudo" | Rascunho no chat primeiro, sempre |
| Preencher consequências negativas plausíveis que ninguém disse | Perguntar; registrar só o que o usuário confirmou |
| Renomear ADR antigo para seguir a regra de nome | Nunca renomear; só o novo segue a regra |
| Corrigir texto de ADR antigo no lugar | Registrar `## Errata` ao final |
