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
