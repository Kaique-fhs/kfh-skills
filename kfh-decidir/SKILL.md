---
name: kfh-decidir
description: Use proactively quando houver uma decisão com trade-off, risco ou mais de uma opção razoável ("qual escolher", "vale a pena", "A ou B", decisão de arquitetura ou de regra). Despacha três kfh-analista independentes com lentes diferentes, sintetiza com dissidência registrada e grava a decisão como ADR. Níveis dia-a-dia (padrão) e caro. Roda só na sessão principal.
argument-hint: "[questão] [--nivel dia-a-dia|caro] [--lente extra]"
---

# kfh-decidir

Você conduz um conselho de decisão: três análises **independentes e em paralelo**, uma síntese que escolhe e registra quem discordou, e um ADR no fim. Não é debate: os analistas não conversam entre si, porque personas do mesmo modelo convergem cedo demais quando se leem. Esta skill roda **só na sessão principal** (subagente não despacha).

## Níveis

| Nível | Analistas (3, em paralelo) | Síntese (1) | Quando |
| --- | --- | --- | --- |
| `dia-a-dia` (padrão) | `kfh-analista` com `model: sonnet` | `kfh-analista` com `model: opus`, `effort: high` | qualquer decisão comum |
| `caro` | `kfh-analista` com `model: fable`, `effort: high` | `kfh-analista` com `model: fable`, `effort: max` | o usuário pediu, ou a decisão é irreversível, cara ou de arquitetura central |

Escolha `caro` por conta própria quando reconhecer um dos critérios, e diga em uma linha que escolheu. O modelo passado no despacho sobrepõe o do arquivo do analista.

## Lentes

Fixas, uma por analista: `viabilidade e custo` · `risco e falha` · `valor para quem usa`. Uma quarta lente de domínio pode vir do usuário em `--lente` (ex.: `rigor estatístico`); nesse caso são quatro analistas. Lente é um ângulo de análise, não uma posição a defender.

## Procedimento

1. **Enquadrar.** Questão em uma frase; opções conhecidas (se nenhuma, os analistas propõem); restrições; arquivos de contexto; nível. Se faltar o essencial, pergunte uma vez, tudo junto. Crie `_rodadas/<AAAA-MM-DD-HHMM>/analises/`.
2. **Despachar os analistas em paralelo** (todos na mesma mensagem). Cada pedido contém: a questão, as opções, o contexto, **a lente dele**, o nível, e o caminho `analises/<lente>.md`. Nenhum pedido contém a análise de outro analista.
3. **Sintetizar.** Um despacho de `kfh-analista` com lente `síntese`, modelo e esforço do nível, recebendo a questão e as três (ou quatro) análises. Saída fixa: Decisão · Alternativas descartadas e por quê · Dissidência · O que faria mudar a decisão · Confiança. **Não faça média**; escolha e diga o custo de estar errado. Grave em `analises/sintese.md`.
4. **Rodada adversarial, só se as recomendações dos analistas coincidirem** (a síntese diz isso em Dissidência). Um despacho a mais de `kfh-analista` com lente `derrube esta decisão`, mesmo modelo dos analistas, recebendo a síntese; grave em `analises/contra.md`. Depois redespache a síntese com o contra-argumento anexado; ela confirma ou revisa. Se houve dissidência, pule este passo.
5. **Registrar.** Invoque `kfh-criar-adr` com a síntese como material: Fase 1 (rascunho no chat) e, após a confirmação do usuário, Fase 2 (gravar). Esta é a única confirmação do fluxo.
6. **Responder** ao usuário em poucas linhas: a decisão, a dissidência em uma frase, o caminho do ADR e o custo da rodada (quantos despachos, em que nível).

## O que esta skill não faz

Não decide sozinha sem os analistas; não roda os analistas em sequência vendo a análise anterior; não grava ADR sem confirmação; não roda dentro de subagente.
