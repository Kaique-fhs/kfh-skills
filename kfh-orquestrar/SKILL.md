---
name: kfh-orquestrar
description: Use proactively quando o trabalho tiver muitos arquivos, tarefas repetidas ou várias tarefas independentes (lote de PDFs, catalogar, converter, revisar N itens). Divide em lotes de até 10, despacha kfh-executor em paralelo, revisa com kfh-revisor, consolida com kfh-consolidador e reescreve o handoff. Não pergunta "subagente ou sequencial". Para plano de código com tarefas, delega ao subagent-driven-development. Roda só na sessão principal.
---

# kfh-orquestrar

Você coordena uma rodada de trabalho em lote. Você não executa itens: escreve pedidos, despacha, revisa, consolida e fecha. A situação vai sempre no pedido; os agentes são genéricos.

## Decidir o modo (sem perguntar)

- Lista de itens independentes (arquivos, registros, etapas repetidas) → **este procedimento**.
- Plano de código com tarefas (spec + plano do Superpowers) → skill `subagent-driven-development`; não duplique o processo dela.
- Uma única tarefa pequena, ou tarefas acopladas entre si → faça inline e diga em uma linha: "fiz inline porque <motivo>".

Nunca pergunte ao usuário qual modo usar.

## Procedimento

1. **Entender o pedido.** Objetivo; o que é "um item"; a Saída esperada **com um exemplo de uma linha preenchida**; o Marcador de vazio (padrão `não encontrado`); qual skill cada item usa. Se o pedido for vago, pergunte **uma vez, agora, tudo junto**. Depois disso você não pergunta mais: decide e registra no handoff.
2. **Preparar a rodada.** Crie `_rodadas/<AAAA-MM-DD-HHMM>/` na raiz do projeto com `pedidos/`, `relatorios/`, `revisoes/`. Leia `handoff.md` se existir e os ADRs do projeto: eles são regras críticas a repetir nos pedidos.
3. **Planejar os lotes.** No **máximo 10 itens por lote**, um `kfh-executor` por item. Modelo por item: o padrão do executor (Haiku) para volume; `model: sonnet` no despacho só quando o item exige julgamento. Se a rodada terá mais de **20 despachos**, diga em uma linha quantos serão e siga.
4. **Escrever um pedido por item** em `pedidos/<item>.md`, no formato abaixo. Repita nas Regras críticas as 2 ou 3 regras do CLAUDE.md e dos ADRs que importam para o item: subagente não herda a conversa.
5. **Despachar o lote em paralelo** (todos os `Agent` do lote na mesma mensagem), cada um com o conteúdo do pedido e o caminho do relatório em `relatorios/<item>.md`.
6. **Ler os status.** Itens `DONE_WITH_CONCERNS`, `BLOCKED` ou `NEEDS_CONTEXT`: leia o relatório você mesmo antes de revisar. `NEEDS_CONTEXT` que um arquivo do projeto responde → redespache com a resposta no pedido; que nenhum arquivo responde → anote em Dúvidas em aberto e marque o item `pendente humano`.
7. **Revisar o lote.** Um `kfh-revisor` por lote, com todos os pedidos e relatórios do lote e o caminho `revisoes/lote-<n>.md`.
8. **Retrabalho.** Achado **bloqueia** ou **corrigir** → redespache o item com o achado colado no pedido. **Até 3 tentativas** por item; na terceira falha o item fica marcado (`não encontrado` no campo, ou `pendente humano` no item) e a rodada segue. **sugestão** não gera retrabalho; vai para o handoff.
9. **Próximo lote**, até acabar.
10. **Consolidar.** Um `kfh-consolidador` com: objetivo, formato final, lista de artefatos aprovados, lista de itens marcados, caminho do relatório. Ele devolve o produto final, o `handoff.md` reescrito e `ADR proposto` (Fase 1 da `kfh-criar-adr`).
11. **ADRs.** Se vier `ADR proposto`, mostre o rascunho ao usuário e, após confirmação, faça você a **Fase 2** da `kfh-criar-adr` (gravar). Esta é a única pergunta do fluxo além da do passo 1.
12. **Fechar.** Resumo em poucas linhas: o que saiu e onde; itens marcados; quantos despachos e em quantos lotes; o que ficou em Dúvidas em aberto. Portão humano por padrão só aqui; portões intermediários (ex.: extrair → validar → consolidar) só quando o pedido os definir.

## Formato do pedido de despacho

```
# Pedido <item>
Tarefa: <uma frase: o que fazer com este item>
Item: <caminho ou identificador>
Contexto: <onde está, o que já existe, o que ler antes; nada além disso>
Skill: <nome da skill a invocar, ou "nenhuma">
Saída: <arquivo e formato, com UMA linha de exemplo preenchida>
Marcador de vazio: não encontrado
Critério de pronto: <como saber que terminou bem>
Não faça: <não resumir, não corrigir o autor, não tocar em outros arquivos, ...>
Relatório: _rodadas/<id>/relatorios/<item>.md
Regras críticas: <2-3 regras do CLAUDE.md e dos ADRs que valem para este item>
```

## Contrato de resposta dos subagentes

Todo subagente responde em no máximo 15 linhas com `Status: DONE | DONE_WITH_CONCERNS | BLOCKED | NEEDS_CONTEXT`, Produzido, Verificado, Preocupações e Relatório. O relatório completo fica no arquivo. Trate a resposta como afirmação; o revisor verifica.

## Guardrails desta skill

| Guardrail | Onde |
| --- | --- |
| Parada | `maxTurns: 50` no executor; 3 tentativas por item |
| Orçamento | aviso acima de 20 despachos; Haiku por padrão |
| Concorrência | `CLAUDE_CODE_MAX_CONCURRENT_SUBAGENTS=10` no harness; lotes de 10 aqui |
| Qualidade | revisor por lote; consolidação só com itens aprovados ou marcados |
| Portão humano | fechamento; intermediários só se pedidos |
| Permissões | revisor e analista só leitura; ninguém além da sessão despacha |
