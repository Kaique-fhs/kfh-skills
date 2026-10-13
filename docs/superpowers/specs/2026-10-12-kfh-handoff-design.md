# kfh-handoff-salvar e kfh-handoff-continuar — Design

**Data:** 12/10/2026
**Status:** Aprovado em conversa, aguardando revisão do texto

## 1. Objetivo

Trocar de chat sem perder contexto. Conversa é descartável, arquivo é permanente.

Duas skills, no padrão deste repositório (pasta por skill, `SKILL.md` em português, molde da `kfh-criar-adr`):

- **`kfh-handoff-salvar`**: ao encerrar uma sessão com tarefa pela metade, grava um arquivo de handoff no projeto, registra a tarefa como aberta no `CLAUDE.md` do projeto, garante um bloco de reflexo no `CLAUDE.md` global do usuário e commita.
- **`kfh-handoff-continuar`**: ao retomar, lê o handoff, confere o estado real do repositório e diz o próximo passo antes de agir. Quando a tarefa termina na sessão, encerra o ciclo: arquiva o handoff e apaga a linha do `CLAUDE.md`.

Resultado esperado: o `CLAUDE.md` do projeto mostra sempre o que começou e ainda não terminou.

## 2. Decisões de desenho

| Decisão | Escolha | Porquê |
|---|---|---|
| Quantos handoffs por projeto | Vários, um arquivo por tarefa | Mais de uma tarefa pode ficar aberta; a lista no `CLAUDE.md` é o índice |
| Ao terminar | Arquivar em `docs/handoff/concluidos/` | Mantém o histórico de como a tarefa foi conduzida |
| Quem encerra | Qualquer sessão que conclua e verifique a tarefa, guiada pela regra no `CLAUDE.md`; a `continuar` tem o passo explícito | A regra lida em toda sessão fecha o buraco de "ninguém percebeu que terminou" |
| Garantia do bloco global | A `salvar` e a `continuar` garantem o bloco a cada uso, idempotente | Não exige passo prévio obrigatório; funciona ao retomar em outra máquina |
| Terceira skill de configuração | Descartada | Não dá para obrigar a rodar antes; a garantia idempotente nas duas cobre o caso |
| Commit | Após confirmação do usuário, WIP permitido | Mesmo fluxo em duas fases da `kfh-criar-adr` |
| Spec e plano existentes | Referenciados, não copiados | Evita duplicação; o handoff guarda só o que não está lá |
| Script verificador | Descartado | Prosa basta; checklist no `SKILL.md` cobre |
| Push automático | Descartado | Fora do escopo; o usuário decide quando publicar |

## 3. Arquivos no projeto do usuário

```
docs/handoff/
  README_HANDOFF.md            copiado de references/ no primeiro uso
  TEMPLATE_HANDOFF.md          copiado de references/ no primeiro uso
  AAAA-MM-DD-<tema>.md         um por tarefa aberta
  concluidos/
    AAAA-MM-DD-<tema>.md       movido ao encerrar, mesmo nome
CLAUDE.md                      seção "## Em andamento (handoff)"
~/.claude/CLAUDE.md            bloco "## Handoff" (só no Claude Code)
```

**Nome do handoff:** `AAAA-MM-DD-<tema>.md`. A data é a de abertura e não muda ao atualizar. O tema usa minúsculas, sem acento, palavras separadas por traço, sem outro caractere (mesma regra do nome de arquivo dos ADRs). Exemplo: `2026-10-12-migrar-autenticacao-para-o-gateway.md`.

## 4. Conteúdo do handoff (`TEMPLATE_HANDOFF.md`)

```markdown
# Handoff - <Frase verbal imperativa: o que a tarefa entrega>

**Aberto em:** DD/MM/AAAA
**Atualizado em:** DD/MM/AAAA
**Branch:** <nome> | sem git
**Spec:** docs/superpowers/specs/<arquivo> | nenhuma
**Plano:** docs/superpowers/plans/<arquivo> | nenhum

## Objetivo e porquê
Uma ou duas frases. Com spec: só a frase e "detalhes na spec".

## Estado
- Feito: ...
- Pela metade: ... (o que já está e o que falta nesse item)
- Falta: ...
Com plano: por número de tarefa do plano ("tarefas 1 a 4 feitas, 5 pela metade").

## Decisões e porquês
- Decisão - porquê
- Descartado: alternativa - porquê
Com spec: só o que mudou ou foi decidido durante a execução, fora da spec.

## Onde está cada coisa
- caminho ou link - o que é

## Próximo passo
Um só, concreto, começando com verbo.

## Riscos e dúvidas abertas
- ...

## Como verificar
Comandos ou o que olhar para confirmar o estado descrito acima.

## Pendente de registro permanente
- o que - destino (CLAUDE.md, ADR, memória). Seção opcional: some quando vazia.
```

