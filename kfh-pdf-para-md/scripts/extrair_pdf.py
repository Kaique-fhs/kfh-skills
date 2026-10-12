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


# ---------- página ----------

@dataclass
class Pagina:
    numero: int
    tipos: list[str]
    texto: str
    tabelas: list[str] = field(default_factory=list)

    @property
    def extraida(self) -> bool:
        return "escaneado" not in self.tipos


def detectar_colunas(page) -> float | None:
    """Devolve o x do meio da calha entre duas colunas, ou None.

    Divide a página em FAIXAS faixas verticais e conta quantas palavras cruzam cada faixa.
    Calha = faixa entre 35% e 65% da largura cruzada por menos de LIMIAR_CALHA das palavras,
    com pelo menos MIN_LADO das palavras de cada lado.
    """
    palavras = page.extract_words()
    if len(palavras) < 10:
        return None
    x_min = float(page.bbox[0])
    largura = float(page.width)
    cruzam = [0] * FAIXAS

    def faixa(x: float) -> int:
        return min(max(int((x - x_min) / largura * FAIXAS), 0), FAIXAS - 1)

    for w in palavras:
        for i in range(faixa(w["x0"]), faixa(w["x1"]) + 1):
            cruzam[i] += 1
    total = len(palavras)
    for i in range(int(FAIXAS * 0.35), int(FAIXAS * 0.65) + 1):
        if cruzam[i] / total >= LIMIAR_CALHA:
            continue
        x_calha = x_min + (i + 0.5) * largura / FAIXAS
        esq = sum(1 for w in palavras if w["x1"] <= x_calha) / total
        dir_ = sum(1 for w in palavras if w["x0"] >= x_calha) / total
        if esq >= MIN_LADO and dir_ >= MIN_LADO:
            return x_calha
    return None


def extrair_pagina(page) -> Pagina:
    n = page.page_number
    bruto = (page.extract_text() or "").strip()
    if len(bruto) < MIN_CHARS_TEXTO:
        if page.images:
            return Pagina(n, ["escaneado"], ESCANEADO)
        if not bruto:
            return Pagina(n, ["vazia"], VAZIA)

    tipos: list[str] = []
    tabelas_md: list[str] = []
    corpo = page
    for t in page.find_tables():
        linhas = t.extract()
        if len(linhas) >= 2 and max(len(l) for l in linhas) >= 2:
            tabelas_md.append(tabela_para_markdown(linhas))
            corpo = corpo.outside_bbox(t.bbox)
    if tabelas_md:
        tipos.append("tabelas")

    x_calha = detectar_colunas(corpo)
    if x_calha is not None:
        tipos.append("coluna-dupla")
        x0, top, x1, bottom = corpo.bbox
        esq = corpo.crop((x0, top, x_calha, bottom)).extract_text() or ""
        dir_ = corpo.crop((x_calha, top, x1, bottom)).extract_text() or ""
        texto = esq.rstrip() + "\n" + dir_.lstrip()
    else:
        texto = corpo.extract_text() or ""

    if not tipos:
        tipos.append("texto")
    return Pagina(n, tipos, limpar_texto(texto), tabelas_md)


# ---------- cabeçalho e rodapé repetidos ----------

def normalizar_linha(linha: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"\d", "#", linha)).strip().lower()


def _paginas_com_texto(paginas: list[Pagina]) -> list[Pagina]:
    return [p for p in paginas if p.extraida and p.texto != VAZIA]


def _indices_de_borda(linhas: list[str]) -> set[int]:
    nao_vazias = [i for i, l in enumerate(linhas) if l.strip()]
    return set(nao_vazias[:2] + nao_vazias[-2:])


def detectar_repetidos(paginas: list[Pagina]) -> dict[str, str]:
    """Linhas de borda (2 primeiras + 2 últimas) que aparecem em mais de 50% das páginas (mínimo 3)."""
    com_texto = _paginas_com_texto(paginas)
    if len(com_texto) <= 2:
        return {}
    contagem: Counter[str] = Counter()
    originais: dict[str, str] = {}
    for p in com_texto:
        linhas = p.texto.splitlines()
        candidatas = {linhas[i] for i in _indices_de_borda(linhas)}
        for l in candidatas:
            if re.fullmatch(r"\d+", l.strip()):
                continue  # numeração é tratada à parte
            chave = normalizar_linha(l)
            contagem[chave] += 1
            originais.setdefault(chave, l)
    minimo = max(3, len(com_texto) // 2 + 1)
    return {k: originais[k] for k, c in contagem.items() if c >= minimo}


def remover_repetidos(paginas: list[Pagina], repetidos: dict[str, str]) -> list[str]:
    """Remove das bordas as linhas repetidas e a numeração de página. Devolve o que removeu."""
    com_texto = _paginas_com_texto(paginas)
    if len(com_texto) <= 2:
        return []
    removidos: list[str] = []
    numeracao = False
    for p in com_texto:
        linhas = p.texto.splitlines()
        bordas = _indices_de_borda(linhas)
        novas: list[str] = []
        for i, l in enumerate(linhas):
            if i in bordas:
                if re.fullmatch(r"\d+", l.strip()):
                    numeracao = True
                    continue
                chave = normalizar_linha(l)
                if chave in repetidos:
                    if repetidos[chave] not in removidos:
                        removidos.append(repetidos[chave])
                    continue
            novas.append(l)
        p.texto = "\n".join(novas).strip()
    if numeracao:
        removidos.append("numeração de página")
    return removidos
