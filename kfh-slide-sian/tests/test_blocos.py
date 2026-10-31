from __future__ import annotations

import re
from pathlib import Path

import pytest

import blocos
import conferir

RAIZ = Path(__file__).resolve().parents[1]
ARQUIVOS = sorted((RAIZ / "blocos").glob("*.md"))
MODELO = RAIZ / "base" / "modelo.html"
NOMES_PROIBIDOS = r"rayssa|ka[ií]que|kaique|marcelo|sgc|sco|banco de horas"


def css_da_base() -> str:
    html = MODELO.read_text(encoding="utf-8")
    return "\n".join(re.findall(r"<style[^>]*>(.*?)</style>", html, re.DOTALL))


def test_ha_blocos():
    assert ARQUIVOS, "nenhum bloco em kfh-slide-sian/blocos"


@pytest.mark.parametrize("caminho", ARQUIVOS, ids=lambda p: p.stem)
def test_bloco_tem_todos_os_campos(caminho):
    b = blocos.ler_bloco(caminho)
    for campo in ("nome", "serve", "quando", "quando_nao", "passos", "editaveis", "css", "html"):
        assert b[campo].strip(), campo
    assert b["editaveis"].startswith(".")


@pytest.mark.parametrize("caminho", ARQUIVOS, ids=lambda p: p.stem)
def test_bloco_sem_cor_literal_nem_fonte(caminho):
    css = blocos.ler_bloco(caminho)["css"]
    pagina = f"<style>{css}</style>"
    assert conferir.cores_literais(pagina) == []
    assert conferir.fontes_invalidas(pagina) == []


@pytest.mark.parametrize("caminho", ARQUIVOS, ids=lambda p: p.stem)
def test_bloco_sem_conteudo_da_referencia(caminho):
    b = blocos.ler_bloco(caminho)
    for campo in ("html", "css"):
        assert re.search(rf"\b(?:{NOMES_PROIBIDOS})\b", b[campo], re.IGNORECASE) is None
    assert not re.search(r"#F5F4F2|#E6E3DF", b["css"] + b["html"], re.IGNORECASE)


@pytest.mark.parametrize("caminho", ARQUIVOS, ids=lambda p: p.stem)
def test_bloco_sem_posicao_absoluta_do_slide(caminho):
    css = blocos.ler_bloco(caminho)["css"]
    # raiz do bloco (seletor de uma classe só) fica no fluxo do .corpo, nunca absoluta
    for seletor, corpo in re.findall(r"([^{}]+)\{([^}]*)\}", css):
        if re.fullmatch(r"\s*\.[\w-]+\s*", seletor):
            assert not re.search(r"position\s*:\s*(?:absolute|fixed)", corpo), seletor


@pytest.mark.parametrize("caminho", ARQUIVOS, ids=lambda p: p.stem)
def test_classes_do_html_existem(caminho):
    b = blocos.ler_bloco(caminho)
    faltando = (
        blocos.classes_usadas(b["html"])
        - blocos.classes_definidas(b["css"])
        - blocos.classes_definidas(css_da_base())
    )
    assert faltando == set()


def test_ler_bloco_campo_ausente(tmp_path):
    md = tmp_path / "x.md"
    md.write_text(
        "# X\n- **Serve para:** a\n- **Quando usar:** b\n- **Quando não usar:** c\n"
        "- **Passos de clique:** d\n## CSS\n```css\n.a{}\n```\n## HTML\n```html\n<p class=\"a\"></p>\n```\n",
        encoding="utf-8",
    )
    with pytest.raises(ValueError, match="Editáveis"):
        blocos.ler_bloco(md)


def test_classes_usadas_e_definidas():
    assert blocos.classes_usadas('<div class="a b"><p class="c"></p></div>') == {"a", "b", "c"}
    assert blocos.classes_definidas(".a .b:hover, .c.d::before { x: 1 } /* .z */") == {"a", "b", "c", "d"}