**Regras de conteúdo** (no README e na checklist da `salvar`):

- Cabe numa tela. O que já está na spec ou no plano é referenciado, não copiado.
- Próximo passo é um só. Se houver dois, o segundo vai para "Falta".
- "Pela metade" sempre diz o que já existe e o que falta naquele item.
- "Como verificar" traz comandos executáveis quando houver (testes, `git log`).
- Nada inventado: cada decisão e risco veio da conversa ou de resposta do usuário.
- Nenhum placeholder do template sobra (`<...>`, `DD/MM/AAAA`, `...`).

**`README_HANDOFF.md`**, no molde do `README_ADR.md`: o que é a pasta, quando abrir um handoff, ciclo de vida (abrir e atualizar com `kfh-handoff-salvar`, retomar e encerrar com `kfh-handoff-continuar`), convenção de nome, pasta `concluidos/`, a seção do `CLAUDE.md` como índice do que está aberto, e as regras de conteúdo acima.

## 5. Seção do `CLAUDE.md` do projeto

Texto exato, acrescentado ao final do arquivo precedido de linha em branco, ou como conteúdo único se o arquivo não existe. Nunca reescrever o restante do `CLAUDE.md`.

```markdown
## Em andamento (handoff)

Tarefas começadas e ainda não terminadas. Cada linha aponta para o handoff em `docs/handoff/`.

- Ao abrir uma sessão, leia a lista abaixo. Para continuar uma delas, use a skill `kfh-handoff-continuar`.
- Ao encerrar com tarefa pela metade, use `kfh-handoff-salvar` para criar ou atualizar o handoff e esta lista.
- Ao terminar e verificar uma tarefa da lista, na mesma sessão, mova o handoff para `docs/handoff/concluidos/` e apague a linha dela aqui.
- Nunca apague uma linha de tarefa que não está terminada e verificada.

Abertas:

- AAAA-MM-DD — <tarefa> — `docs/handoff/AAAA-MM-DD-<tema>.md`
```

- Uma linha por tarefa aberta, no formato `- AAAA-MM-DD — <título do handoff sem "Handoff - "> — ` seguido do caminho entre crases.
- A seção permanece mesmo sem tarefa aberta, com `- (nenhuma)` no lugar da lista, para as regras continuarem valendo.
- Se a seção já existe, só a lista é alterada: acrescentar, manter ou apagar linhas. O texto das regras não é reescrito.

## 6. Bloco global em `~/.claude/CLAUDE.md`

Texto exato e idêntico nos dois `SKILL.md`. Acrescentado ao final precedido de linha em branco; o arquivo é criado se não existe. Só quando a pasta `~/.claude` existe (Claude Code). Sem a pasta (app claude.ai), a skill avisa em uma linha e segue.

```markdown
## Handoff

- Se a conversa vai encerrar com tarefa pela metade, ou o usuário diz que vai trocar de chat, ofereça a skill `kfh-handoff-salvar` antes de terminar.
- Ao abrir sessão em projeto cujo `CLAUDE.md` tem `## Em andamento (handoff)` com tarefas abertas, diga quais são e ofereça `kfh-handoff-continuar`.
- Ao terminar e verificar uma tarefa dessa lista, encerre o handoff: mova para `docs/handoff/concluidos/` e apague a linha.
```

Idempotência: a skill procura o título `## Handoff`; se existe, não toca no arquivo.

## 7. `kfh-handoff-salvar`

**Estrutura da pasta:** `SKILL.md`, `references/README_HANDOFF.md`, `references/TEMPLATE_HANDOFF.md`.

**Gatilho (description):** "salva o handoff", "vou encerrar o chat", "escreve o HANDOFF", "guarda o estado para continuar depois", "vou trocar de chat", ou tarefa pela metade com a conversa chegando ao fim.

**Antes de começar:**

1. Localizar `docs/handoff/` na raiz do projeto. Se não existe, será criada na Fase 2 com `README_HANDOFF.md` e `TEMPLATE_HANDOFF.md` copiados de `references/` sem alteração.
2. Listar handoffs abertos (`docs/handoff/*.md`, exceto README, TEMPLATE e `concluidos/`). Se a tarefa atual já tem um, pelo tema ou pela linha no `CLAUDE.md`, é atualização do mesmo arquivo, não arquivo novo. Em dúvida, perguntar.
3. Procurar spec e plano da tarefa em `docs/superpowers/specs/` e `docs/superpowers/plans/`, pelo tema no nome do arquivo ou por terem sido citados na conversa. Se existem, o handoff referencia e não copia. Em dúvida sobre qual arquivo é o da tarefa, perguntar.
4. Conferir o estado real, não a memória da conversa: `git status`, `git branch`, testes se forem rápidos. Isso alimenta "Estado" e "Como verificar".
5. Conferir o `CLAUDE.md` do projeto: se falta a seção, será acrescentada; se falta a linha da tarefa, será acrescentada.
6. Conferir `~/.claude/CLAUDE.md` conforme a seção 6.

