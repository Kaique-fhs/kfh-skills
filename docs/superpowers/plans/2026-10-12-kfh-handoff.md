# kfh-handoff-salvar e kfh-handoff-continuar — Plano de implementação

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Duas skills em prosa, `kfh-handoff-salvar` e `kfh-handoff-continuar`, que gravam e retomam o estado de tarefas pela metade entre chats, com registro do que está aberto no `CLAUDE.md` do projeto.

**Architecture:** Cada skill é uma pasta com `SKILL.md` em português no molde da `kfh-criar-adr` (duas fases: rascunho no chat, gravação após confirmação). A `salvar` carrega `references/README_HANDOFF.md` e `references/TEMPLATE_HANDOFF.md`, copiados para `docs/handoff/` do projeto no primeiro uso. Não há código: a verificação é por cenários rodados com subagentes num repositório git descartável, seguindo a `writing-skills` (baseline sem a skill, depois com a skill).

**Tech Stack:** Markdown; git; Python 3 só para `empacotar.py` e para o projeto de brinquedo dos cenários (pytest).

**Spec:** `docs/superpowers/specs/2026-10-12-kfh-handoff-design.md`

## Global Constraints

- Idioma dos arquivos: português com acentos, como as demais skills do repositório.
- Frontmatter com `name` igual ao nome da pasta e `description` começando com "Use quando", só gatilhos, sem resumo do procedimento, abaixo de 1024 caracteres.
- Texto do bloco `## Handoff` do `~/.claude/CLAUDE.md` idêntico, byte a byte, nos dois `SKILL.md`.
- Texto da seção `## Em andamento (handoff)` do `CLAUDE.md` do projeto conforme a spec, seção 5.
- Nome de handoff: `AAAA-MM-DD-<tema>.md`, minúsculas, sem acento, só traços.
- Nenhum cenário de teste toca no `~/.claude/CLAUDE.md` real: o subagente trata uma pasta `home/.claude` do scratchpad como se fosse `~/.claude`.
- Scratchpad desta sessão: `C:/Users/KAIQUE~1.SOU/AppData/Local/Temp/claude/C--Users-kaique-souza-Desktop-kfh-harness-kfh-skills/cb15d144-368c-4b95-96a5-18f651f1dded/scratchpad`. Nos passos abaixo, `$S` é esse caminho, e `<repo>` é `C:/Users/kaique.souza/Desktop/kfh-harness/kfh-skills`.
- Commits pequenos, mensagens no estilo do histórico (`kfh-handoff-salvar: ...`), terminando com `Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>`.

## Review Focus

1. `CLAUDE.md` do projeto já existe com outras seções e outra tarefa aberta: a `salvar` acrescenta só a linha nova; nada mais muda. Teste no cenário 2 da Tarefa 4.
2. Projeto sem `docs/superpowers/`: campos `Spec` e `Plano` ficam `nenhuma` / `nenhum`, sem a skill perguntar por eles. Teste no cenário 1 da Tarefa 4.
3. Árvore limpa exceto o handoff e o `CLAUDE.md`: o commit acontece mesmo assim. Teste no cenário 2 da Tarefa 4.
4. Comando de "Como verificar" falha na retomada: a `continuar` relata como divergência e propõe, não trava nem conserta por conta própria. Teste no cenário 5 da Tarefa 7.
5. Linha do `CLAUDE.md` aponta para arquivo que já está em `concluidos/`: a `continuar` diz que a tarefa foi encerrada e oferece apagar a linha. Teste no cenário 8 da Tarefa 7.

---

### Tarefa 1: Fixture dos cenários e baseline da `salvar` (RED)

**Files:**
- Create: `$S/preparar_fixture.sh` (fora do projeto)
- Create: `$S/baseline-salvar.md` (anotações, fora do projeto)

**Interfaces:**
- Produces: o script `preparar_fixture.sh <nome>` cria `$S/<nome>/projeto` (repositório git com projeto Python meio pronto) e `$S/<nome>/home/.claude/` vazia. As Tarefas 4, 5 e 7 chamam esse script.

- [ ] **Passo 1: Escrever o script da fixture**

Gravar `$S/preparar_fixture.sh`:

```bash
#!/usr/bin/env bash
# Uso: bash preparar_fixture.sh <nome>
# Cria $S/<nome>/projeto (git, projeto Python pela metade) e $S/<nome>/home/.claude/
set -e
S="$(cd "$(dirname "$0")" && pwd)"
RAIZ="$S/$1"
rm -rf "$RAIZ"
mkdir -p "$RAIZ/projeto" "$RAIZ/home/.claude"
cd "$RAIZ/projeto"
git init -q -b main
git config user.email "teste@exemplo.com"
git config user.name "Teste"

cat > calc.py <<'PY'
def somar(a, b):
    return a + b


def dividir(a, b):
    raise NotImplementedError("pela metade")
PY

cat > test_calc.py <<'PY'
from calc import somar, dividir


def test_somar():
    assert somar(2, 3) == 5


def test_dividir():
    assert dividir(6, 3) == 2
PY

git add -A
git commit -q -m "inicio: somar pronto, dividir pendente"

# alteração não commitada, para o git status não estar limpo
cat >> calc.py <<'PY'


def _validar(b):
    if b == 0:
        raise ValueError("divisor zero")
PY
echo "fixture em $RAIZ"
```

- [ ] **Passo 2: Rodar o script e conferir**

Run: `bash $S/preparar_fixture.sh baseline-salvar && cd $S/baseline-salvar/projeto && git status --short && python -m pytest -q`
Expected: `M calc.py`; pytest com 1 passed, 1 failed.

