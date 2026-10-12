"""Gera o zip de uma skill deste repositorio para upload no claude.ai.

Uso: python empacotar.py <nome-da-skill>
Saida: dist/<nome-da-skill>.zip, com a pasta da skill na raiz do zip
(<nome-da-skill>/SKILL.md, ...). Caminhos internos sempre com barra normal.
"""
import sys
import zipfile
from pathlib import Path

IGNORAR = {"__pycache__", ".pytest_cache", ".DS_Store", "dist"}


def empacotar(pasta: Path, destino: Path) -> Path:
    if not (pasta / "SKILL.md").is_file():
        raise SystemExit(f"Skill invalida: {pasta / 'SKILL.md'} nao existe")
    destino.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(destino, "w", zipfile.ZIP_DEFLATED) as z:
        for arquivo in sorted(pasta.rglob("*")):
            if not arquivo.is_file():
                continue
            relativo = arquivo.relative_to(pasta)
            if IGNORAR & set(relativo.parts) or arquivo.suffix == ".pyc":
                continue
            z.write(arquivo, f"{pasta.name}/{relativo.as_posix()}")
    return destino


def main(argv):
    if len(argv) != 2:
        print(__doc__)
        return 2
    raiz = Path(__file__).resolve().parent
    pasta = raiz / argv[1]
    destino = raiz / "dist" / f"{pasta.name}.zip"
    print(f"OK: {empacotar(pasta, destino)}")
    with zipfile.ZipFile(destino) as z:
        print("\n".join(z.namelist()))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
