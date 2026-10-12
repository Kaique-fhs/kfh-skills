import pdfplumber

from extrair_pdf import ESCANEADO, VAZIA, Pagina, detectar_colunas, extrair_pagina


def _pagina(caminho, n):
    pdf = pdfplumber.open(str(caminho))
    return pdf, pdf.pages[n - 1]


def test_pagina_texto(pdf_texto):
    pdf, pg = _pagina(pdf_texto, 1)
    with pdf:
        p = extrair_pagina(pg)
    assert isinstance(p, Pagina)
    assert p.numero == 1
    assert p.tipos == ["texto"]
    assert "Introdução à estatística aplicada." in p.texto  # hifenização juntada
    assert p.tabelas == []
    assert p.extraida


def test_detecta_calha_em_coluna_dupla(pdf_coluna_dupla):
    pdf, pg = _pagina(pdf_coluna_dupla, 1)
    with pdf:
        x = detectar_colunas(pg)
    assert x is not None
    assert 200 < x < 310  # coluna esquerda termina perto de x=200; direita começa em 310; a calha é a primeira faixa vazia depois de 35% (208pt)


def test_nao_detecta_calha_em_texto_corrido(pdf_texto):
    pdf, pg = _pagina(pdf_texto, 1)
    with pdf:
        assert detectar_colunas(pg) is None


def test_pagina_coluna_dupla_sai_em_ordem_de_leitura(pdf_coluna_dupla):
    pdf, pg = _pagina(pdf_coluna_dupla, 1)
    with pdf:
        p = extrair_pagina(pg)
    assert "coluna-dupla" in p.tipos
    assert p.texto.index("Coluna esquerda linha tres.") < p.texto.index("Coluna direita linha um.")
    assert "Coluna esquerda linha um. Coluna direita linha um." not in p.texto


def test_pagina_com_tabela_separa_tabela_do_texto(pdf_tabela):
    pdf, pg = _pagina(pdf_tabela, 1)
    with pdf:
        p = extrair_pagina(pg)
    assert "tabelas" in p.tipos
    assert p.tabelas == ["| ano | n |\n| --- | --- |\n| 2020 | 30 |\n| 2021 | 45 |"]
    assert "Texto fora da tabela." in p.texto
    assert "2020" not in p.texto  # conteúdo da tabela não duplica no corpo


def test_pagina_escaneada(pdf_escaneado):
    pdf, pg = _pagina(pdf_escaneado, 1)
    with pdf:
        p = extrair_pagina(pg)
    assert p.tipos == ["escaneado"]
    assert p.texto == ESCANEADO
    assert not p.extraida


def test_pagina_vazia(pdf_vazio):
    pdf, pg = _pagina(pdf_vazio, 1)
    with pdf:
        p = extrair_pagina(pg)
    assert p.tipos == ["vazia"]
    assert p.texto == VAZIA
    assert p.extraida


def test_pagina_curta_sem_imagem_e_texto_nao_escaneado(pdf_curto):
    pdf, pg = _pagina(pdf_curto, 1)
    with pdf:
        p = extrair_pagina(pg)
    assert p.tipos == ["texto"]
    assert p.texto == "Fim."
