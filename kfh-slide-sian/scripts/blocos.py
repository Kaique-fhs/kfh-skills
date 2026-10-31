"""Leitura dos blocos de slide (blocos/<nome>.md) e conferência de classes."""
from __future__ import annotations

import re
from pathlib import Path

_CAMPOS = {
    "serve": "Serve para",
    "quando": "Quando usar",
    "quando_nao": "Quando não usar",
    "passos": "Passos de clique",
    "editaveis": "Editáveis",
}


def _campo(texto: str, rotulo: str) -> str:
    m = re.search(rf"^- \*\*{re.escape(rotulo)}:\*\*[ \t]*(.+)$", texto, re.MULTILINE)
    if not m:
        raise ValueError(f"campo ausente: {rotulo}")
    valor = m.group(1).strip()
    if rotulo == "Editáveis":
        valor = valor.strip("`").strip()
    return valor


def _codigo(texto: str, titulo: str, linguagem: str) -> str:
    m = re.search(
        rf"^## {titulo}\s*\n```{linguagem}\n(.*?)\n```", texto, re.MULTILINE | re.DOTALL
    )
    if not m:
        raise ValueError(f"campo ausente: {titulo}")
    return m.group(1)


def ler_bloco(caminho: Path) -> dict:
    texto = Path(caminho).read_text(encoding="utf-8")
    titulo = re.search(r"^# (.+)$", texto, re.MULTILINE)
    if not titulo:
        raise ValueError("campo ausente: Nome")
    bloco = {"nome": titulo.group(1).strip()}
    for chave, rotulo in _CAMPOS.items():
        bloco[chave] = _campo(texto, rotulo)
    bloco["css"] = _codigo(texto, "CSS", "css")
    bloco["html"] = _codigo(texto, "HTML", "html")
    return bloco


def classes_definidas(css: str) -> set[str]:
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.DOTALL)
    css = re.sub(r"\"[^\"]*\"|'[^']*'", "", css)
    seletores = re.findall(r"([^{}]+)\{", css)
    return {c for s in seletores for c in re.findall(r"\.([A-Za-z_][\w-]*)", s)}


def classes_usadas(html: str) -> set[str]:
    usadas: set[str] = set()
    for valor in re.findall(r"\bclass\s*=\s*\"([^\"]*)\"", html):
        usadas.update(valor.split())
    return usadas
