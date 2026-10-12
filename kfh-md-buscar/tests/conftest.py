from __future__ import annotations

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

ARTIGO_MD = """---
fonte: artigo.pdf
paginas: 2
---

<!-- artigo.pdf | p. 1 -->
Título do Artigo de Teste
Recebido em 2020, publicado em
março de 2021.
Autores: Fulana Silva e Beltrano Souza.

<!-- tabela 1 -->
| grupo | n |
| --- | --- |
| A | 30 |

<!-- artigo.pdf | p. 2 -->
A amostra teve 120 participantes.
Conclusão: o efeito foi pequeno.
"""

ACHADOS_MD = """---
pasta: .
arquivos: 1
campos: [título, ano, autores, amostra, revista, grupo]
gerado_em: 2026-10-12T16:10:00
---

| campo | resposta | arquivo | página | trecho literal | status |
| --- | --- | --- | --- | --- | --- |
| título | Título do Artigo de Teste | artigo.md | 1 | "Título do Artigo de Teste" | encontrado |
| ano | 2021 | artigo.md | 1 | “Recebido em 2020, publicado em março de 2021.” | encontrado |
| autores | Fulana Silva e Beltrano Souza | artigo.md | 2 | "Autores: Fulana Silva e Beltrano Souza." | encontrado |
| amostra | 120 | artigo.md | 2 | "A amostra teve 150 participantes." | parcial |
| revista | Revista X | artigo.md | | | não encontrado |
| grupo | A: 30 | artigo.md | 1 | "\\| A \\| 30 \\|" | encontrado |
| efeito | pequeno | artigo.md | 3 | "o efeito foi pequeno" | encontrado |
"""


@pytest.fixture
def pasta(tmp_path) -> Path:
    (tmp_path / "artigo.md").write_text(ARTIGO_MD, encoding="utf-8")
    (tmp_path / "achados.md").write_text(ACHADOS_MD, encoding="utf-8")
    return tmp_path
