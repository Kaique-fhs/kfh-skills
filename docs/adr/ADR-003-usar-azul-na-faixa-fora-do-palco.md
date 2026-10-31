# ADR-003 - Usar azul na faixa fora do palco

**Status:** Proposto
**Data:** 31/10/2026

## Contexto
A referência usava preto (#000) na faixa fora do slide, e preto não é cor da marca (ver ADR-002).

---

## Decisao
A faixa fora do palco usa `--stage-bg: var(--azul)` (#24286E).

- O usuário pode reverter.

---

## Consequencias
- nenhuma cor fora da paleta na página
- o visual difere da referência e ainda não foi aprovado no navegador
- <a confirmar: outras consequências>

---

## Alternativas consideradas
- Preto (#000) da referência - não é cor oficial da marca
- <a confirmar: outras alternativas>

---

## Referencias
- ADR-002-usar-so-cores-oficiais-na-kfh-slide-sian.md
- .superpowers/sdd/2026-10-31-kfh-slide-sian/globais.md
- kfh-slide-sian/base/modelo.html (:root)
- Convencao de nome: `ADR-NNN` — tres digitos, minusculas e tracos, sem prefixo; a serie `ADR-LOCAL-*` foi aposentada (ADR-009). Ver `docs/ams/adr/README_ADR.md`.
