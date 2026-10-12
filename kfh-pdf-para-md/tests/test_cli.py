import re
from collections import Counter
from pathlib import Path

import pdfplumber

from extrair_pdf import Pagina, Resumo, abrir_pdf, coletar_pdfs, main, montar_md, processar_pdf, tipo_arquivo

import pytest


def _palavras(texto: str) -> set[str]:
    return set(re.findall(r"\w+", texto.lower()))


def test_tipo_arquivo():
    assert tipo_arquivo([Pagina(1, ["texto"], "a"), Pagina(2, ["texto"], "b")]) == "texto"
    assert tipo_arquivo([Pagina(1, ["texto"], "a"), Pagina(2, ["coluna-dupla"], "b")]) == "misto"
    assert tipo_arquivo([Pagina(1, ["coluna-dupla", "tabelas"], "a"), Pagina(2, ["vazia"], "")]) == "coluna-dupla+tabelas"
    assert tipo_arquivo([Pagina(1, ["vazia"], "")]) == "vazia"


def test_montar_md_frontmatter_e_marcadores(tmp_path):
    caminho = tmp_path / "a|b.pdf"
    paginas = [Pagina(1, ["texto"], "um"), Pagina(2, ["escaneado"], "[não extraído: x]"), Pagina(3, ["tabelas"], "três", ["| a |\n| --- |\n| 1 |"])]
    md = montar_md(caminho, paginas, ["Cab", "numeração de página"])
    assert md.startswith("---\nfonte: a|b.pdf\n")
    assert "paginas: 3\n" in md
    assert "tipo_detectado: misto\n" in md
    assert "tipos_por_pagina: {1: texto, 2: escaneado, 3: tabelas}\n" in md
    assert "paginas_nao_extraidas: [2]\n" in md
    assert 'removido_repetido: ["Cab", "numeração de página"]\n' in md
    assert "<!-- a_b.pdf | p. 1 -->\num\n" in md
    assert "<!-- a_b.pdf | p. 3 -->\ntrês\n\n<!-- tabela 1 -->\n| a |" in md
    assert md.count("<!-- a_b.pdf | p. ") == 3


def test_abrir_pdf_normal(pdf_texto):
    pdf, tmp = abrir_pdf(pdf_texto)
    with pdf:
        assert len(pdf.pages) == 3
    assert tmp is None


def test_abrir_pdf_protegido_levanta_valueerror(pdf_protegido):
    with pytest.raises(ValueError, match="protegido"):
        abrir_pdf(pdf_protegido)


def test_abrir_pdf_invalido(tmp_path):
    ruim = tmp_path / "ruim.pdf"
    ruim.write_bytes(b"isto nao e um pdf")
    with pytest.raises(ValueError, match="invalido"):
        abrir_pdf(ruim)


def test_processar_pdf_gera_md_fiel(pdf_misto, tmp_path):
    saida = tmp_path / "out"
    r = processar_pdf(pdf_misto, saida, sobrescrever=False)
    assert isinstance(r, Resumo)
    assert r.erro is None
    assert r.paginas == 3 and r.tipo == "misto" and r.nao_extraidas == []
    md = (saida / "misto.md").read_text(encoding="utf-8")
    assert md.count("<!-- misto.pdf | p. ") == 3
    # cabeçalho repetido e numeração removidos e registrados
    assert "Revista Teste, v. 1" not in md.split("---", 2)[2]
    assert 'removido_repetido: ["Revista Teste, v. 1", "numeração de página"]' in md
    assert "removido: Revista Teste, v. 1" in r.observacoes
    # não acrescenta: toda palavra do corpo (com hifens) existe no texto bruto, sem pré-junção
    corpo = md.split("---", 2)[2]
    corpo_sem_marcadores = re.sub(r"<!--.*?-->", "", corpo)
    corpo_sem_marcadores = re.sub(r"^\|(?: --- \|)+$", "", corpo_sem_marcadores, flags=re.M)  # separador de tabela
    with pdfplumber.open(str(pdf_misto)) as pdf:
        bruto = "\n".join((pg.extract_text() or "") for pg in pdf.pages)
    palavras_corpo = Counter(re.findall(r"[\w-]+", corpo_sem_marcadores.lower()))
    palavras_bruto = Counter(re.findall(r"[\w-]+", bruto.lower()))
    # palavra juntada na quebra de linha: a forma junta existe em outro ponto do bruto (regra do vocabulário);
    # cada junção legítima soma 1 ao permitido dessa forma
    for ini, fim in re.findall(r"(\w+)-\n(\w+)", bruto.lower()):
        if palavras_bruto[ini + fim] > 0:
            palavras_bruto[ini + fim] += 1
    inventadas = set(palavras_corpo) - set(palavras_bruto)
    assert inventadas == set(), f"palavras inventadas: {inventadas}"
    duplicadas = {w: c for w, c in palavras_corpo.items() if c > palavras_bruto[w]}
    assert duplicadas == {}, f"palavras duplicadas: {duplicadas}"


