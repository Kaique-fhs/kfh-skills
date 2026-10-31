from __future__ import annotations

from conferir import (
    cores_literais,
    fontes_invalidas,
    main,
    paleta_root_invalida,
    rotulos_repetidos,
)


def test_cor_literal_fora_do_root_reprovada():
    assert cores_literais("<style>.a{color:#F5F4F2}</style>") == ["#F5F4F2"]


def test_root_e_viewport_ignorados():
    html = (
        "<style>:root{--x:#24286E}\n"
        "/* viewport-base:inicio */\nhtml{background:#000}\n/* viewport-base:fim */\n"
        ".b{color:var(--x)}</style>"
    )
    assert cores_literais(html) == []


def test_id_e_data_uri_nao_contam():
    html = (
        "<style>#deckStage{left:0}</style>"
        '<img src="data:image/png;base64,AAAA#fff">'
    )
    assert cores_literais(html) == []


def test_style_inline_reprovado():
    html = '<div style="background:rgba(0,0,0,.5)">x</div>'
    assert len(cores_literais(html)) == 1


def test_root_aceita_oficiais_com_caixa_e_espacos():
    html = "<style>:root{--a:#ff6934;--b:rgba( 255 , 105 , 52 , .16 )}</style>"
    assert paleta_root_invalida(html) == []


def test_root_reprova_neutro_antigo():
    assert paleta_root_invalida("<style>:root{--d:#E6E3DF}</style>") == ["#E6E3DF"]


def test_fontes():
    ok = (
        '<style>a{font-family:"Supreme",sans-serif}'
        'b{font:600 15px "Supreme", sans-serif}</style>'
    )
    assert fontes_invalidas(ok) == []
    assert fontes_invalidas("<style>a{font-family:Arial}</style>") == ["Arial"]


def test_main_codigo_de_saida(tmp_path, capsys):
    limpo = tmp_path / "limpo.html"
    limpo.write_text("<style>:root{--a:#24286E}a{color:var(--a)}</style>", encoding="utf-8")
    sujo = tmp_path / "sujo.html"
    sujo.write_text("<style>.a{color:#F5F4F2}</style>", encoding="utf-8")
    assert main([str(limpo)]) == 0
    assert "OK" in capsys.readouterr().out
    assert main([str(sujo)]) == 1
    assert "#F5F4F2" in capsys.readouterr().out


def test_rotulos_repetidos_devolve_o_repetido():
    html = (
        '<section class="slide" aria-label="X" data-v="1"></section>'
        '<section class="slide capa" aria-label="X" data-v="1"></section>'
    )
    assert rotulos_repetidos(html) == ["X"]


def test_rotulos_unicos_devolvem_vazio():
    html = (
        '<section class="slide" aria-label="A" data-v="1"></section>'
        '<section class="slide" aria-label="B" data-v="1"></section>'
        '<button aria-label="A"></button>'
    )
    assert rotulos_repetidos(html) == []


def test_main_reprova_rotulo_repetido(tmp_path, capsys):
    arq = tmp_path / "rep.html"
    arq.write_text(
        '<section class="slide" aria-label="X"></section><section class="slide" aria-label="X"></section>',
        encoding="utf-8",
    )
    assert main([str(arq)]) == 1
    assert "X" in capsys.readouterr().out
