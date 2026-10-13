---
name: kfh-handoff-salvar
description: Use quando o usuário vai encerrar ou trocar de chat com uma tarefa pela metade e precisa que outra sessão continue de onde parou. Aciona em "salva o handoff", "escreve o HANDOFF", "vou encerrar o chat", "vou trocar de chat", "guarda o estado para continuar depois", ou quando a conversa está chegando ao fim com trabalho não terminado. Também para atualizar um handoff já aberto.
---

# kfh-handoff-salvar — Versão 1.0

Você grava o estado de uma tarefa não terminada num arquivo de handoff, para que outra sessão continue de onde parou. Conversa é descartável, arquivo é permanente. O padrão do arquivo é o de `references/TEMPLATE_HANDOFF.md` e as regras são as de `references/README_HANDOFF.md`. Leia os dois antes de escrever qualquer coisa. Você trabalha em duas fases: primeiro apresenta o rascunho completo no chat, depois, só após confirmação explícita, grava e commita.

No app claude.ai (skill enviada por zip) a variável `${CLAUDE_SKILL_DIR}` não existe: `references/` é a pasta dentro desta skill; use o caminho relativo.

Idioma: português com acentos.

## Antes de começar

1. **Localize `docs/handoff/`** a partir da raiz do projeto. Se não existe, você vai criá-la na Fase 2 com `README_HANDOFF.md` e `TEMPLATE_HANDOFF.md` copiados de `references/` sem alteração.
2. **Liste os handoffs abertos:** `docs/handoff/*.md`, exceto `README_HANDOFF.md`, `TEMPLATE_HANDOFF.md` e a pasta `concluidos/`. Se a tarefa desta conversa já tem um handoff, pelo tema ou pela linha no `CLAUDE.md`, você vai atualizar esse arquivo, não criar outro. Em dúvida, pergunte.
3. **Procure spec e plano da tarefa** em `docs/superpowers/specs/` e `docs/superpowers/plans/`, pelo tema no nome do arquivo ou por terem sido citados na conversa. Se existem, o handoff referencia e não copia. Se as pastas não existem, os campos ficam `nenhuma` e `nenhum`, sem perguntar. Em dúvida sobre qual arquivo é o da tarefa, pergunte.
4. **Confira o estado real, não a memória da conversa:** `git status --short`, `git branch --show-current`, `git log --oneline -5`, e os testes do projeto se rodam em menos de um minuto. Isso alimenta "Estado" e "Como verificar". Sem git: liste os arquivos tocados na sessão.
5. **Confira o `CLAUDE.md` do projeto.** Se não existe, será criado só com o bloco de "Seção do CLAUDE.md do projeto". Se existe e não tem `## Em andamento (handoff)`, a seção será acrescentada ao final. Se tem, só a lista `Abertas:` muda: a linha desta tarefa é acrescentada se falta. Nunca reescreva o resto do arquivo nem as linhas de outras tarefas.
6. **Confira `~/.claude/CLAUDE.md`.** Se a pasta `~/.claude` existe e o arquivo não contém o título `## Handoff`, o bloco de "Bloco do CLAUDE.md global" será acrescentado ao final na Fase 2, criando o arquivo se preciso. Se já contém, não toque. Se a pasta `~/.claude` não existe (app claude.ai), avise em uma linha e siga. Não crie outro arquivo ou pasta em `~/.claude`: o bloco é o único registro global.

## Fase 1 — Rascunho

Monte o handoff a partir do que a conversa já tem, seguindo o template seção por seção. Para o que faltar, pergunte, uma pergunta por vez, e só o que falta:

- **Próximo passo:** se a conversa não deixa claro qual é o único próximo passo concreto.
- **Riscos e dúvidas abertas:** se nada foi dito, pergunte "há risco ou dúvida que o próximo chat precisa saber?". Se o usuário disser que não, a seção fica com `- nenhum registrado`.
- **Descartado:** se houve decisão mas as alternativas não aparecem na conversa, pergunte. Não invente alternativas nem riscos.

Não pergunte o que já está na conversa. Não pergunte por nome de arquivo, data ou mensagem de commit: isso você propõe. Se não pode perguntar (sem resposta do usuário), deixe a seção com `- não informado` em vez de preencher por conta própria.

**Separe o que é permanente.** Antes de apresentar, percorra as decisões e marque as que não devem morrer com o handoff:

- decisão de arquitetura, trade-off ou regra de negócio: destino ADR, via skill `kfh-criar-adr`;
- regra de como trabalhar neste projeto: destino `CLAUDE.md` do projeto;
- preferência do usuário que vale em todo projeto: destino memória.

Cada uma entra em "Pendente de registro permanente" com o destino. Esta skill não grava ADR nem memória; só aponta. Se o usuário quiser registrar agora, faça depois da gravação do handoff, com a skill certa.