def test_caminho_longo_grava_com_prefixo_estendido(pdf_texto, tmp_path):
    saida = tmp_path
    while len(str((saida / "texto.md").absolute())) < 255:
        saida = saida / ("pasta_longa_" + "x" * 40)
    r = processar_pdf(pdf_texto, saida, sobrescrever=False)
    assert r.erro is None, r.erro
    assert len(str(r.saida.absolute())) >= 255
    assert Path("\\\\?\\" + str(r.saida.absolute())).exists()


def test_processar_pdf_escaneado_marca_pagina(pdf_escaneado, tmp_path):
    r = processar_pdf(pdf_escaneado, tmp_path / "out", False)
    assert r.nao_extraidas == [1]
    md = (tmp_path / "out" / "escaneado.md").read_text(encoding="utf-8")
    assert "paginas_nao_extraidas: [1]" in md
    assert "[não extraído: página sem camada de texto, provável escaneado]" in md


def test_processar_pdf_protegido_devolve_erro(pdf_protegido, tmp_path):
    r = processar_pdf(pdf_protegido, tmp_path / "out", False)
    assert r.erro == "não extraído: protegido"
    assert r.saida is None
    assert not (tmp_path / "out" / "protegido.md").exists()


def test_processar_pdf_nao_sobrescreve_sem_flag(pdf_texto, tmp_path):
    saida = tmp_path / "out"
    processar_pdf(pdf_texto, saida, False)
    (saida / "texto.md").write_text("conteúdo antigo", encoding="utf-8")
    r = processar_pdf(pdf_texto, saida, False)
    assert r.erro is None
    assert "já existia; pulado (use --sobrescrever)" in r.observacoes
    assert (saida / "texto.md").read_text(encoding="utf-8") == "conteúdo antigo"
    processar_pdf(pdf_texto, saida, True)
    assert (saida / "texto.md").read_text(encoding="utf-8").startswith("---\nfonte: texto.pdf")


def test_coletar_pdfs(tmp_path, pdf_texto):
    vazia = tmp_path / "vazia_dir"
    vazia.mkdir()
    pdfs, msgs = coletar_pdfs([str(pdf_texto), str(vazia), str(tmp_path / "nao_existe.pdf")])
    assert pdfs == [pdf_texto]
    assert any(m.startswith("aviso: pasta sem PDF") for m in msgs)
    assert any(m.startswith("erro: caminho não existe") for m in msgs)


def test_main_pasta_padrao_e_codigo_de_saida(pdf_texto, pdf_protegido, capsys):
    codigo = main([str(pdf_texto.parent)])
    saida = capsys.readouterr()
    assert codigo == 1  # protegido.pdf está na mesma pasta
    assert (pdf_texto.parent / "extraido" / "texto.md").exists()
    assert "| arquivo | páginas | tipo | não extraídas | saída | observações |" in saida.out
    assert "não extraído: protegido" in saida.out
    assert "erro: protegido.pdf: não extraído: protegido" in saida.err


def test_main_com_saida_explicita(pdf_texto, tmp_path):
    destino = tmp_path / "md"
    assert main([str(pdf_texto), "--saida", str(destino)]) == 0
    assert (destino / "texto.md").exists()


def test_saida_apontando_para_arquivo_nao_derruba_o_lote(pdf_texto, tmp_path, capsys):
    arquivo = tmp_path / "arquivo.txt"
    arquivo.write_text("x", encoding="utf-8")
    codigo = main([str(pdf_texto), "--saida", str(arquivo)])
    saida = capsys.readouterr()
    assert codigo == 1
    assert "não extraído: não foi possível gravar" in saida.out
    assert "erro: texto.pdf:" in saida.err
    assert "Traceback" not in saida.err


def test_abrir_pdf_fallback_falho_nao_deixa_temporario(pdf_texto, monkeypatch):
    import tempfile

    import extrair_pdf

    def levanta(*a, **k):
        raise RuntimeError("x")

    antes = {p.name for p in Path(tempfile.gettempdir()).glob("*.pdf")}
    monkeypatch.setattr(extrair_pdf.pdfplumber, "open", levanta)
    with pytest.raises(ValueError, match="invalido"):
        abrir_pdf(pdf_texto)
    depois = {p.name for p in Path(tempfile.gettempdir()).glob("*.pdf")}
    assert depois - antes == set()
