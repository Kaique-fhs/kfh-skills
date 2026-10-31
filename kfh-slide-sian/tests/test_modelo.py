from __future__ import annotations

import re
from pathlib import Path

import conferir
import embutir
from test_embutir import criar_marca, criar_viewport

MODELO = Path(__file__).resolve().parents[1] / "base" / "modelo.html"


def ler() -> str:
    return MODELO.read_text(encoding="utf-8")


def test_modelo_tem_marcadores():
    texto = ler()
    for marcador in (
        "/* {{VIEWPORT_BASE}} */",
        "{{FONTE_SUPREME}}",
        "{{LOGO_ORIGINAL}}",
        "{{CANTO}}",
        "{{CHAVE_EDICAO}}",
    ):
        assert marcador in texto


def test_modelo_embutido_passa_na_conferencia(tmp_path):
    assets = criar_marca(tmp_path / "assets")
    viewport = criar_viewport(tmp_path / "home", "2.10.0")
    html = embutir.embutir(ler(), assets, viewport, tmp_path / "Modelo.html")
    assert conferir.cores_literais(html) == []
    assert conferir.paleta_root_invalida(html) == []
    assert conferir.fontes_invalidas(html) == []


def test_modelo_sem_conteudo_da_referencia():
    texto = ler()
    proibidos = r"rayssa|ka[ií]que|marcelo|sgc|sco|banco de horas"
    assert re.search(rf"\b(?:{proibidos})\b", texto, re.IGNORECASE) is None
    assert not re.search(r"#F5F4F2|#E6E3DF", texto, re.IGNORECASE)


def test_js_so_tem_o_marcador_da_chave():
    sobras = [m for m in re.findall(r"\{\{[^}]*\}\}", ler()) if m != "{{CHAVE_EDICAO}}"]
    # os demais marcadores do modelo (fora do JS) são esperados; JS não pode ter nenhum
    js = re.search(r"<script>(.*?)</script>", ler(), re.DOTALL).group(1)
    assert [m for m in re.findall(r"\{\{[^}]*\}\}", js) if m != "{{CHAVE_EDICAO}}"] == []
    assert sobras  # sanidade: os marcadores de logo/canto existem


def test_modelo_tem_capa_slide_e_encerramento():
    texto = ler()
    secoes = re.findall(r'<section class="slide([^"]*)"([^>]*)>', texto)
    assert len(secoes) == 3
    assert sum("capa" in c.split() for c, _ in secoes) == 1
    assert sum("encerramento" in c.split() for c, _ in secoes) == 1
    assert all('data-v="1"' in resto for _, resto in secoes)


def test_canto_a_esquerda():
    css = re.search(r"\.canto\s*\{([^}]*)\}", ler()).group(1)
    assert re.search(r"left:\s*0\b", css)
    assert "right" not in css
