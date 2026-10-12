#!/usr/bin/env python
"""kfh-pdf-para-md: extrai PDFs para Markdown fiel, página a página, com marcador de página.

Uso:
  python extrair_pdf.py <pdf | pasta> [<pdf | pasta> ...] [--saida DIR] [--sobrescrever]

Um .md por PDF, em --saida (padrão: <pasta do PDF>/extraido/). Não faz OCR, não resume,
não inventa: página sem camada de texto sai marcada como não extraída.
"""
from __future__ import annotations

import argparse
import datetime as dt
import re
import sys
import tempfile
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path

import pdfplumber

ESCANEADO = "[não extraído: página sem camada de texto, provável escaneado]"
VAZIA = "[página sem conteúdo]"
MIN_CHARS_TEXTO = 20
FAIXAS = 40  # faixas verticais para detectar a calha entre colunas
LIMIAR_CALHA = 0.01  # fração máxima de palavras cruzando a faixa da calha
MIN_LADO = 0.20  # fração mínima de palavras em cada lado da calha


# ---------- funções puras ----------

def juntar_hifenizacao(texto: str) -> str:
    """Junta 'palavra-\\nresto' em 'palavraresto' só quando o próximo caractere é letra minúscula."""

    def _junta(m: re.Match) -> str:
        return m.group(1) + m.group(2) if m.group(2).islower() else m.group(0)

    return re.sub(r"(\w)-\n(\w)", _junta, texto)


def limpar_texto(texto: str) -> str:
    """Espaços múltiplos -> um; linhas vazias repetidas -> uma; hifenização de quebra juntada."""
    texto = juntar_hifenizacao(texto)
    saida: list[str] = []
    vazia_antes = False
    for linha in texto.splitlines():
        linha = re.sub(r"[ \t]+", " ", linha).strip()
        if linha == "":
            if vazia_antes:
                continue
            vazia_antes = True
        else:
            vazia_antes = False
        saida.append(linha)
    return "\n".join(saida).strip()


def tabela_para_markdown(linhas: list[list[str | None]]) -> str:
    def celula(c: str | None) -> str:
        return (c or "").replace("\n", " ").replace("|", "\\|").strip()

    ncol = max(len(l) for l in linhas)
    norm = [[celula(c) for c in l] + [""] * (ncol - len(l)) for l in linhas]
    cab = "| " + " | ".join(norm[0]) + " |"
    sep = "| " + " | ".join(["---"] * ncol) + " |"
    corpo = ["| " + " | ".join(l) + " |" for l in norm[1:]]
    return "\n".join([cab, sep, *corpo])


def nome_seguro(nome: str) -> str:
    return nome.replace("-->", "_").replace("|", "_")


def marcador(nome: str, n: int) -> str:
    return f"<!-- {nome_seguro(nome)} | p. {n} -->"
