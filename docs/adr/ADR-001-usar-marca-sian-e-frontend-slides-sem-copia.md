# ADR-001 - Usar kfh-marca-sian e frontend-slides sem copia na kfh-slide-sian

**Status:** Proposto
**Data:** 31/10/2026

## Contexto
A kfh-slide-sian precisa da identidade visual da SIAN e da mecânica de slides HTML, que já existem em outras duas skills.

- copiar o conteúdo delas deixaria a kfh-slide-sian desatualizada quando as originais mudarem

---

## Decisao
A kfh-slide-sian exige as skills kfh-marca-sian e frontend-slides e lê os arquivos delas na hora de embutir, sem cópia.

- Visual vale a marca; mecânica vale a frontend-slides.
- Da frontend-slides pula-se a Fase 2 (estilo é sempre SIAN; não se oferecem presets nem prévias).

---

## Consequencias
- as mudanças nas duas skills valem na próxima apresentação, sem manutenção dupla
- <a confirmar: consequências negativas, por exemplo dependência de as duas skills estarem instaladas>

---

## Alternativas consideradas
- <a confirmar: alternativas descartadas; a spec cita apenas o risco de copiar o conteúdo>

---

## Referencias
- docs/superpowers/specs/2026-10-31-kfh-slide-sian-design.md (§4b)
- kfh-slide-sian/SKILL.md, kfh-slide-sian/scripts/embutir.py
- Convencao de nome: `ADR-NNN` — tres digitos, minusculas e tracos, sem prefixo; a serie `ADR-LOCAL-*` foi aposentada (ADR-009). Ver `docs/ams/adr/README_ADR.md`.