- [ ] **Passo 3: Rodar o cenário sem a skill (baseline)**

Disparar um subagente `general-purpose` com este prompt, substituindo `$S` pelo caminho real:

```
Você está no meio de uma sessão de trabalho no projeto $S/baseline-salvar/projeto (repositório git).
Contexto da sessão até agora: o usuário pediu uma calculadora em calc.py com somar e dividir, com testes em test_calc.py. Você implementou somar, escreveu os dois testes, e começou dividir: criou a validação de divisor zero (_validar) mas ainda não escreveu o corpo de dividir. Vocês decidiram que divisão por zero lança ValueError em vez de retornar None, porque o chamador precisa saber que falhou. O usuário também comentou que neste projeto os testes rodam com "python -m pytest -q".
Para este teste, trate a pasta $S/baseline-salvar/home/.claude como se fosse ~/.claude.
Agora o usuário diz: "vou trocar de chat, salva o handoff para eu continuar depois".
Faça o que faria. Ao final, relate: o que gravou (caminhos e conteúdo), o que commitou, e o que perguntou ao usuário.
```

- [ ] **Passo 4: Registrar o baseline**

Gravar em `$S/baseline-salvar.md` o que o subagente fez, verbatim onde importa: onde gravou o arquivo, se conferiu `git status` e testes antes de escrever, se apresentou rascunho antes de gravar, se tocou no `CLAUDE.md` do projeto e no global, se commitou, o que inventou (riscos, alternativas) e se o próximo passo era único. Esses são os pontos que a skill precisa corrigir.

Expected: falhas típicas a observar: `HANDOFF.md` na raiz; gravação direta sem rascunho; sem linha no `CLAUDE.md`; sem commit ou commit sem confirmação; riscos inventados.

---

### Tarefa 2: Referências da `salvar` (template e README)

**Files:**
- Create: `kfh-handoff-salvar/references/TEMPLATE_HANDOFF.md`
- Create: `kfh-handoff-salvar/references/README_HANDOFF.md`

**Interfaces:**
- Produces: os dois arquivos que o `SKILL.md` da Tarefa 3 manda copiar para `docs/handoff/` do projeto.

- [ ] **Passo 1: Gravar `TEMPLATE_HANDOFF.md`**

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

- [ ] **Passo 2: Gravar `README_HANDOFF.md`**

```markdown
# Handoffs

## Sobre

Este diretório contém os handoffs do projeto: o estado de tarefas começadas e ainda não terminadas, escrito para que outra sessão, outro chat ou outra pessoa continue de onde parou.

Conversa é descartável, arquivo é permanente.

---

## Quando abrir um handoff

Abra quando uma sessão vai encerrar e a tarefa não terminou: código pela metade, decisão tomada mas não aplicada, verificação pendente.

Não abra para tarefa concluída: nesse caso o lugar é o commit, o ADR ou o `CLAUDE.md`.

---

## Ciclo de vida

1. **Abrir ou atualizar**, com a skill `kfh-handoff-salvar`: grava o arquivo aqui, registra a tarefa na seção `## Em andamento (handoff)` do `CLAUDE.md` do projeto e commita.
2. **Retomar**, com a skill `kfh-handoff-continuar`: lê o handoff, confere o estado real do repositório e propõe o próximo passo antes de agir.
3. **Encerrar**, quando a tarefa termina e é verificada: o arquivo vai para `concluidos/` com o mesmo nome e a linha sai do `CLAUDE.md`, na mesma sessão.

A seção do `CLAUDE.md` é o índice do que está aberto. Se uma tarefa está listada lá, ela não terminou.

---

## Template

Todo handoff segue o padrão definido em:

`TEMPLATE_HANDOFF.md`

A seção `Pendente de registro permanente` é opcional: existe só enquanto há item nela.

---

## Estrutura

- Local: `docs/handoff/`
- Concluídos: `docs/handoff/concluidos/`
- Nome: `AAAA-MM-DD-<tema>.md`. A data é a de abertura e não muda ao atualizar. O tema usa minúsculas, sem acento, palavras separadas por traço, sem outro caractere.

Exemplo:

- `2026-10-12-migrar-autenticacao-para-o-gateway.md`

---

## Regras

- Cabe numa tela. O que já está na spec ou no plano é referenciado, não copiado.
- Próximo passo é um só. Se houver dois, o segundo vai para "Falta".
- "Pela metade" sempre diz o que já existe e o que falta naquele item.
- "Como verificar" traz comandos executáveis quando houver.
- Nada inventado: cada decisão e risco veio da conversa ou do usuário.
- Nenhum placeholder do template sobra.

---

## Objetivo

- Trocar de chat sem perder contexto
- Saber, pelo `CLAUDE.md`, o que começou e não terminou
- Guardar as decisões tomadas no caminho, inclusive as descartadas
```

- [ ] **Passo 3: Conferir**

Run: `ls kfh-handoff-salvar/references/ && grep -c '^## ' kfh-handoff-salvar/references/TEMPLATE_HANDOFF.md`
Expected: os dois arquivos listados; `8` seções `##` no template.

- [ ] **Passo 4: Commit**

```bash
git add kfh-handoff-salvar/references/
git commit -m "kfh-handoff-salvar: template e README do handoff em references/

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>"
```

---

### Tarefa 3: `kfh-handoff-salvar/SKILL.md`

**Files:**
- Create: `kfh-handoff-salvar/SKILL.md`