**Fase 1, rascunho.** Montar o arquivo a partir da conversa. Perguntar só o que falta, uma pergunta por vez: próximo passo se não estiver claro, riscos, alternativas descartadas. Nada inventado. Antes de apresentar, separar o permanente: decisão de arquitetura sugere ADR via `kfh-criar-adr`, regra de trabalho do projeto sugere `CLAUDE.md`, preferência do usuário sugere memória. Cada item entra em "Pendente de registro permanente" com o destino; a `salvar` não grava ADR, só aponta. Apresentar neste formato e parar:

```
Arquivo: docs/handoff/2026-10-12-migrar-autenticacao.md (novo | atualiza)
Pasta docs/handoff/: existe | será criada com README e TEMPLATE
CLAUDE.md do projeto: já tem seção e linha | receberá a seção | receberá a linha
~/.claude/CLAUDE.md: já tem bloco | receberá o bloco | sem ~/.claude, pulado
Commit: WIP: migrar autenticação (handoff) — inclui: <resumo do git status>

--- conteúdo do arquivo ---
<handoff completo>
--- fim ---

Leia e corrija. Posso gravar e commitar?
```

**Fase 2, gravação.** Só após confirmação explícita ("ok", "pode", "sim"). Pedido de ajuste não é confirmação: ajustar, reapresentar só o que mudou, esperar de novo. Ordem:

1. Criar `docs/handoff/` e copiar as referências, se faltar.
2. Gravar o handoff. Em atualização, "Aberto em" não muda e "Atualizado em" recebe a data de hoje.
3. Seção e linha no `CLAUDE.md` do projeto (seção 5).
4. Bloco global (seção 6).
5. Commit de tudo que está pendente no repositório. Mensagem `WIP: <tema> (handoff)`; sem o prefixo `WIP:` se o usuário disser que o código está estável. O arquivo global fica fora do repositório e não entra. Sem git: só grava e avisa.
6. Reportar: caminho do handoff, o que aconteceu com a pasta, com cada `CLAUDE.md` e com o commit.

**Checklist antes de gravar:** nome do arquivo na convenção; nenhum placeholder; próximo passo único; "pela metade" com o que existe e o que falta; spec e plano referenciados quando existem; linha do `CLAUDE.md` sem duplicata; bloco global idêntico ao texto da seção 6.

**Erros comuns** (tabela no `SKILL.md`): gravar sem rascunho; criar segundo arquivo para tarefa que já tem handoff; copiar a spec inteira em "Objetivo"; dois próximos passos; inventar risco plausível que ninguém disse; apagar linha de outra tarefa ao editar a lista; reescrever o resto do `CLAUDE.md`.

## 8. `kfh-handoff-continuar`

**Estrutura da pasta:** só `SKILL.md`.

**Gatilho (description):** "continua o handoff", "retoma de onde parou", "lê o HANDOFF", "o que ficou pendente", "terminei a tarefa do handoff", ou sessão aberta em projeto com tarefas em "Em andamento (handoff)".

**Antes de começar:**

1. Garantir o bloco global (seção 6), idempotente.
2. Ler a seção `## Em andamento (handoff)` do `CLAUDE.md` do projeto. Sem seção ou com `(nenhuma)`: dizer que não há handoff aberto e parar. Uma tarefa: é ela. Várias: listar e perguntar qual, salvo o pedido já nomear.
3. Se a linha aponta para arquivo que não existe: procurar em `docs/handoff/` e em `concluidos/`. Achou em `concluidos/`: a tarefa já foi encerrada; oferecer apagar a linha. Não achou: avisar e parar.

**Retomada, antes de agir:**

1. Ler o handoff inteiro. Se tem spec ou plano, ler os dois também.
2. Conferir o estado real contra o que o handoff diz: branch atual igual à registrada; `git status` e `git log` desde a data de atualização do handoff; existência dos arquivos em "Onde está cada coisa"; rodar o que está em "Como verificar". Sem git: só os arquivos e os comandos.
3. Relatar neste formato e parar:

