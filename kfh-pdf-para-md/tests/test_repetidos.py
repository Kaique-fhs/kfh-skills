from extrair_pdf import VAZIA, Pagina, detectar_repetidos, normalizar_linha, remover_repetidos


def _p(n, texto, tipos=None):
    return Pagina(n, tipos or ["texto"], texto)


def test_normalizar_linha():
    assert normalizar_linha("Revista  X, v. 12, n. 3") == "revista x, v. ##, n. #"


def test_detecta_cabecalho_em_mais_da_metade_das_paginas():
    paginas = [
        _p(1, "Revista X, v. 1\nTexto um.\n1"),
        _p(2, "Revista X, v. 1\nTexto dois.\n2"),
        _p(3, "Revista X, v. 1\nTexto três.\n3"),
        _p(4, "Sem cabeçalho aqui.\nTexto quatro."),
    ]
    rep = detectar_repetidos(paginas)
    assert rep == {"revista x, v. #": "Revista X, v. 1"}


def test_nao_detecta_com_duas_paginas():
    paginas = [_p(1, "Autor Fulano\nPrimeira."), _p(2, "Autor Fulano\nSegunda.")]
    assert detectar_repetidos(paginas) == {}
    assert remover_repetidos(paginas, {}) == []
    assert paginas[0].texto == "Autor Fulano\nPrimeira."


def test_exige_minimo_de_tres_ocorrencias():
    paginas = [_p(1, "Cab\na"), _p(2, "Cab\nb"), _p(3, "x\nc"), _p(4, "y\nd")]
    assert detectar_repetidos(paginas) == {}  # 2 de 4 não passa de 50%


def test_remove_cabecalho_e_numeracao_e_registra():
    paginas = [
        _p(1, "Revista X, v. 1\nTexto um.\n1"),
        _p(2, "Revista X, v. 1\nTexto dois.\n2"),
        _p(3, "Revista X, v. 1\nTexto três.\n3"),
    ]
    removidos = remover_repetidos(paginas, detectar_repetidos(paginas))
    assert removidos == ["Revista X, v. 1", "numeração de página"]
    assert [p.texto for p in paginas] == ["Texto um.", "Texto dois.", "Texto três."]


def test_so_remove_na_borda_nao_no_meio():
    paginas = [
        _p(1, "Cab\nmeio um\nCab\nfim um\nz"),
        _p(2, "Cab\nmeio dois\nCab\nfim dois\nz"),
        _p(3, "Cab\nmeio tres\nCab\nfim tres\nz"),
    ]
    remover_repetidos(paginas, detectar_repetidos(paginas))
    # "Cab" e "z" repetem na borda das 3 páginas e saem; o "Cab" central fica. Linhas com palavras
    # diferentes (um/dois/tres) não repetem; com dígitos repetiriam, porque normalizar_linha troca dígito por "#"
    assert paginas[0].texto == "meio um\nCab\nfim um"


def test_ignora_paginas_nao_extraidas_e_vazias_na_contagem():
    paginas = [
        _p(1, "Cab\na"), _p(2, "Cab\nb"), _p(3, "Cab\nc"),
        Pagina(4, ["escaneado"], "[não extraído: página sem camada de texto, provável escaneado]"),
        Pagina(5, ["vazia"], VAZIA),
    ]
    removidos = remover_repetidos(paginas, detectar_repetidos(paginas))
    assert removidos == ["Cab"]
    assert paginas[3].texto.startswith("[não extraído")
    assert paginas[4].texto == VAZIA
