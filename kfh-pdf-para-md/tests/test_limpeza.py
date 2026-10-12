from extrair_pdf import ESCANEADO, VAZIA, juntar_hifenizacao, limpar_texto, marcador, nome_seguro, tabela_para_markdown


def test_constantes_de_texto_fixo():
    assert ESCANEADO == "[não extraído: página sem camada de texto, provável escaneado]"
    assert VAZIA == "[página sem conteúdo]"


def test_junta_hifen_quando_proxima_letra_e_minuscula():
    assert juntar_hifenizacao("estatís-\ntica aplicada") == "estatística aplicada"


def test_nao_junta_hifen_antes_de_maiuscula_ou_numero():
    assert juntar_hifenizacao("Grupo-\nControle") == "Grupo-\nControle"
    assert juntar_hifenizacao("COVID-\n19") == "COVID-\n19"


def test_limpar_colapsa_espacos_e_linhas_vazias():
    entrada = "a   b\t c\n\n\n\nd  \n"
    assert limpar_texto(entrada) == "a b c\n\nd"


def test_limpar_aplica_hifenizacao():
    assert limpar_texto("estatís-\ntica") == "estatística"


def test_tabela_para_markdown_escapa_pipe_e_completa_colunas():
    linhas = [["ano", "n|m"], ["2020", None], ["2021"]]
    assert tabela_para_markdown(linhas) == (
        "| ano | n\\|m |\n"
        "| --- | --- |\n"
        "| 2020 |  |\n"
        "| 2021 |  |"
    )


def test_tabela_para_markdown_troca_quebra_de_linha_na_celula():
    assert tabela_para_markdown([["a\nb", "c"], ["1", "2"]]).splitlines()[0] == "| a b | c |"


def test_nome_seguro_substitui_pipe_e_seta():
    assert nome_seguro("a|b-->c.pdf") == "a_b_c.pdf"
    assert nome_seguro("normal.pdf") == "normal.pdf"


def test_marcador_tem_formato_do_contrato():
    assert marcador("artigo.pdf", 7) == "<!-- artigo.pdf | p. 7 -->"
    assert marcador("a|b.pdf", 1) == "<!-- a_b.pdf | p. 1 -->"


def test_junta_hifen_com_vocabulario_quando_forma_junta_existe():
    assert juntar_hifenizacao("estatís-\ntica aplicada", {"estatística"}) == "estatística aplicada"
    assert limpar_texto("estatís-\ntica", {"estatística"}) == "estatística"


def test_nao_junta_composto_sem_evidencia_no_vocabulario():
    assert juntar_hifenizacao("bem-\nestar", {"outra"}) == "bem-\nestar"
    assert limpar_texto("qui-\nquadrado", set()) == "qui-\nquadrado"
