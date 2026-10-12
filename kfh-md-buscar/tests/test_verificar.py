from pathlib import Path

from verificar_citacoes import FALHA, blocos_por_pagina, dividir_celulas, ler_achados, main, normalizar, verificar_registro


def test_dividir_celulas_respeita_pipe_escapado():
    assert dividir_celulas("| a | b \\| c | d |") == ["a", "b | c", "d"]
    assert dividir_celulas("| x |  | y |") == ["x", "", "y"]


def test_ler_achados_le_cabecalho_e_registros(pasta):
    linhas, cabecalho, regs = ler_achados((pasta / "achados.md").read_text(encoding="utf-8"))
    assert cabecalho == ["campo", "resposta", "arquivo", "página", "trecho literal", "status"]
    assert len(regs) == 7
    assert regs[0].campo == "título" and regs[0].pagina == "1" and regs[0].status == "encontrado"
    assert regs[5].trecho == '"| A | 30 |"'
    assert linhas[regs[0].indice].startswith("| título |")


def test_normalizar_aspas_espacos_e_caixa():
    assert normalizar('“Recebido  em\n2020”') == "recebido em 2020"
    assert normalizar('"estatís- tica"') == "estatística"


def test_blocos_por_pagina(pasta):
    blocos = blocos_por_pagina((pasta / "artigo.md").read_text(encoding="utf-8"))
    assert sorted(blocos) == [1, 2]
    assert "Título do Artigo" in blocos[1] and "120 participantes" in blocos[2]
    assert "120 participantes" not in blocos[1]


def test_verificar_cada_registro(pasta):
    _, _, regs = ler_achados((pasta / "achados.md").read_text(encoding="utf-8"))
    cache: dict = {}
    resultados = [verificar_registro(r, [pasta], cache) for r in regs]
    assert resultados == [
        "ok",
        "ok",
        "trecho não existe na página",
        "trecho não existe na página",
        "status incoerente",
        "ok",
        "página não existe",
    ]


def test_arquivo_inexistente_e_sem_marcador(pasta):
    from verificar_citacoes import Registro

    (pasta / "solto.md").write_text("texto sem marcador", encoding="utf-8")
    r1 = Registro("c", "r", "nao_existe.md", "1", '"x"', "encontrado", 0)
    r2 = Registro("c", "r", "solto.md", "1", '"texto"', "encontrado", 0)
    assert verificar_registro(r1, [pasta], {}) == "arquivo não existe"
    assert verificar_registro(r2, [pasta], {}) == "arquivo sem marcador"


def test_main_sem_marcar_so_relata(pasta, capsys):
    codigo = main([str(pasta / "achados.md")])
    out = capsys.readouterr().out
    assert codigo == 1
    assert "| # | campo | arquivo | página | resultado |" in out
    assert "trecho não existe na página" in out
    assert FALHA not in (pasta / "achados.md").read_text(encoding="utf-8")


def test_main_com_marcar_reescreve_status_e_verificado(pasta):
    codigo = main([str(pasta / "achados.md"), "--marcar"])
    assert codigo == 1
    texto = (pasta / "achados.md").read_text(encoding="utf-8")
    assert texto.count(FALHA) == 4
    assert "| título | Título do Artigo de Teste | artigo.md | 1 | \"Título do Artigo de Teste\" | encontrado |" in texto
    assert "| grupo | A: 30 | artigo.md | 1 | \"\\| A \\| 30 \\|\" | encontrado |" in texto  # escape preservado
    assert "\nverificado: 2026-" in texto or "\nverificado: 20" in texto
    # segunda rodada: linhas marcadas contam como pendentes, código continua 1
    assert main([str(pasta / "achados.md")]) == 1


def test_tudo_ok_devolve_zero(tmp_path):
    (tmp_path / "a.md").write_text("<!-- a.pdf | p. 1 -->\nFrase única.\n", encoding="utf-8")
    (tmp_path / "achados.md").write_text(
        "| campo | resposta | arquivo | página | trecho literal | status |\n"
        "| --- | --- | --- | --- | --- | --- |\n"
        "| x | Frase | a.md | 1 | \"Frase única.\" | encontrado |\n"
        "| y | | a.md | | | não encontrado |\n",
        encoding="utf-8",
    )
    assert main([str(tmp_path / "achados.md"), "--marcar"]) == 0
    texto = (tmp_path / "achados.md").read_text(encoding="utf-8")
    assert texto.startswith("---\nverificado: ")  # frontmatter criado quando não existia
