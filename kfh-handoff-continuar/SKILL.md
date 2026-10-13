---
name: kfh-handoff-continuar
description: Use quando o usuário quer retomar uma tarefa deixada pela metade em outra sessão ou chat, a partir de um handoff em docs/handoff/, ou quando o CLAUDE.md do projeto lista tarefas em "Em andamento (handoff)". Aciona em "continua o handoff", "retoma de onde parou", "lê o HANDOFF", "o que ficou pendente", "terminei a tarefa do handoff". Também para encerrar o handoff quando a tarefa termina.
---

# kfh-handoff-continuar — Versão 1.0

Você retoma uma tarefa a partir do handoff gravado pela `kfh-handoff-salvar`: lê o arquivo, confere o estado real do repositório e propõe o próximo passo. Você só age depois que o usuário aprova a proposta. Quando a tarefa termina e é verificada na sessão, você encerra o handoff: move o arquivo para `docs/handoff/concluidos/` e apaga a linha do `CLAUDE.md`.

Idioma: português com acentos.

## Antes de começar

1. **Garanta o `~/.claude/CLAUDE.md`.** Se a pasta `~/.claude` existe e o arquivo não contém o título `## Handoff`, acrescente ao final o bloco de "Bloco do CLAUDE.md global", criando o arquivo se preciso. Se já contém, não toque. Se a pasta não existe (app claude.ai), avise em uma linha e siga. Não crie outro arquivo ou pasta em `~/.claude`.
2. **Leia a seção `## Em andamento (handoff)` do `CLAUDE.md` do projeto.** Uma tarefa: é ela. Várias: liste e pergunte qual, salvo o pedido já nomear. Sem a seção, ou com a lista em `- (nenhuma)`: se o usuário anexou ou apontou um arquivo de handoff, ou existe um `.md` aberto em `docs/handoff/`, use esse arquivo e, no relato da Retomada, acrescente a linha `Registro: handoff fora do índice; vou copiá-lo para docs/handoff/ e registrar a linha no CLAUDE.md antes de seguir`. Se não há arquivo nenhum, diga que não há handoff aberto e pare.
3. **Abra o arquivo da linha.** Se não existe no caminho indicado, procure pelo nome em `docs/handoff/` e em `docs/handoff/concluidos/`. Achou em `concluidos/`: a tarefa já foi encerrada; diga isso e ofereça apagar a linha. Não achou: avise e pare.

## Retomada — antes de agir

1. **Leia o handoff inteiro.** Se o cabeçalho aponta spec ou plano, leia os dois também.
2. **Confira o estado real contra o handoff:**
   - branch atual (`git branch --show-current`) igual à do cabeçalho;
   - `git status --short`, e os commits depois do handoff: `git log --oneline $(git log -1 --format=%H -- docs/handoff/<arquivo>)..HEAD`. A âncora é o último commit que tocou o arquivo do handoff, nunca a data do cabeçalho: a data tem só o dia e o git lê DD/MM como MM/DD. Lista vazia significa "nenhum commit depois do handoff", e isso não é divergência. Se o handoff nunca foi commitado, use `git log --oneline -5` e diga isso no relato;
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

O relato e a parada valem mesmo quando o próximo passo é óbvio, a decisão já está tomada e o usuário disse "termina de vez": o relato existe para o usuário conferir se o handoff ainda descreve o repositório, e só ele pode dizer que sim.

## Durante a sessão

Execute o próximo passo como está no handoff. Trabalho que você acha que deveria existir, mas o handoff e o usuário não pediram (um teste a mais, uma refatoração), vai como pergunta no chat, não como código. Feito o próximo passo, olhe "Pela metade" e "Falta": se ainda há item, a tarefa não está pronta; proponha o item seguinte e espere o "sim", mesmo que o usuário tenha dito "termina de vez". Se a conversa vai acabar com a tarefa ainda aberta, use a `kfh-handoff-salvar`: ela atualiza o mesmo arquivo e a mesma linha.

## Encerramento

A tarefa está pronta quando as três coisas valem ao mesmo tempo: o próximo passo foi feito; "Pela metade" e "Falta" não têm mais item; a verificação abaixo passou e foi mostrada. Faltando uma, não há encerramento.

1. **Pronta exige verificação.** Rode "Como verificar" e os testes do projeto, com o resultado mostrado no chat, não afirmado. Se algo falha, não encerre: a tarefa continua aberta.
2. **Confira "Pendente de registro permanente".** Para cada item, pergunte se registra agora (ADR via `kfh-criar-adr`, `CLAUDE.md`, memória) ou deixa. O encerramento não bloqueia por isso, mas o relato final lista o que ficou.
3. **Mostre o que vai fazer e peça confirmação:**

```
Encerrar handoff: docs/handoff/2026-10-12-migrar-autenticacao-para-o-gateway.md
Verificação: testes 14/14 | <comando> ok
Código pendente: <resumo do git status> — commit próprio "<mensagem descritiva>" antes do encerramento | nenhum
Vai: mover para docs/handoff/concluidos/ (mesmo nome); apagar a linha no CLAUDE.md (lista fica: <outras> | - (nenhuma)); commit "Encerrar handoff: migrar autenticação para o gateway" | sem git, sem commit
Pendente permanente: <itens> | nenhum

Posso encerrar?
```

4. **Após o "sim":** se há código da tarefa não commitado, faça primeiro um commit próprio, com mensagem que descreva o código, não o handoff. Depois mova o arquivo para `docs/handoff/concluidos/` com `git mv`, criando a pasta se faltar; apague só a linha desta tarefa na lista `Abertas:`; se era a última, escreva `- (nenhuma)` no lugar dela e mantenha a seção com as regras; `git add -A` e `git commit -m "Encerrar handoff: <tema>"`. O commit de encerramento leva só a movimentação e o `CLAUDE.md`. Sem git: mova o arquivo, edite o `CLAUDE.md` e avise que não houve commit. Reporte o caminho novo, o estado da lista e os hashes.

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
| Começar a implementar antes do relatório porque "o próximo passo era claro" | Relatório, "Sigo com isso?", e só então agir |
| Confiar no handoff sem rodar `git status` e "Como verificar" | Conferir o estado real; o handoff pode estar defasado |
| Tratar divergência como erro e parar, ou consertar sem avisar | Mostrar a diferença e propor o que fazer |
| Acrescentar teste ou refatoração que o handoff não pede | Perguntar; executar só o próximo passo |
| Encerrar com teste falhando, ou dizendo "deve passar" | Rodar e mostrar o resultado; falhou, continua aberta |
| Encerrar com item ainda em "Falta" porque o próximo passo foi feito | Propor o item seguinte e esperar; pronta é "Falta" vazio |
| `git log --since=<Atualizado em>` e relatar os commits do mesmo dia como divergência | Âncora no último commit que tocou o handoff |
| Código da tarefa dentro do commit "Encerrar handoff" | Commit próprio do código antes; o de encerramento leva só a movimentação e o `CLAUDE.md` |
| Parar porque não há seção no `CLAUDE.md`, com handoff anexado pelo usuário | Usar o arquivo e registrá-lo no projeto antes de seguir |
| Apagar o handoff ao encerrar | Mover para `docs/handoff/concluidos/` |
| Deixar `Abertas:` vazio, ou apagar a seção inteira, ao tirar a última linha | Escrever `- (nenhuma)` e manter as regras |
| Apagar linha de outra tarefa | Só a linha desta tarefa |
| Sessão acabando com tarefa aberta e nada salvo | Chamar `kfh-handoff-salvar` |
