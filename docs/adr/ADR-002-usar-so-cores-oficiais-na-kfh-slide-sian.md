# ADR-002 - Usar só cores oficiais e transparências delas na kfh-slide-sian

**Status:** Proposto
**Data:** 31/10/2026

## Contexto
A apresentação de referência usava dois neutros fora da paleta da marca (#F5F4F2 e #E6E3DF).

---

## Decisao
Só valem as cores oficiais da SIAN, inclusive em rgba() com os mesmos RGB.

- #F5F4F2 (fundo de cartão) vira `--fundo-cartao` = rgba(199,195,189,.18).
- #E6E3DF (divisor) vira `--divisor` = rgba(199,195,189,.46).
- O conferir.py reprova qualquer cor fora da paleta.

---

## Consequencias
- o material fica dentro do manual da marca
- o tom dos cartões e divisores muda um pouco em relação à referência
- <a confirmar: outras consequências>

---

## Alternativas consideradas
- Manter os dois neutros da referência - o usuário decidiu que só cores oficiais valem
- <a confirmar: outras alternativas>

---

## Referencias
- docs/superpowers/specs/2026-10-31-kfh-slide-sian-design.md
- .superpowers/sdd/2026-10-31-kfh-slide-sian/globais.md
- kfh-slide-sian/scripts/conferir.py
- Convencao de nome: `ADR-NNN` — tres digitos, minusculas e tracos, sem prefixo; a serie `ADR-LOCAL-*` foi aposentada (ADR-009). Ver `docs/ams/adr/README_ADR.md`.