**Interfaces:**
- Consumes: `references/TEMPLATE_HANDOFF.md` e `references/README_HANDOFF.md` da Tarefa 2.
- Produces: a seção `## Em andamento (handoff)` e o bloco `## Handoff`, cujos textos a Tarefa 6 copia sem alteração.

- [ ] **Passo 1: Gravar o `SKILL.md`**

```markdown
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
6. **Confira `~/.claude/CLAUDE.md`.** Se a pasta `~/.claude` existe e o arquivo não contém o título `## Handoff`, o bloco de "Bloco do CLAUDE.md global" será acrescentado ao final na Fase 2, criando o arquivo se preciso. Se já contém, não toque. Se a pasta `~/.claude` não existe (app claude.ai), avise em uma linha e siga.

## Fase 1 — Rascunho

Monte o handoff a partir do que a conversa já tem, seguindo o template seção por seção. Para o que faltar, pergunte, uma pergunta por vez, e só o que falta:

- **Próximo passo:** se a conversa não deixa claro qual é o único próximo passo concreto.
- **Riscos e dúvidas abertas:** se nada foi dito, pergunte "há risco ou dúvida que o próximo chat precisa saber?". Se o usuário disser que não, a seção fica com `- nenhum registrado`.
- **Descartado:** se houve decisão mas as alternativas não aparecem na conversa, pergunte. Não invente alternativas nem riscos.

Não pergunte o que já está na conversa. Não pergunte por nome de arquivo, data ou mensagem de commit: isso você propõe.

**Separe o que é permanente.** Antes de apresentar, percorra as decisões e marque as que não devem morrer com o handoff:

- decisão de arquitetura, trade-off ou regra de negócio: destino ADR, via skill `kfh-criar-adr`;
- regra de como trabalhar neste projeto: destino `CLAUDE.md` do projeto;
- preferência do usuário que vale em todo projeto: destino memória.

Cada uma entra em "Pendente de registro permanente" com o destino. Esta skill não grava ADR nem memória; só aponta. Se o usuário quiser registrar agora, faça depois da gravação do handoff, com a skill certa.

Apresente neste formato, e pare:

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
- **Estado:** três marcas, `Feito`, `Pela metade`, `Falta`. "Pela metade" diz o que já existe e o que falta naquele item. Marca sem conteúdo recebe `nada`.
- **Decisões:** `Decisão - porquê`; descartadas como `Descartado: alternativa - porquê`.
- **Onde está cada coisa:** `caminho ou link - o que é`, incluindo a branch e os arquivos tocados nesta sessão.
- **Próximo passo:** um só, concreto, começando com verbo. Se houver dois, o segundo vai para "Falta".
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
- Nenhuma decisão, alternativa ou risco inventado.
- "Como verificar" com comando e resultado esperado.
- Linha no `CLAUDE.md` do projeto sem duplicata; linhas de outras tarefas e resto do arquivo intactos.
- Bloco global idêntico ao desta skill; `~/.claude/CLAUDE.md` não reescrito.

## Erros comuns

