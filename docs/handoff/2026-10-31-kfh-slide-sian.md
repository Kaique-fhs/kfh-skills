# Handoff - kfh-slide-sian (31/10/2026)

## Estado
- Branch `kfh-slide-sian` (12 commits sobre main, 15abd2f..a638575) pronto e revisado; 88 testes passam. Não juntado ao main.
- ADRs em Proposta: `docs/adr/ADR-001` a `ADR-003` (aguardam aprovação do usuário).
- `kfh-marca-sian/SKILL.md` tem mudança alheia não commitada; não faz parte desta rodada.

## O que falta
1. Usuário aprovar o visual de `kfh-slide-sian/exemplos/demonstracao.html` no navegador (inclui faixa azul, ADR-003).
2. Juntar o branch ao main.
3. Instalar a skill em `~/.claude/skills/`.
4. Decidir se a lista de nomes proibidos dos testes (nomes de pessoas da referência) vai no zip.
5. Aprovar ou ajustar os ADRs e passá-los a Aceito.

## Follow-ups
- `conferir.py` não checa `fill`/`stroke` de SVG nem cores nomeadas (hoje nenhum arquivo usa).
- Ninguém verificou a impressão.
- Teclado, edição, Ctrl+S e restauração não foram exercitados no navegador (JS vem da referência).

## Minors adiadas (detalhe em `.superpowers/sdd/2026-10-31-kfh-slide-sian/progress.md`)
- embutir.py: write_text fora do try, UnicodeDecodeError não capturado, sem teste do caminho de erro de main, `{{X}}` dentro do viewport-base tratado como marcador.
- conferir.py: atalho `font:` e `font-family: var()` falham abertos; falsos positivos (url(#add), rgba(var()), data:svg); código morto; testes cobrem só os casos do brief.
- modelo/blocos: logos da capa/encerramento animam a cada troca; blocos.py só lê class com aspas duplas; blocos combinados na altura do .corpo.
- cronograma/linha do tempo: `--h 175px` pode tocar a legenda, 600px só cabe sozinho, 5 colunas fixas; Editáveis do cronograma incompletos; comentário de `--ini` aponta data errada.
- SKILL.md: numeração soa manual, description sem "HTML" pode puxar pedido de PowerPoint, não manda ajustar `.capa-roteiro`.
- destaque-lista e faixa-conta ~4% menores que a referência.