Apresente neste formato, e pare. "O pedido era claro" não dispensa o rascunho: o usuário lê por trinta segundos e corrige antes de qualquer gravação.

```
Arquivo: docs/handoff/2026-10-12-migrar-autenticacao-para-o-gateway.md (novo | atualiza)
Pasta docs/handoff/: existe | será criada com README_HANDOFF.md e TEMPLATE_HANDOFF.md
CLAUDE.md do projeto: já tem seção e linha | será criado com a seção | receberá a seção | receberá a linha
~/.claude/CLAUDE.md: já tem o bloco | receberá o bloco | sem ~/.claude, pulado
Commit: WIP: migrar autenticação (handoff) — inclui: <resumo do git status> | sem git, pulado

--- conteúdo do arquivo ---
<handoff completo, pronto para gravar>
--- fim ---

Leia e corrija. Posso gravar e commitar?
```

Regras do conteúdo:

- **Título:** `# Handoff - <Frase verbal imperativa: o que a tarefa entrega>`. Ex.: "Migrar autenticação para o gateway".
- **Nome do arquivo:** `AAAA-MM-DD-` seguido do título em minúsculas, sem acentos, palavras separadas por traço, sem outro caractere. A data é a de hoje para arquivo novo; em atualização, o nome não muda.
- **Cabeçalho:** cinco linhas em negrito, nesta ordem, sem lista: `**Aberto em:**` e `**Atualizado em:**` em DD/MM/AAAA; `**Branch:**` com o nome ou `sem git`; `**Spec:**` com o caminho ou `nenhuma`; `**Plano:**` com o caminho ou `nenhum`.
- **Seções e ordem:** `## Objetivo e porquê`, `## Estado`, `## Decisões e porquês`, `## Onde está cada coisa`, `## Próximo passo`, `## Riscos e dúvidas abertas`, `## Como verificar`, e `## Pendente de registro permanente` só se houver item. Sem subseções `###` e sem seções extras.
- **Com spec:** "Objetivo e porquê" é uma frase mais "detalhes na spec"; "Decisões e porquês" traz só o que mudou ou foi decidido durante a execução, fora da spec.
- **Com plano:** "Estado" fala por número de tarefa do plano: "tarefas 1 a 4 feitas, 5 pela metade: ...".
- **Estado:** três marcas, `Feito`, `Pela metade`, `Falta`. "Pela metade" diz o que já existe e o que falta naquele item. Marca sem conteúdo recebe `nada`. "Falta" lista só o que o usuário pediu ou aprovou; trabalho que você acha que deveria existir, mas ninguém pediu, vai para "Riscos e dúvidas abertas" como dúvida.
- **Decisões:** `Decisão - porquê`; descartadas como `Descartado: alternativa - porquê`.
- **Onde está cada coisa:** `caminho ou link - o que é`, incluindo a branch e os arquivos tocados nesta sessão.
- **Próximo passo:** um só, concreto, começando com verbo. Se houver dois, o segundo vai para "Falta". Lista numerada aqui é erro.
- **Como verificar:** comandos executáveis quando houver (testes, `git log`, `git status`) e o resultado esperado de cada um.
- **Tamanho:** cabe numa tela. Se passa, está copiando o que a spec ou o plano já dizem.

## Fase 2 — Gravação

Só comece após o usuário confirmar o rascunho de forma explícita ("ok", "pode", "sim"). Pedido de ajuste não é confirmação: ajuste, reapresente só o que mudou, e espere de novo.

1. Se `docs/handoff/` não existe, crie e copie `references/README_HANDOFF.md` e `references/TEMPLATE_HANDOFF.md` para lá, com o mesmo nome e conteúdo.
2. Grave o handoff com o conteúdo confirmado. Em atualização, `Aberto em` não muda e `Atualizado em` recebe a data de hoje.
3. Garanta o `CLAUDE.md` do projeto conforme o item 5 de "Antes de começar", com a linha no formato de "Seção do CLAUDE.md do projeto".
4. Garanta o `~/.claude/CLAUDE.md` conforme o item 6.
5. Commit, se há git: `git add -A` e `git commit -m "WIP: <tema> (handoff)"`. Sem o prefixo `WIP:` só se o usuário disser que o código está estável. O arquivo global fica fora do repositório e não entra no commit. Sem git: avise que não houve commit.
6. Reporte: caminho do handoff, o que aconteceu com a pasta, com cada `CLAUDE.md` e com o commit (hash), e o que ficou em "Pendente de registro permanente".
7. **Sem git e sem `~/.claude` (app claude.ai):** os arquivos gravados podem ser descartados com o chat. No reporte, mostre o conteúdo completo do handoff num bloco de código e diga ao usuário para baixar o arquivo ou anexá-lo ao próximo chat, onde a `kfh-handoff-continuar` o aceita mesmo sem `CLAUDE.md`.

