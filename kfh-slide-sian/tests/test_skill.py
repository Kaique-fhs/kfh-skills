from __future__ import annotations

import re
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
SKILL = RAIZ / "SKILL.md"


def _texto() -> str:
    return SKILL.read_text(encoding="utf-8")


def _corpo_apos_frontmatter() -> list[str]:
    linhas = _texto().splitlines()
    assert linhas[0] == "---"
    fim = linhas.index("---", 1)
    return linhas[fim + 1 :]


def test_frontmatter():
    texto = _texto()
    assert texto.startswith("---\n")
    cabecalho = texto.split("---", 2)[1]
    assert "name: kfh-slide-sian" in cabecalho
    assert "description:" in cabecalho


def test_obrigatorias_no_topo():
    topo = "\n".join(_corpo_apos_frontmatter()[:30])
    assert "kfh-marca-sian" in topo
    assert "frontend-slides" in topo


def test_indice_bate_com_pasta():
    citados = set(re.findall(r"blocos/([\w-]+)\.md", _texto()))
    existentes = {p.stem for p in (RAIZ / "blocos").glob("*.md")}
    assert citados, "o SKILL.md não cita nenhum bloco"
    assert citados == existentes


def test_pula_fase_2():
    assert "Fase 2" in _texto()
