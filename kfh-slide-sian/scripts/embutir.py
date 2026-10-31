"""Embute fonte, logos, canto e CSS de viewport no rascunho HTML da apresentação SIAN."""
from __future__ import annotations

import base64
import re
import sys
import unicodedata
from pathlib import Path

RAIZ_SKILL = Path(__file__).resolve().parents[1]

ARQUIVOS_MARCA = (
    "fontes/Supreme-Variable.woff2",
    "logos/sian-logo-original.png",
    "logos/sian-logo-branca.png",
    "grafismos/sian-icone-canto.png",
)


class DependenciaAusente(Exception):
    pass


class MarcadorDesconhecido(Exception):
    pass


def achar_marca(raiz_skill: Path, home: Path) -> Path:
    candidatas = [
        raiz_skill.parent / "kfh-marca-sian" / "assets",
        home / ".claude" / "skills" / "kfh-marca-sian" / "assets",
    ]
    faltas: list[str] = []
    for assets in candidatas:
        faltam = [a for a in ARQUIVOS_MARCA if not (assets / a).is_file()]
        if not faltam:
            return assets
        if not faltas:
            faltas = [f"{assets / a}" for a in faltam]
    raise DependenciaAusente("instale a kfh-marca-sian: faltam " + ", ".join(faltas))


def _versao(pasta: Path) -> tuple[int, ...] | None:
    partes = pasta.name.split(".")
    if all(p.isdigit() for p in partes):
        return tuple(int(p) for p in partes)
    return None


def achar_viewport_base(home: Path) -> Path:
    base = home / ".claude" / "plugins" / "cache" / "frontend-slides" / "frontend-slides"
    candidatas = []
    if base.is_dir():
        for pasta in base.iterdir():
            versao = _versao(pasta)
            css = pasta / "skills" / "frontend-slides" / "viewport-base.css"
            if versao is not None and css.is_file():
                candidatas.append((versao, css))
    if not candidatas:
        raise DependenciaAusente("instale o plugin frontend-slides")
    return max(candidatas, key=lambda c: c[0])[1]


def data_uri(arquivo: Path, mime: str) -> str:
    return f"data:{mime};base64," + base64.b64encode(arquivo.read_bytes()).decode("ascii")


def chave_edicao(saida: Path) -> str:
    nome = unicodedata.normalize("NFKD", saida.stem)
    nome = "".join(c for c in nome if not unicodedata.combining(c)).lower()
    nome = re.sub(r"[^a-z0-9]+", "-", nome).strip("-")
    return "sian-" + nome


def embutir(rascunho: str, assets: Path, viewport: Path, saida: Path) -> str:
    css = viewport.read_text(encoding="utf-8")
    trocas = {
        "{{VIEWPORT_BASE}}": None,
        "{{FONTE_SUPREME}}": data_uri(assets / "fontes/Supreme-Variable.woff2", "font/woff2"),
        "{{LOGO_ORIGINAL}}": data_uri(assets / "logos/sian-logo-original.png", "image/png"),
        "{{LOGO_BRANCA}}": data_uri(assets / "logos/sian-logo-branca.png", "image/png"),
        "{{CANTO}}": data_uri(assets / "grafismos/sian-icone-canto.png", "image/png"),
        "{{CHAVE_EDICAO}}": chave_edicao(saida),
    }
    texto = rascunho.replace(
        "/* {{VIEWPORT_BASE}} */",
        "/* viewport-base:inicio */\n" + css + "\n/* viewport-base:fim */",
    )
    for marcador, valor in trocas.items():
        if valor is not None:
            texto = texto.replace(marcador, valor)
    sobras = sorted(set(re.findall(r"\{\{([A-Z_]+)\}\}", texto)))
    if sobras:
        raise MarcadorDesconhecido("marcadores desconhecidos: " + ", ".join(sobras))
    return texto


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("uso: python embutir.py <rascunho.html> <saida.html>", file=sys.stderr)
        return 1
    rascunho, saida = Path(argv[0]), Path(argv[1])
    try:
        texto = rascunho.read_text(encoding="utf-8")
        assets = achar_marca(RAIZ_SKILL, Path.home())
        viewport = achar_viewport_base(Path.home())
        resultado = embutir(texto, assets, viewport, saida)
    except (DependenciaAusente, MarcadorDesconhecido, OSError) as erro:
        print(f"ERRO: {erro}", file=sys.stderr)
        return 1
    saida.write_text(resultado, encoding="utf-8")
    print(f"OK: {saida}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