```
Handoff: docs/handoff/2026-10-12-migrar-autenticacao.md (atualizado em 12/10/2026)
Spec/Plano: <caminhos> | nenhum
Confere: branch ok | 3 commits depois do handoff | testes 12/12
Diverge: <o que o handoff diz e o que o repositório mostra> | nada

Próximo passo do handoff: <copiado>
Proposta: <igual> | <ajustado, porquê>

Sigo com isso?
```

Divergência é informação, não erro: o relato mostra a diferença e propõe o que fazer. Só começa a executar após o "sim".

**Durante a sessão:** trabalhar normalmente. Se a conversa vai acabar com a tarefa ainda aberta, usar a `kfh-handoff-salvar`, que atualiza o mesmo arquivo e a mesma linha.

**Encerramento**, quando a tarefa fica pronta na sessão:

1. "Pronta" exige verificação: rodar "Como verificar" e os testes, com resultado mostrado, não afirmado. Se algo falha, não encerra.
2. Conferir "Pendente de registro permanente". Item pendente: perguntar se registra agora ou deixa. O encerramento não bloqueia por isso, mas o relato final lista o que ficou.
3. Mostrar o que vai acontecer e pedir confirmação: mover o arquivo para `docs/handoff/concluidos/` com o mesmo nome; apagar a linha no `CLAUDE.md`; manter a seção com `- (nenhuma)` se era a última; commit `Encerrar handoff: <tema>`.
4. Após o "sim", executar e reportar.

**Erros comuns:** agir antes do relatório; encerrar com teste falhando ou sem rodar; apagar a seção inteira do `CLAUDE.md` ao apagar a última linha; apagar o handoff em vez de mover; tratar divergência como erro e parar sem proposta.

## 9. Ambiente app claude.ai

As skills são enviadas por zip (`empacotar.py`). Nesse ambiente não há `~/.claude` nem, em geral, git, e os arquivos gravados podem ser descartados com o chat. Comportamento: bloco global pulado com aviso; commit pulado com aviso; a `salvar` mostra o handoff completo no chat e pede para baixar ou anexar ao próximo chat; a `continuar` aceita um handoff anexado ou apontado mesmo sem seção no `CLAUDE.md`, e o registra no projeto antes de seguir. Caminhos para `references/` são relativos à pasta da skill, como a nota já presente na `kfh-md-buscar`.

Acrescentado após a revisão final (12/10/2026): na `continuar`, a âncora dos commits "depois do handoff" é o último commit que tocou o arquivo do handoff, não a data do cabeçalho; "pronta" é definida como próximo passo feito, "Pela metade" e "Falta" vazios e verificação mostrada; código da tarefa não commitado recebe commit próprio antes do commit de encerramento, e o bloco de confirmação mostra isso.

## 10. Verificação antes de entregar

**Estrutural:** frontmatter YAML válido; `name` igual ao nome da pasta; description com os gatilhos; `references/` presente na `salvar` com os dois arquivos; texto do bloco global idêntico nos dois `SKILL.md`; `python empacotar.py <skill>` gera zip com `SKILL.md` e `references/`.

**Comportamental**, seguindo a `writing-skills`: cada cenário roda num repositório git descartável no scratchpad, com um subagente que recebe o `SKILL.md` e o pedido do usuário. O subagente é instruído a tratar uma pasta `home/.claude` do scratchpad como se fosse `~/.claude`, para não tocar no arquivo real. Esperado em cada cenário:

1. **Salvar, primeiro uso** (sem `docs/handoff/`, sem `CLAUDE.md`): rascunho apresentado e parada; após "sim", pasta com README e TEMPLATE, handoff sem placeholder, `CLAUDE.md` com seção e linha, bloco global, um commit WIP.
2. **Salvar, atualização** (handoff e linha existem): mesmo arquivo com "Atualizado em" novo, nenhuma linha duplicada, seção intacta.
3. **Salvar com spec e plano presentes:** campos Spec e Plano preenchidos, estado por número de tarefa, decisões só do que mudou.
4. **Continuar, uma tarefa aberta:** relatório confere/diverge e parada antes de agir.
5. **Continuar, divergência plantada** (branch diferente): divergência relatada, proposta ajustada, sem execução.
6. **Encerrar:** arquivo em `concluidos/`, linha apagada, seção mantida com `- (nenhuma)`, commit de encerramento. Variante com teste falhando: não encerra.
7. **Sem `~/.claude`:** as duas avisam e seguem.

## 11. Fora de escopo

Script verificador; integração automática com `kfh-criar-adr` (a `salvar` só aponta); push automático; terceira skill de configuração; renomear handoffs existentes.
