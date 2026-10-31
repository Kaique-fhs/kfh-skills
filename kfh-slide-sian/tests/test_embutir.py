from __future__ import annotations

import base64
from pathlib import Path

import pytest

import embutir

ARQUIVOS_MARCA = {
    "fontes/Supreme-Variable.woff2": b"FONTE",
    "logos/sian-logo-original.png": b"LOGO",
    "logos/sian-logo-branca.png": b"BRANCA",
    "grafismos/sian-icone-canto.png": b"CANTO",
}


def b64(dado: bytes) -> str:
    return base64.b64encode(dado).decode("ascii")


def criar_marca(assets: Path) -> Path:
    for rel, conteudo in ARQUIVOS_MARCA.items():
        alvo = assets / rel
        alvo.parent.mkdir(parents=True, exist_ok=True)
        alvo.write_bytes(conteudo)
    return assets


def criar_viewport(home: Path, versao: str) -> Path:
    css = (
        home / ".claude/plugins/cache/frontend-slides/frontend-slides"
        / versao / "skills/frontend-slides/viewport-base.css"
    )
    css.parent.mkdir(parents=True, exist_ok=True)
    css.write_text(f"/* v{versao} */", encoding="utf-8")
    return css


RASCUNHO = """<style>
/* {{VIEWPORT_BASE}} */
@font-face{src:url({{FONTE_SUPREME}})}
.a{background:url({{LOGO_ORIGINAL}})}
.b{background:url({{LOGO_BRANCA}})}
.c{background:url({{CANTO}})}
</style>
<script>const K = "{{CHAVE_EDICAO}}";</script>
"""


def test_embutir_troca_todos_os_marcadores(tmp_path):
    assets = criar_marca(tmp_path / "assets")
    viewport = tmp_path / "viewport-base.css"
    viewport.write_text("html{margin:0}", encoding="utf-8")
    saida = tmp_path / "apresentacao.html"

    r = embutir.embutir(RASCUNHO, assets, viewport, saida)

    assert "data:font/woff2;base64," + b64(b"FONTE") in r
    assert "data:image/png;base64," + b64(b"LOGO") in r
    assert "data:image/png;base64," + b64(b"BRANCA") in r
    assert "data:image/png;base64," + b64(b"CANTO") in r
    assert "/* viewport-base:inicio */\nhtml{margin:0}\n/* viewport-base:fim */" in r
    assert "sian-apresentacao" in r
    assert "{{" not in r


def test_marcador_desconhecido_falha(tmp_path):
    assets = criar_marca(tmp_path / "assets")
    viewport = tmp_path / "v.css"
    viewport.write_text("x", encoding="utf-8")
    with pytest.raises(embutir.MarcadorDesconhecido) as e:
        embutir.embutir("{{XYZ}}", assets, viewport, tmp_path / "s.html")
    assert "XYZ" in str(e.value)


def test_chave_edicao_com_acento_e_espaco():
    assert embutir.chave_edicao(Path("Reunião de Março.html")) == "sian-reuniao-de-marco"


def test_achar_marca_prefere_irma_no_repo(tmp_path):
    raiz = tmp_path / "repo" / "kfh-slide-sian"
    raiz.mkdir(parents=True)
    irma = criar_marca(tmp_path / "repo" / "kfh-marca-sian" / "assets")
    home = tmp_path / "home"
    criar_marca(home / ".claude/skills/kfh-marca-sian/assets")
    assert embutir.achar_marca(raiz, home) == irma


def test_achar_marca_cai_para_home(tmp_path):
    raiz = tmp_path / "repo" / "kfh-slide-sian"
    raiz.mkdir(parents=True)
    home = tmp_path / "home"
    esperado = criar_marca(home / ".claude/skills/kfh-marca-sian/assets")
    assert embutir.achar_marca(raiz, home) == esperado


def test_achar_marca_sem_arquivo_falha(tmp_path):
    raiz = tmp_path / "repo" / "kfh-slide-sian"
    raiz.mkdir(parents=True)
    with pytest.raises(embutir.DependenciaAusente) as e:
        embutir.achar_marca(raiz, tmp_path / "home")
    assert "kfh-marca-sian" in str(e.value)


def test_viewport_pega_maior_versao_numerica(tmp_path):
    criar_viewport(tmp_path, "2.1.0")
    esperado = criar_viewport(tmp_path, "2.10.0")
    achado = embutir.achar_viewport_base(tmp_path)
    assert achado == esperado
    assert "2.10.0" in str(achado)


def test_viewport_ausente_falha(tmp_path):
    with pytest.raises(embutir.DependenciaAusente) as e:
        embutir.achar_viewport_base(tmp_path)
    assert "frontend-slides" in str(e.value)


def test_main_grava_saida(tmp_path, monkeypatch):
    raiz = tmp_path / "repo" / "kfh-slide-sian"
    raiz.mkdir(parents=True)
    criar_marca(tmp_path / "repo" / "kfh-marca-sian" / "assets")
    home = tmp_path / "home"
    criar_viewport(home, "2.1.0")
    monkeypatch.setattr(embutir, "RAIZ_SKILL", raiz)
    monkeypatch.setattr(Path, "home", classmethod(lambda cls: home))
    rascunho = tmp_path / "rascunho.html"
    rascunho.write_text(RASCUNHO, encoding="utf-8")
    saida = tmp_path / "Reunião de Março.html"

    assert embutir.main([str(rascunho), str(saida)]) == 0
    texto = saida.read_text(encoding="utf-8")
    assert "sian-reuniao-de-marco" in texto
    assert "{{" not in texto