### Seção do CLAUDE.md do projeto

Use exatamente este bloco, precedido de uma linha em branco quando acrescentado a um arquivo existente. A linha de exemplo da lista é substituída pela linha real da tarefa.

```markdown
## Em andamento (handoff)

Tarefas começadas e ainda não terminadas. Cada linha aponta para o handoff em `docs/handoff/`.

- Ao abrir uma sessão, leia a lista abaixo. Para continuar uma delas, use a skill `kfh-handoff-continuar`.
- Ao encerrar com tarefa pela metade, use `kfh-handoff-salvar` para criar ou atualizar o handoff e esta lista.
- Ao terminar e verificar uma tarefa da lista, na mesma sessão, mova o handoff para `docs/handoff/concluidos/` e apague a linha dela aqui.
- Nunca apague uma linha de tarefa que não está terminada e verificada.

Abertas:

- 2026-10-12 — Migrar autenticação para o gateway — `docs/handoff/2026-10-12-migrar-autenticacao-para-o-gateway.md`
```

- Uma linha por tarefa aberta: `- AAAA-MM-DD — <título sem "Handoff - "> — ` e o caminho entre crases. A data é a de abertura.
- Se a lista está em `- (nenhuma)`, substitua essa linha pela linha da tarefa.
- Se a seção já existe, só a lista muda. As regras não são reescritas.

### Bloco do CLAUDE.md global

Use exatamente este bloco em `~/.claude/CLAUDE.md`, precedido de uma linha em branco quando acrescentado a um arquivo existente:

```markdown
## Handoff

- Se a conversa vai encerrar com tarefa pela metade, ou o usuário diz que vai trocar de chat, ofereça a skill `kfh-handoff-salvar` antes de terminar.
- Ao abrir sessão em projeto cujo `CLAUDE.md` tem `## Em andamento (handoff)` com tarefas abertas, diga quais são e ofereça `kfh-handoff-continuar`.
- Ao terminar e verificar uma tarefa dessa lista, encerre o handoff: mova para `docs/handoff/concluidos/` e apague a linha.
```

## Checklist antes de gravar

- Arquivo em `docs/handoff/`, nome `AAAA-MM-DD-tema.md`, minúsculas, sem acento, só traços.
- Tarefa que já tinha handoff: mesmo arquivo, `Aberto em` preservado.
- Cabeçalho com as cinco linhas; `Spec` e `Plano` preenchidos quando os arquivos existem.
- Sete seções na ordem, mais a oitava só se há item.
- Nenhum placeholder do template sobrou (`<...>`, `DD/MM/AAAA`, `...`).
- Um só próximo passo. "Pela metade" com o que existe e o que falta.
- Nenhuma decisão, alternativa, risco ou item de "Falta" inventado.
- "Como verificar" com comando e resultado esperado.
- Linha no `CLAUDE.md` do projeto sem duplicata; linhas de outras tarefas e resto do arquivo intactos.
- Bloco global idêntico ao desta skill; `~/.claude/CLAUDE.md` não reescrito; nada mais criado em `~/.claude`.

## Erros comuns

| Erro | Correto |
|------|---------|
| Gravar direto porque "o pedido já tinha tudo" | Rascunho no chat primeiro, sempre |
| `HANDOFF.md` na raiz do projeto | `docs/handoff/AAAA-MM-DD-tema.md` |
| Ponteiro ou cópia em `~/.claude/handoffs/` | Só o bloco `## Handoff` em `~/.claude/CLAUDE.md` |
| Segundo arquivo para tarefa que já tem handoff | Atualizar o mesmo arquivo |
| Copiar a spec inteira em "Objetivo e porquê" | Uma frase e "detalhes na spec" |
| "Próximo passo: 1. terminar X 2. testar 3. commitar" | Um passo; o resto vai para "Falta" |
| "Pela metade: módulo de auth" | "Pela metade: módulo de auth - login feito, refresh de token falta" |
| "Falta: adicionar teste de divisor zero" que ninguém pediu | Dúvida em "Riscos e dúvidas abertas" |
| Risco plausível que ninguém disse | Perguntar; registrar só o confirmado |
| Estado tirado da memória da conversa | `git status` e testes rodados antes do rascunho |
| Reescrever o `CLAUDE.md` ou apagar linha de outra tarefa | Só acrescentar a linha desta tarefa |
| Parar porque não há `~/.claude` | Avisar em uma linha e seguir |
| Sem git: gravar, relatar o caminho e encerrar | Mostrar o handoff inteiro no chat e pedir para baixar ou anexar |
