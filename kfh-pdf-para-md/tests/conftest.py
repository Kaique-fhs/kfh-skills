from __future__ import annotations

import sys
from pathlib import Path

import pytest

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "scripts"))
sys.path.insert(0, str(RAIZ / "tests"))

from gerar_pdf import gerar_pdf, grade, linhas_de_texto  # noqa: E402

CABECALHO = (72, 800, "Revista Teste, v. 1")


def _rodape(n: int) -> tuple:
    return (290, 40, str(n))


def _pagina_texto(n: int, frases: list[str]) -> dict:
    return {"textos": linhas_de_texto(72, 770, frases) + [CABECALHO, _rodape(n)]}


def _pagina_colunas(n: int) -> dict:
    esq = linhas_de_texto(60, 770, ["Coluna esquerda linha um.", "Coluna esquerda linha dois.", "Coluna esquerda linha tres."])
    dir_ = linhas_de_texto(310, 770, ["Coluna direita linha um.", "Coluna direita linha dois.", "Coluna direita linha tres."])
    return {"textos": esq + dir_ + [CABECALHO, _rodape(n)]}


def _pagina_artigo_p1(n: int) -> dict:
    titulo = linhas_de_texto(72, 770, [
        "Um estudo longo sobre a associacao entre variaveis categoricas em amostras pequenas",
        "e a sua aplicacao em pesquisas de saude publica no Brasil contemporaneo e rural",
    ])
    esq = linhas_de_texto(60, 720, [
        "Esq linha um.", "Esq linha dois.", "Esq linha tres.", "Esq linha quatro.",
        "Esq linha cinco.", "Esq linha seis bem-",
    ])
    dir_ = linhas_de_texto(310, 720, [
        "dois Dir linha um.", "Dir linha dois.", "Dir linha tres.", "Dir linha quatro.",
        "Dir linha cinco.", "Dir linha seis.",
    ])
    return {"textos": titulo + esq + dir_ + [CABECALHO, _rodape(n)]}


def _pagina_tabela(n: int) -> dict:
    celulas = [(80, 760, "ano"), (200, 760, "n"), (80, 742, "2020"), (200, 742, "30"), (80, 724, "2021"), (200, 724, "45")]
    return {
        "textos": celulas + [(72, 680, "Texto fora da tabela."), CABECALHO, _rodape(n)],
        "linhas": grade(72, 772, [120, 120], 3),
    }


def _grava(tmp_path: Path, nome: str, dados: bytes) -> Path:
    p = tmp_path / nome
    p.write_bytes(dados)
    return p


@pytest.fixture
def pdf_texto(tmp_path) -> Path:
    """3 páginas de texto corrido, cabeçalho repetido e número de página no rodapé; hifenização na p. 1."""
    paginas = [
        _pagina_texto(1, ["Introdução à estatís-", "tica aplicada.", "Segunda frase da página um."]),
        _pagina_texto(2, ["Página dois começa aqui.", "Página dois fala de estatística.", "Outra frase."]),
        _pagina_texto(3, ["Página três encerra."]),
    ]
    return _grava(tmp_path, "texto.pdf", gerar_pdf(paginas))


@pytest.fixture
def pdf_coluna_dupla(tmp_path) -> Path:
    return _grava(tmp_path, "colunas.pdf", gerar_pdf([_pagina_colunas(1), _pagina_colunas(2), _pagina_colunas(3)]))


@pytest.fixture
def pdf_artigo_p1(tmp_path) -> Path:
    """Primeira página de artigo: título largo, duas colunas e quebra 'bem-' / 'dois' entre colunas."""
    return _grava(tmp_path, "artigo.pdf", gerar_pdf([_pagina_artigo_p1(1)]))


@pytest.fixture
def pdf_tabela(tmp_path) -> Path:
    return _grava(tmp_path, "tabela.pdf", gerar_pdf([_pagina_tabela(1), _pagina_tabela(2), _pagina_tabela(3)]))


@pytest.fixture
def pdf_misto(tmp_path) -> Path:
    """p.1 texto, p.2 colunas, p.3 tabela."""
    return _grava(tmp_path, "misto.pdf", gerar_pdf([
        _pagina_texto(1, ["Introdução à estatís-", "tica aplicada.", "Segunda frase da página um."]),
        {"textos": linhas_de_texto(60, 770, ["Coluna esquerda linha um.", "Coluna esquerda linha dois.", "Coluna esquerda linha tres.",
                                             "Página dois fala de estatística."])
                   + linhas_de_texto(310, 770, ["Coluna direita linha um.", "Coluna direita linha dois.", "Coluna direita linha tres."])
                   + [CABECALHO, _rodape(2)]},
        _pagina_tabela(3),
    ]))


@pytest.fixture
def pdf_curto(tmp_path) -> Path:
    """1 página com menos de 20 caracteres e sem imagem."""
    return _grava(tmp_path, "curto.pdf", gerar_pdf([{"textos": [(72, 770, "Fim.")]}]))


@pytest.fixture
def pdf_duas_paginas_com_cabecalho(tmp_path) -> Path:
    return _grava(tmp_path, "duas.pdf", gerar_pdf([
        _pagina_texto(1, ["Primeira página."]),
        _pagina_texto(2, ["Segunda página."]),
    ]))


@pytest.fixture
def pdf_escaneado(tmp_path) -> Path:
    from PIL import Image

    p = tmp_path / "escaneado.pdf"
    Image.new("RGB", (595, 842), "white").save(p)
    return p


@pytest.fixture
def pdf_vazio(tmp_path) -> Path:
    from pypdf import PdfWriter

    p = tmp_path / "vazia.pdf"
    w = PdfWriter()
    w.add_blank_page(595, 842)
    w.write(p)
    return p


@pytest.fixture
def pdf_protegido(tmp_path, pdf_texto) -> Path:
    from pypdf import PdfWriter

    p = tmp_path / "protegido.pdf"
    w = PdfWriter(clone_from=str(pdf_texto))
    w.encrypt("segredo")
    w.write(p)
    return p