| Erro | Correto |
|------|---------|
| Gravar direto porque "o pedido já tinha tudo" | Rascunho no chat primeiro, sempre |
| `HANDOFF.md` na raiz do projeto | `docs/handoff/AAAA-MM-DD-tema.md` |
| Segundo arquivo para tarefa que já tem handoff | Atualizar o mesmo arquivo |
| Copiar a spec inteira em "Objetivo e porquê" | Uma frase e "detalhes na spec" |
| "Próximo passo: terminar X e depois Y" | Um passo; Y vai para "Falta" |
| "Pela metade: módulo de auth" | "Pela metade: módulo de auth - login feito, refresh de token falta" |
| Risco plausível que ninguém disse | Perguntar; registrar só o confirmado |
| Estado tirado da memória da conversa | `git status` e testes rodados antes do rascunho |
| Reescrever o `CLAUDE.md` ou apagar linha de outra tarefa | Só acrescentar a linha desta tarefa |
| Parar porque não há `~/.claude` | Avisar em uma linha e seguir |
```

- [ ] **Passo 2: Conferir estrutura**

Run: `head -4 kfh-handoff-salvar/SKILL.md && grep -c '' kfh-handoff-salvar/SKILL.md && python -c "import re,sys;t=open('kfh-handoff-salvar/SKILL.md',encoding='utf-8').read();fm=t.split('---')[1];print(len(fm))"`
Expected: frontmatter com `name: kfh-handoff-salvar`; frontmatter abaixo de 1024 caracteres.

- [ ] **Passo 3: Commit**

```bash
git add kfh-handoff-salvar/SKILL.md
git commit -m "kfh-handoff-salvar: SKILL.md (gatilho, antes de começar, rascunho, gravação, CLAUDE.md)

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>"
```

---

### Tarefa 4: Cenários da `salvar` com a skill (GREEN) e fechamento de brechas

**Files:**
- Modify: `kfh-handoff-salvar/SKILL.md` (só se um cenário falhar)
- Create: `$S/resultados-salvar.md` (anotações, fora do projeto)

**Interfaces:**
- Consumes: `preparar_fixture.sh` da Tarefa 1; `SKILL.md` da Tarefa 3.

Cada cenário dispara um subagente `general-purpose`. Prefixo comum a todos os prompts (substituir `$S`, `<nome>` e `<caminho-da-skill>` pelo caminho absoluto de `kfh-handoff-salvar/SKILL.md` neste repositório):

```
Você tem a skill em <caminho-da-skill>. Leia-a inteira (e os arquivos de references/ que ela cita) e siga-a à risca.
Você está no meio de uma sessão de trabalho no projeto $S/<nome>/projeto (repositório git).
Para este teste, trate a pasta $S/<nome>/home/.claude como se fosse ~/.claude em tudo que a skill diz sobre ~/.claude.
Contexto da sessão até agora: o usuário pediu uma calculadora em calc.py com somar e dividir, com testes em test_calc.py. Você implementou somar, escreveu os dois testes, e começou dividir: criou a validação de divisor zero (_validar) mas ainda não escreveu o corpo de dividir. Vocês decidiram que divisão por zero lança ValueError em vez de retornar None, porque o chamador precisa saber que falhou. O usuário também comentou que neste projeto os testes rodam com "python -m pytest -q".
```

- [ ] **Cenário 1a: primeiro uso, gate do rascunho**

Run: `bash $S/preparar_fixture.sh s1a`. Prompt = prefixo + :

```
Agora o usuário diz: "vou trocar de chat, salva o handoff para eu continuar depois".
Faça o que a skill manda. Você NÃO vai receber resposta do usuário neste teste: se a skill manda parar e esperar, pare. Ao final, relate exatamente o que apresentou ao usuário e liste todo arquivo que criou ou alterou (deve ser nenhum, se você parou).
```

Expected: rascunho no formato da Fase 1 com cabeçalho `Arquivo: docs/handoff/2026-10-12-...`, `Spec: nenhuma`, `Plano: nenhum`, estado conferido por `git status` e pytest, um só próximo passo (escrever o corpo de `dividir`), decisão sobre ValueError com "Descartado: retornar None", nenhum arquivo criado. Conferir com `cd $S/s1a/projeto && git status --short && ls` (só `M calc.py`, sem `docs/`).

- [ ] **Cenário 1b: primeiro uso, gravação**

Run: `bash $S/preparar_fixture.sh s1b`. Prompt = prefixo + :

```
Agora o usuário diz: "vou trocar de chat, salva o handoff para eu continuar depois".
Simule a conversa em dois turnos: primeiro produza o rascunho exatamente como a skill manda; em seguida considere que o usuário respondeu "sim" e execute a Fase 2 completa. Ao final, relate o rascunho, o que gravou e o commit.
```

Expected, conferido por comando:

```bash
cd $S/s1b/projeto
ls docs/handoff/            # README_HANDOFF.md TEMPLATE_HANDOFF.md 2026-10-12-<tema>.md
diff docs/handoff/README_HANDOFF.md <repo>/kfh-handoff-salvar/references/README_HANDOFF.md   # vazio
grep -c '<' docs/handoff/2026-10-12-*.md   # 0 placeholders
grep -A3 '^Abertas:' CLAUDE.md             # uma linha com a data e o caminho
grep -c '^## Handoff' $S/s1b/home/.claude/CLAUDE.md   # 1
git log --oneline -1                        # WIP: ... (handoff)
git status --short                          # vazio
```

- [ ] **Cenário 2: atualização, com outra tarefa aberta e CLAUDE.md pré-existente**

Run: `bash $S/preparar_fixture.sh s2`, depois plantar o estado:

```bash
cd $S/s2/projeto
mkdir -p docs/handoff
cp <repo>/kfh-handoff-salvar/references/*.md docs/handoff/
cat > docs/handoff/2026-10-10-implementar-dividir.md <<'MD'
# Handoff - Implementar dividir

**Aberto em:** 10/10/2026
**Atualizado em:** 10/10/2026
**Branch:** main
**Spec:** nenhuma
**Plano:** nenhum

## Objetivo e porquê
Completar a calculadora com dividir, porque somar sozinho não atende o usuário.

## Estado
- Feito: somar e os dois testes
- Pela metade: nada
- Falta: dividir

## Decisões e porquês
- nenhuma ainda

## Onde está cada coisa
- calc.py - funções
- test_calc.py - testes

## Próximo passo
Escrever dividir.

## Riscos e dúvidas abertas
- nenhum registrado

## Como verificar
python -m pytest -q: esperado 1 passed, 1 failed
MD
cat > CLAUDE.md <<'MD'
# Calculadora

Projeto de exemplo. Rode os testes com `python -m pytest -q`.

## Em andamento (handoff)

Tarefas começadas e ainda não terminadas. Cada linha aponta para o handoff em `docs/handoff/`.

- Ao abrir uma sessão, leia a lista abaixo. Para continuar uma delas, use a skill `kfh-handoff-continuar`.
- Ao encerrar com tarefa pela metade, use `kfh-handoff-salvar` para criar ou atualizar o handoff e esta lista.
- Ao terminar e verificar uma tarefa da lista, na mesma sessão, mova o handoff para `docs/handoff/concluidos/` e apague a linha dela aqui.
- Nunca apague uma linha de tarefa que não está terminada e verificada.

Abertas:

- 2026-10-09 — Documentar a API — `docs/handoff/2026-10-09-documentar-a-api.md`
- 2026-10-10 — Implementar dividir — `docs/handoff/2026-10-10-implementar-dividir.md`
MD
mkdir -p $S/s2/home/.claude && printf '## Handoff\n\n- bloco já presente (teste)\n' > $S/s2/home/.claude/CLAUDE.md
git add -A && git commit -q -m "handoffs anteriores"
git checkout -q calc.py   # árvore limpa: testa o commit mesmo sem código novo
```

Prompt = prefixo (ajustar: "a validação _validar já está commitada") + :

```
Agora o usuário diz: "salva o handoff, vou parar por hoje".
Simule os dois turnos: rascunho, depois "sim" e Fase 2. Relate o rascunho, o que gravou e o commit.
```

Expected:

```bash
cd $S/s2/projeto
ls docs/handoff/*.md | wc -l               # 3 (README, TEMPLATE, o mesmo handoff; nenhum novo)
grep 'Aberto em' docs/handoff/2026-10-10-implementar-dividir.md     # 10/10/2026 (preservado)
grep 'Atualizado em' docs/handoff/2026-10-10-implementar-dividir.md # 12/10/2026
grep -c 'implementar-dividir' CLAUDE.md    # 1 (sem duplicata)
grep -c 'documentar-a-api' CLAUDE.md       # 1 (outra tarefa intacta)
head -3 CLAUDE.md                           # cabeçalho original intacto
cat $S/s2/home/.claude/CLAUDE.md           # inalterado
git log --oneline -1                        # WIP: ... (commit aconteceu com árvore limpa)
```

- [ ] **Cenário 3: com spec e plano presentes**

Run: `bash $S/preparar_fixture.sh s3`, depois plantar:

```bash
cd $S/s3/projeto
mkdir -p docs/superpowers/specs docs/superpowers/plans
printf '# Calculadora — Design\n\nObjetivo: somar e dividir. Divisão por zero lança ValueError.\n' > docs/superpowers/specs/2026-10-11-calculadora-design.md
printf '# Calculadora — Plano\n\n### Tarefa 1: somar\n### Tarefa 2: testes\n### Tarefa 3: validar divisor\n### Tarefa 4: dividir\n' > docs/superpowers/plans/2026-10-11-calculadora.md
git add -A && git commit -q -m "spec e plano"
cat >> calc.py <<'PY'


def _validar(b):
    if b == 0:
        raise ValueError("divisor zero")
PY
```

Prompt = prefixo + `Existe spec e plano em docs/superpowers/. Agora o usuário diz: "salva o handoff". Simule os dois turnos e relate.`

Expected: cabeçalho com `**Spec:** docs/superpowers/specs/2026-10-11-calculadora-design.md` e `**Plano:** docs/superpowers/plans/2026-10-11-calculadora.md`; "Estado" por número de tarefa ("tarefas 1 a 3 feitas, 4 falta" ou equivalente); "Objetivo e porquê" com "detalhes na spec"; "Decisões e porquês" sem repetir o ValueError que já está na spec, ou marcando-o como já na spec.

- [ ] **Cenário 7: sem `~/.claude`**

Run: `bash $S/preparar_fixture.sh s7 && rm -rf $S/s7/home`. Prompt = prefixo (com a frase sobre `~/.claude` trocada por "Para este teste, considere que a pasta ~/.claude NÃO existe e trate $S/s7/home/.claude como ~/.claude, que não existe") + `Agora o usuário diz: "salva o handoff". Simule os dois turnos e relate.`

Expected: rascunho com `~/.claude/CLAUDE.md: sem ~/.claude, pulado`; handoff e `CLAUDE.md` do projeto gravados; `ls $S/s7/home` falha (nada criado); commit feito.

- [ ] **Fechar brechas**

Para cada cenário que falhou, anotar em `$S/resultados-salvar.md` a racionalização ou a lacuna, verbatim, e corrigir o `SKILL.md` na seção que corresponde (regra, checklist ou tabela de erros comuns). Rodar o cenário de novo até passar. Só então:

```bash
git add kfh-handoff-salvar/SKILL.md
git commit -m "kfh-handoff-salvar: ajustes após cenários com subagente

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>"
```

Se nenhum cenário falhou, não há commit nesta tarefa.

---

### Tarefa 5: Baseline da `continuar` (RED)

**Files:**
- Create: `$S/baseline-continuar.md` (anotações, fora do projeto)

**Interfaces:**
- Consumes: `preparar_fixture.sh` da Tarefa 1; as referências da Tarefa 2 para plantar um handoff real.

- [ ] **Passo 1: Plantar um projeto com handoff aberto**

```bash
bash $S/preparar_fixture.sh bc
cd $S/bc/projeto
git checkout -q calc.py
mkdir -p docs/handoff
cp <repo>/kfh-handoff-salvar/references/*.md docs/handoff/
cat > docs/handoff/2026-10-10-implementar-dividir.md <<'MD'
# Handoff - Implementar dividir

**Aberto em:** 10/10/2026
**Atualizado em:** 10/10/2026
**Branch:** main
**Spec:** nenhuma
**Plano:** nenhum

## Objetivo e porquê
Completar a calculadora com dividir, porque somar sozinho não atende o usuário.

## Estado
- Feito: somar e os dois testes
- Pela metade: nada
- Falta: dividir, com ValueError para divisor zero

## Decisões e porquês
- Divisão por zero lança ValueError - o chamador precisa saber que falhou
- Descartado: retornar None - esconde o erro

## Onde está cada coisa
- calc.py - funções
- test_calc.py - testes

## Próximo passo
Escrever o corpo de dividir em calc.py, lançando ValueError quando b == 0.

## Riscos e dúvidas abertas
- nenhum registrado

## Como verificar
python -m pytest -q: esperado 1 passed, 1 failed (test_dividir ainda falha)
MD
cat > CLAUDE.md <<'MD'
## Em andamento (handoff)

Tarefas começadas e ainda não terminadas. Cada linha aponta para o handoff em `docs/handoff/`.

- Ao abrir uma sessão, leia a lista abaixo. Para continuar uma delas, use a skill `kfh-handoff-continuar`.
- Ao encerrar com tarefa pela metade, use `kfh-handoff-salvar` para criar ou atualizar o handoff e esta lista.
- Ao terminar e verificar uma tarefa da lista, na mesma sessão, mova o handoff para `docs/handoff/concluidos/` e apague a linha dela aqui.
- Nunca apague uma linha de tarefa que não está terminada e verificada.

Abertas:

- 2026-10-10 — Implementar dividir — `docs/handoff/2026-10-10-implementar-dividir.md`
MD
git add -A && git commit -q -m "WIP: implementar dividir (handoff)"
```

- [ ] **Passo 2: Rodar o cenário sem a skill**

Subagente `general-purpose`:

```
Você abriu uma sessão nova no projeto $S/bc/projeto (repositório git). Leia o CLAUDE.md dele.
Para este teste, trate $S/bc/home/.claude como se fosse ~/.claude.
O usuário diz: "continua de onde paramos; quando terminar, termina de vez".
Faça o que faria. Relate o que leu, o que conferiu, o que fez e o que perguntou.
```

- [ ] **Passo 3: Registrar o baseline**

Em `$S/baseline-continuar.md`: se leu o handoff; se conferiu `git status`, branch e rodou "Como verificar" antes de agir; se propôs o próximo passo e esperou, ou já implementou; ao terminar, se rodou os testes e mostrou resultado; se moveu o handoff para `concluidos/` ou apagou; se apagou a linha e manteve a seção; se commitou.

Expected: falhas típicas: implementa sem propor; apaga o handoff ou deixa onde está; apaga a seção inteira; não commita.

---

### Tarefa 6: `kfh-handoff-continuar/SKILL.md`

**Files:**
- Create: `kfh-handoff-continuar/SKILL.md`

**Interfaces:**
- Consumes: o texto do bloco `## Handoff` da Tarefa 3, copiado sem alteração.

- [ ] **Passo 1: Gravar o `SKILL.md`**

```markdown
---
name: kfh-handoff-continuar
description: Use quando o usuário quer retomar uma tarefa deixada pela metade em outra sessão ou chat, a partir de um handoff em docs/handoff/, ou quando o CLAUDE.md do projeto lista tarefas em "Em andamento (handoff)". Aciona em "continua o handoff", "retoma de onde parou", "lê o HANDOFF", "o que ficou pendente", "terminei a tarefa do handoff". Também para encerrar o handoff quando a tarefa termina.
---

# kfh-handoff-continuar — Versão 1.0

Você retoma uma tarefa a partir do handoff gravado pela `kfh-handoff-salvar`: lê o arquivo, confere o estado real do repositório e propõe o próximo passo. Você só age depois que o usuário aprova a proposta. Quando a tarefa termina e é verificada na sessão, você encerra o handoff: move o arquivo para `docs/handoff/concluidos/` e apaga a linha do `CLAUDE.md`.

Idioma: português com acentos.

## Antes de começar

1. **Garanta o `~/.claude/CLAUDE.md`.** Se a pasta `~/.claude` existe e o arquivo não contém o título `## Handoff`, acrescente ao final o bloco de "Bloco do CLAUDE.md global", criando o arquivo se preciso. Se já contém, não toque. Se a pasta não existe (app claude.ai), avise em uma linha e siga.
2. **Leia a seção `## Em andamento (handoff)` do `CLAUDE.md` do projeto.** Sem a seção, ou com a lista em `- (nenhuma)`: diga que não há handoff aberto e pare. Uma tarefa: é ela. Várias: liste e pergunte qual, salvo o pedido já nomear.
3. **Abra o arquivo da linha.** Se não existe no caminho indicado, procure pelo nome em `docs/handoff/` e em `docs/handoff/concluidos/`. Achou em `concluidos/`: a tarefa já foi encerrada; diga isso e ofereça apagar a linha. Não achou: avise e pare.

## Retomada — antes de agir

1. **Leia o handoff inteiro.** Se o cabeçalho aponta spec ou plano, leia os dois também.
2. **Confira o estado real contra o handoff:**
   - branch atual (`git branch --show-current`) igual à do cabeçalho;
   - `git status --short` e `git log --oneline` desde a data de `Atualizado em`: o que mudou depois do handoff;
   - cada caminho em "Onde está cada coisa" existe;
   - rode o que está em "Como verificar" e compare com o resultado esperado.
   Sem git: só os caminhos e os comandos.
3. **Relate neste formato e pare:**

```
Handoff: docs/handoff/2026-10-12-migrar-autenticacao-para-o-gateway.md (atualizado em 12/10/2026)
Spec/Plano: <caminhos> | nenhum
Confere: branch ok | 3 commits depois do handoff | testes 12/12 | arquivos presentes
Diverge: <o que o handoff diz e o que o repositório mostra> | nada

Próximo passo do handoff: <copiado>
Proposta: <igual> | <ajustado: porquê>

Sigo com isso?
```

Divergência é informação, não erro: mostre a diferença e proponha o que fazer com ela. Um comando de "Como verificar" que falha ou dá resultado diferente do esperado é divergência: entra no relato, não é consertado por conta própria. Só comece a executar após o "sim". Pedido de ajuste não é confirmação.

## Durante a sessão

Trabalhe normalmente. Se a conversa vai acabar com a tarefa ainda aberta, use a `kfh-handoff-salvar`: ela atualiza o mesmo arquivo e a mesma linha.

## Encerramento

Quando a tarefa fica pronta na sessão:

1. **Pronta exige verificação.** Rode "Como verificar" e os testes do projeto, com o resultado mostrado no chat, não afirmado. Se algo falha, não encerre: a tarefa continua aberta.
2. **Confira "Pendente de registro permanente".** Para cada item, pergunte se registra agora (ADR via `kfh-criar-adr`, `CLAUDE.md`, memória) ou deixa. O encerramento não bloqueia por isso, mas o relato final lista o que ficou.
3. **Mostre o que vai fazer e peça confirmação:**

```
Encerrar handoff: docs/handoff/2026-10-12-migrar-autenticacao-para-o-gateway.md
Verificação: testes 14/14 | <comando> ok
Vai: mover para docs/handoff/concluidos/ (mesmo nome); apagar a linha no CLAUDE.md (lista fica: <outras> | - (nenhuma)); commit "Encerrar handoff: migrar autenticação para o gateway"
Pendente permanente: <itens> | nenhum

Posso encerrar?
```

4. **Após o "sim":** mova o arquivo para `docs/handoff/concluidos/` com `git mv`, criando a pasta se faltar (sem git, mova o arquivo); apague só a linha desta tarefa na lista `Abertas:`; se era a última, deixe `- (nenhuma)` no lugar e mantenha a seção com as regras; `git add -A` e `git commit -m "Encerrar handoff: <tema>"`. Reporte o caminho novo, o estado da lista e o hash.

### Bloco do CLAUDE.md global

Use exatamente este bloco em `~/.claude/CLAUDE.md`, precedido de uma linha em branco quando acrescentado a um arquivo existente:

```markdown
## Handoff

- Se a conversa vai encerrar com tarefa pela metade, ou o usuário diz que vai trocar de chat, ofereça a skill `kfh-handoff-salvar` antes de terminar.
- Ao abrir sessão em projeto cujo `CLAUDE.md` tem `## Em andamento (handoff)` com tarefas abertas, diga quais são e ofereça `kfh-handoff-continuar`.
- Ao terminar e verificar uma tarefa dessa lista, encerre o handoff: mova para `docs/handoff/concluidos/` e apague a linha.
```

## Erros comuns

| Erro | Correto |
|------|---------|
| Começar a implementar antes do relatório | Relatório, "Sigo com isso?", e só então agir |
| Confiar no handoff sem rodar `git status` e "Como verificar" | Conferir o estado real; o handoff pode estar defasado |
| Tratar divergência como erro e parar, ou consertar sem avisar | Mostrar a diferença e propor o que fazer |
| Encerrar com teste falhando, ou dizendo "deve passar" | Rodar e mostrar o resultado; falhou, continua aberta |
| Apagar o handoff ao encerrar | Mover para `docs/handoff/concluidos/` |
| Apagar a seção inteira do `CLAUDE.md` ao tirar a última linha | Deixar `- (nenhuma)` e manter as regras |
| Apagar linha de outra tarefa | Só a linha desta tarefa |
| Sessão acabando com tarefa aberta e nada salvo | Chamar `kfh-handoff-salvar` |
```

- [ ] **Passo 2: Conferir que o bloco global é idêntico nos dois `SKILL.md`**

Run:

```bash
python - <<'PY'
import re
def bloco(p):
    t=open(p,encoding='utf-8').read()
    m=re.search(r'### Bloco do CLAUDE.md global.*?```markdown\n(.*?)```',t,re.S)
    return m.group(1)
a=bloco('kfh-handoff-salvar/SKILL.md'); b=bloco('kfh-handoff-continuar/SKILL.md')
print('IGUAL' if a==b else 'DIFERENTE')
PY
```

Expected: `IGUAL`.

- [ ] **Passo 3: Commit**

```bash
git add kfh-handoff-continuar/SKILL.md
git commit -m "kfh-handoff-continuar: SKILL.md (retomada, relatório antes de agir, encerramento)

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>"
```

---

### Tarefa 7: Cenários da `continuar` com a skill (GREEN) e fechamento de brechas

**Files:**
- Modify: `kfh-handoff-continuar/SKILL.md` (só se um cenário falhar)
- Create: `$S/resultados-continuar.md`

**Interfaces:**
- Consumes: o plantio do Passo 1 da Tarefa 5 (repetir com outro nome de fixture para cada cenário); `SKILL.md` da Tarefa 6.

Prefixo comum dos prompts (substituir `<caminho-da-skill>` pelo caminho absoluto de `kfh-handoff-continuar/SKILL.md`):

```
Você tem a skill em <caminho-da-skill>. Leia-a inteira e siga-a à risca.
Você abriu uma sessão nova no projeto $S/<nome>/projeto (repositório git).
Para este teste, trate a pasta $S/<nome>/home/.claude como se fosse ~/.claude em tudo que a skill diz sobre ~/.claude.
```

- [ ] **Cenário 4: uma tarefa aberta, parar antes de agir**

Plantar como no Passo 1 da Tarefa 5 com nome `c4`. Prompt = prefixo + :

```
O usuário diz: "continua o handoff".
Você NÃO vai receber resposta do usuário neste teste: se a skill manda parar e esperar, pare. Relate exatamente o que apresentou e liste todo arquivo que alterou.
```

Expected: relatório no formato da Retomada, com `Confere: branch ok`, pytest `1 passed, 1 failed` batendo com "Como verificar", `Diverge: nada`, proposta igual ao próximo passo; nenhum arquivo do projeto alterado (`git status --short` vazio); `$S/c4/home/.claude/CLAUDE.md` criado com `## Handoff`.

- [ ] **Cenário 5: divergência plantada**

Plantar como `c5`, depois:

```bash
cd $S/c5/projeto
git checkout -q -b experimento
cat > calc.py <<'PY'
def somar(a, b):
    return a + b


def dividir(a, b):
    return a / b
PY
git commit -q -am "dividir sem validar zero"
```

Prompt = prefixo + `O usuário diz: "retoma de onde parou". Sem resposta do usuário neste teste: se a skill manda parar, pare. Relate.`

Expected: `Diverge:` cita branch `experimento` em vez de `main`, um commit depois do handoff, e pytest `2 passed` quando o handoff esperava `1 failed`; proposta ajustada (ex.: "dividir já tem corpo, falta o ValueError para zero; conferir se a branch experimento é a certa"); nenhuma alteração feita.

- [ ] **Cenário 6: encerramento**

Plantar como `c6`. Prompt = prefixo + :

```
O usuário diz: "continua o handoff e termina a tarefa de vez".
Simule a conversa: faça o relatório da Retomada; considere que o usuário respondeu "sim"; implemente dividir conforme o próximo passo; rode a verificação; apresente o pedido de encerramento; considere que o usuário respondeu "sim" de novo; encerre. Relate cada etapa e o resultado dos testes.
```

Expected:

```bash
cd $S/c6/projeto
python -m pytest -q                                   # 2 passed
ls docs/handoff/concluidos/                           # 2026-10-10-implementar-dividir.md
ls docs/handoff/*.md                                  # só README e TEMPLATE
grep -A2 '^Abertas:' CLAUDE.md                        # - (nenhuma)
grep -c 'Nunca apague' CLAUDE.md                      # 1 (regras mantidas)
git log --oneline -1                                  # Encerrar handoff: ...
git status --short                                    # vazio
```

- [ ] **Cenário 6b: encerramento com teste falhando**

Plantar como `c6b`. Prompt = prefixo + :

```
O usuário diz: "o dividir já está pronto, pode encerrar o handoff".
Siga a skill. Sem resposta do usuário neste teste: se a skill manda parar, pare. Relate.
```

Expected: pytest rodado e mostrado com `1 failed`; a skill não encerra; handoff continua em `docs/handoff/`; linha continua no `CLAUDE.md`; nenhum commit novo.

- [ ] **Cenário 7: sem `~/.claude`**

Plantar como `c7` e `rm -rf $S/c7/home`. Prompt = prefixo (com "considere que ~/.claude NÃO existe") + `O usuário diz: "continua o handoff". Sem resposta: pare onde a skill manda. Relate.`

Expected: aviso de uma linha sobre `~/.claude`; relatório da Retomada apresentado; nada criado em `$S/c7/home`.

- [ ] **Cenário 8: linha aponta para handoff já em `concluidos/`**

Plantar como `c8`, depois `cd $S/c8/projeto && mkdir -p docs/handoff/concluidos && git mv docs/handoff/2026-10-10-implementar-dividir.md docs/handoff/concluidos/ && git commit -q -m "movido"`. Prompt = prefixo + `O usuário diz: "continua o handoff". Sem resposta: pare onde a skill manda. Relate.`

Expected: a skill diz que a tarefa já foi encerrada e oferece apagar a linha; não apaga sem resposta; não tenta retomar.

- [ ] **Fechar brechas**

Mesmo procedimento da Tarefa 4: anotar em `$S/resultados-continuar.md`, corrigir o `SKILL.md`, rodar de novo até passar, commit:

```bash
git add kfh-handoff-continuar/SKILL.md
git commit -m "kfh-handoff-continuar: ajustes após cenários com subagente

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>"
```

---

### Tarefa 8: Verificação estrutural, empacotamento e fechamento

**Files:**
- Modify: nenhum esperado; `dist/*.zip` é ignorado pelo git.

- [ ] **Passo 1: Checagens estruturais**

```bash
for s in kfh-handoff-salvar kfh-handoff-continuar; do
  echo "== $s"
  python - "$s" <<'PY'
import sys,re
s=sys.argv[1]; t=open(f'{s}/SKILL.md',encoding='utf-8').read()
fm=t.split('---')[1]
assert f'name: {s}' in fm, 'name difere da pasta'
assert re.search(r'^description: Use quando', fm, re.M), 'description não começa com Use quando'
assert len(fm) < 1024, 'frontmatter > 1024'
print('frontmatter ok', len(fm))
PY
done
ls kfh-handoff-salvar/references/
```

Expected: `frontmatter ok` para as duas; os dois arquivos de `references/`.

- [ ] **Passo 2: Empacotar**

Run: `python empacotar.py kfh-handoff-salvar && python empacotar.py kfh-handoff-continuar`
Expected: `dist/kfh-handoff-salvar.zip` listando `kfh-handoff-salvar/SKILL.md`, `kfh-handoff-salvar/references/README_HANDOFF.md`, `kfh-handoff-salvar/references/TEMPLATE_HANDOFF.md`; `dist/kfh-handoff-continuar.zip` listando `kfh-handoff-continuar/SKILL.md`.

- [ ] **Passo 3: Estado final do git**

Run: `git status --short && git log --oneline -8`
Expected: árvore limpa; commits das Tarefas 2, 3, 6 e os de ajuste, se houve.

- [ ] **Passo 4: Relato ao usuário**

Listar: os dois `SKILL.md` e as referências; quais cenários passaram de primeira e quais exigiram ajuste, com a brecha fechada; o que ficou fora de escopo conforme a spec, seção 11.
