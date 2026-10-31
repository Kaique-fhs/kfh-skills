"""Confere se um HTML de apresentação respeita cor e fonte do padrão SIAN.

Uso: python conferir.py <arquivo.html>
Sai com 1 se houver cor ou fonte fora do padrão; senão imprime OK e sai com 0.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

OFICIAIS_HEX = {"#24286E", "#FF6934", "#94958B", "#C7C3BD", "#FFFFFF"}
OFICIAIS_RGB = {(36, 40, 110), (255, 105, 52), (148, 149, 139), (199, 195, 189), (255, 255, 255)}
FONTES_OK = {"supreme", "sans-serif", "inherit"}

_COR = re.compile(r"#[0-9a-fA-F]{3,8}(?![\w-])|(?:rgba?|hsla?)\([^)]*\)", re.IGNORECASE)
_COMENTARIO = re.compile(r"/\*(?!\s*viewport-base:).*?\*/", re.DOTALL)
_VIEWPORT = re.compile(
    r"/\*\s*viewport-base:inicio\s*\*/.*?/\*\s*viewport-base:fim\s*\*/", re.DOTALL
)
_DATA_URI = re.compile(r"data:[^\"'()\s]*", re.IGNORECASE)
_STYLE_TAG = re.compile(r"<style\b[^>]*>(.*?)</style>", re.DOTALL | re.IGNORECASE)
_STYLE_ATTR = re.compile(r"""\bstyle\s*=\s*(?:"([^"]*)"|'([^']*)')""", re.IGNORECASE)
_ROOT = re.compile(r":root\s*\{([^}]*)\}", re.IGNORECASE)
# declaração: nome: valor terminada em ; ou }  (um seletor termina em "{", não casa)
_DECLARACAO = re.compile(r"([\w-]+)\s*:\s*([^;{}]*)(?:;|(?=\}))")
_TAMANHO = re.compile(
    r"(?<![\w.-])(?:\d*\.?\d+(?:px|pt|em|rem|%|vw|vh|vmin|vmax|ch|ex)|\w+\([^)]*\))(?:/\S+)?\s+"
)


def _sem_ruido(html: str) -> str:
    """Remove URIs data: e comentários comuns (preserva os marcadores do viewport-base)."""
    return _COMENTARIO.sub("", _DATA_URI.sub("", html))


def _sem_viewport(html: str) -> str:
    return _VIEWPORT.sub("", html)


def _blocos_css(html: str) -> list[str]:
    """Trechos de CSS: conteúdo de <style> e atributos style=""."""
    blocos = _STYLE_TAG.findall(html)
    for aspas_duplas, aspas_simples in _STYLE_ATTR.findall(html):
        blocos.append("{" + (aspas_duplas or aspas_simples) + "}")
    return blocos


def _declaracoes(css: str) -> list[tuple[str, str]]:
    return [(n.lower(), v.strip()) for n, v in _DECLARACAO.findall(css)]


def cores_literais(html: str) -> list[str]:
    """Cores literais em declarações CSS, fora do :root, do viewport-base e de data:."""
    html = _sem_viewport(_sem_ruido(html))
    achadas: list[str] = []
    for bloco in _blocos_css(html):
        bloco = _ROOT.sub("", bloco)
        for _, valor in _declaracoes(bloco):
            achadas.extend(_COR.findall(valor))
    return achadas


def _cor_oficial(cor: str) -> bool:
    if cor.startswith("#"):
        hexa = cor[1:]
        if len(hexa) in (3, 4):
            hexa = "".join(c * 2 for c in hexa)
        if len(hexa) not in (6, 8):
            return False
        return ("#" + hexa[:6]).upper() in OFICIAIS_HEX
    if cor.lower().startswith("rgb"):
        numeros = re.findall(r"[\d.]+%?", cor[cor.index("(") + 1 :])
        try:
            rgb = tuple(round(float(n)) for n in numeros[:3])
        except ValueError:
            return False
        return len(rgb) == 3 and rgb in OFICIAIS_RGB
    return False  # hsl/hsla nunca é oficial


def paleta_root_invalida(html: str) -> list[str]:
    """Cores literais dentro de :root que não são uma das cinco oficiais."""
    html = _sem_viewport(_sem_ruido(html))
    invalidas: list[str] = []
    for bloco in _blocos_css(html):
        for raiz in _ROOT.findall(bloco):
            for _, valor in _declaracoes("{" + raiz + "}"):
                invalidas.extend(c for c in _COR.findall(valor) if not _cor_oficial(c))
    return invalidas


def _familias(valor: str) -> list[str]:
    partes = [p.strip().strip("\"'").strip() for p in valor.split(",")]
    return [p for p in partes if p and not p.lower().startswith("var(")]


def fontes_invalidas(html: str) -> list[str]:
    """Famílias de font-family e do atalho font: fora de Supreme/sans-serif/inherit."""
    html = _sem_viewport(_sem_ruido(html))
    invalidas: list[str] = []
    for bloco in _blocos_css(html):
        for nome, valor in _declaracoes(bloco):
            if nome == "font-family":
                familias = _familias(valor)
            elif nome == "font":
                achou = _TAMANHO.search(valor)
                familias = _familias(valor[achou.end() :]) if achou else []
                if not achou and valor.lower() == "inherit":
                    familias = []
            else:
                continue
            invalidas.extend(f for f in familias if f.lower() not in FONTES_OK)
    return invalidas


def main(argv: list[str]) -> int:
    if len(argv) != 1:
        print("Uso: python conferir.py <arquivo.html>")
        return 2
    html = Path(argv[0]).read_text(encoding="utf-8")
    problemas = (
        [f"cor fora do :root: {c}" for c in cores_literais(html)]
        + [f"cor não oficial no :root: {c}" for c in paleta_root_invalida(html)]
        + [f"fonte fora do padrão: {f}" for f in fontes_invalidas(html)]
    )
    if not problemas:
        print("OK")
        return 0
    for p in problemas:
        print(p)
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
