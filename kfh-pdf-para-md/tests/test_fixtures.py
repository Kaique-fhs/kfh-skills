import pdfplumber


def test_pdf_texto_tem_tres_paginas_com_acentos(pdf_texto):
    with pdfplumber.open(str(pdf_texto)) as pdf:
        assert len(pdf.pages) == 3
        assert "Introdução à estatís-" in pdf.pages[0].extract_text()


def test_pdf_coluna_dupla_sai_intercalado_sem_tratamento(pdf_coluna_dupla):
    with pdfplumber.open(str(pdf_coluna_dupla)) as pdf:
        texto = pdf.pages[0].extract_text()
        assert "Coluna esquerda linha um. Coluna direita linha um." in texto


def test_pdf_tabela_detectada(pdf_tabela):
    with pdfplumber.open(str(pdf_tabela)) as pdf:
        assert pdf.pages[0].extract_tables() == [[["ano", "n"], ["2020", "30"], ["2021", "45"]]]


def test_pdf_escaneado_sem_texto_com_imagem(pdf_escaneado):
    with pdfplumber.open(str(pdf_escaneado)) as pdf:
        assert (pdf.pages[0].extract_text() or "") == ""
        assert len(pdf.pages[0].images) == 1


def test_pdf_vazio_sem_texto_sem_imagem(pdf_vazio):
    with pdfplumber.open(str(pdf_vazio)) as pdf:
        assert (pdf.pages[0].extract_text() or "") == ""
        assert pdf.pages[0].images == []


def test_pdf_protegido_nao_abre_no_pdfplumber(pdf_protegido):
    import pytest

    with pytest.raises(Exception):
        pdfplumber.open(str(pdf_protegido))
