#!/usr/bin/env python
"""kfh-md-buscar: confere se cada trecho citado em achados.md existe na página indicada do .md de origem.

Uso:
  python verificar_citacoes.py <achados.md> [--pasta DIR] [--marcar]

Sem --marcar só relata (código 1 se houver falha). Com --marcar troca o status das linhas que
falharam por "❌ citação não confere" e grava 'verificado:' no frontmatter.
"""
from __future__ import annotations

import argparse
import datetime as dt
import re
import sys
from dataclasses import dataclass
from pathlib import Path

RE_MARCADOR = re.compile(r"^<!-- (.+?) \| p\. (\d+) -->[ \t]*$", re.M)
STATUS_VERIFICAVEIS = {"encontrado", "parcial", "conflitante"}
STATUS_NAO_ENCONTRADO = {"não encontrado", "nao encontrado"}
FALHA = "❌ citação não confere"
COLUNAS_PAGINA = ("página", "pagina")


@dataclass
class Registro:
    campo: str
    resposta: str
    arquivo: str
    pagina: str
    trecho: str
    status: str
    indice: int  # índice da linha no arquivo achados.md


# ---------- leitura ----------

def dividir_celulas(linha: str) -> list[str]:
    s = linha.strip()
    if s.startswith("|"):
        s = s[1:]
    if s.endswith("|") and not s.endswith("\\|"):
        s = s[:-1]
    partes = re.split(r"(?<!\\)\|", s)
    return [p.replace("\\|", "|").strip() for p in partes]


def _e_separador(celulas: list[str]) -> bool:
    return all(re.fullmatch(r":?-{3,}:?", c) for c in celulas if c) and any(celulas)


def ler_achados(texto: str) -> tuple[list[str], list[str], list[Registro]]:
    linhas = texto.splitlines()
    cabecalho: list[str] = []
    registros: list[Registro] = []
    for i, l in enumerate(linhas):
        if not l.lstrip().startswith("|"):
            continue
        celulas = dividir_celulas(l)
        if not cabecalho:
            cabecalho = [c.lower() for c in celulas]
            continue
        if _e_separador(celulas):
            continue
        d = dict(zip(cabecalho, celulas))
        pagina = next((d[c] for c in COLUNAS_PAGINA if c in d), "")
        registros.append(Registro(
            d.get("campo", ""), d.get("resposta", ""), d.get("arquivo", ""), pagina,
            d.get("trecho literal", d.get("trecho", "")), d.get("status", ""), i,
        ))
    return linhas, cabecalho, registros


# ---------- verificação ----------

def normalizar(t: str) -> str:
    for a, b in (("“", '"'), ("”", '"'), ("„", '"'), ("‘", "'"), ("’", "'")):
        t = t.replace(a, b)
    t = t.strip()
    if len(t) >= 2 and t[0] == '"' and t[-1] == '"':
        t = t[1:-1]
    t = re.sub(r"(\w)-\s+(\w)", r"\1\2", t)
    return re.sub(r"\s+", " ", t).strip().lower()


def blocos_por_pagina(md: str) -> dict[int, str]:
    marcas = list(RE_MARCADOR.finditer(md))
    blocos: dict[int, str] = {}
    for i, m in enumerate(marcas):
        fim = marcas[i + 1].start() if i + 1 < len(marcas) else len(md)
        n = int(m.group(2))
        blocos[n] = blocos.get(n, "") + md[m.end():fim]
    return blocos


def resolver_arquivo(nome: str, bases: list[Path]) -> Path | None:
    for b in bases:
        c = b / nome
        if c.is_file():
            return c
    p = Path(nome)
    return p if p.is_file() else None


def verificar_registro(r: Registro, bases: list[Path], cache: dict[Path, dict[int, str] | None]) -> str:
    st = r.status.strip().lower()
    preenchido = any(x.strip() for x in (r.resposta, r.pagina, r.trecho))
    if st in STATUS_NAO_ENCONTRADO:
        return "status incoerente" if preenchido else "ok"
    if st.startswith("❌"):
        return "pendente de correção"
    if st not in STATUS_VERIFICAVEIS:
        return "status desconhecido"
    arq = resolver_arquivo(r.arquivo, bases)
    if arq is None:
        return "arquivo não existe"
    if arq not in cache:
        try:
            cache[arq] = blocos_por_pagina(arq.read_text(encoding="utf-8"))
        except (OSError, UnicodeDecodeError):
            cache[arq] = None
    blocos = cache[arq]
    if blocos is None:
        return "arquivo ilegível"
    if not blocos:
        return "arquivo sem marcador"
    if not r.pagina.strip().isdigit() or int(r.pagina) not in blocos:
        return "página não existe"
    if not r.trecho.strip():
        return "trecho vazio"
    if normalizar(r.trecho) in normalizar(blocos[int(r.pagina)]):
        return "ok"
    return "trecho não existe na página"


# ---------- marcação ----------

def _montar_linha(celulas: list[str]) -> str:
    return "| " + " | ".join(c.replace("|", "\\|") for c in celulas) + " |"


def marcar(linhas: list[str], cabecalho: list[str], registros: list[Registro], resultados: list[str]) -> list[str]:
    novas = list(linhas)
    idx_status = cabecalho.index("status")
    for r, res in zip(registros, resultados):
        if res == "ok":
            continue
        celulas = dividir_celulas(novas[r.indice])
        while len(celulas) <= idx_status:
            celulas.append("")
        celulas[idx_status] = FALHA
        novas[r.indice] = _montar_linha(celulas)
    carimbo = f"verificado: {dt.datetime.now().isoformat(timespec='seconds')}"
    if novas and novas[0].strip() == "---":
        fim = next((i for i in range(1, len(novas)) if novas[i].strip() == "---"), None)
        if fim is not None:
            for i in range(1, fim):
                if novas[i].startswith("verificado:"):
                    novas[i] = carimbo
                    break
            else:
                novas.insert(fim, carimbo)
            return novas
    return ["---", carimbo, "---", ""] + novas


# ---------- CLI ----------

def main(argv: list[str] | None = None) -> int:
    for fluxo in (sys.stdout, sys.stderr):
        try:
            fluxo.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass  # stdout substituído (pytest capsys) ou sem suporte
    ap = argparse.ArgumentParser(description="Confere se cada trecho citado em achados.md existe na página indicada.")
    ap.add_argument("achados", help="caminho do achados.md")
    ap.add_argument("--pasta", help="pasta onde estão os .md citados (padrão: pasta do achados.md)")
    ap.add_argument("--marcar", action="store_true", help="grava '❌ citação não confere' nas linhas que falharam")
    args = ap.parse_args(argv)

    caminho = Path(args.achados)
    if not caminho.is_file():
        print(f"erro: arquivo não existe: {caminho}", file=sys.stderr)
        return 1
    try:
        texto = caminho.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as e:
        print(f"erro: não foi possível ler {caminho}: {type(e).__name__}", file=sys.stderr)
        return 1
    linhas, cabecalho, registros = ler_achados(texto)
    if "status" not in cabecalho:
        print("erro: tabela sem coluna 'status'", file=sys.stderr)
        return 1

    bases: list[Path] = []
    if args.pasta:
        bases.append(Path(args.pasta))
    bases.append(caminho.parent)
    m = re.search(r"^pasta: (.+)$", texto, re.M)
    if m:
        bases.append(Path(m.group(1).strip()))

    cache: dict[Path, dict[int, str] | None] = {}
    resultados = [verificar_registro(r, bases, cache) for r in registros]

    print("| # | campo | arquivo | página | resultado |")
    print("| --- | --- | --- | --- | --- |")
    for n, (r, res) in enumerate(zip(registros, resultados), start=1):
        print(f"| {n} | {r.campo} | {r.arquivo} | {r.pagina or '-'} | {res} |")
    falhas = sum(1 for res in resultados if res != "ok")
    print(f"\n{len(resultados)} linhas, {falhas} falha(s).")

    if args.marcar:
        caminho.write_text("\n".join(marcar(linhas, cabecalho, registros, resultados)) + "\n", encoding="utf-8")
        print(f"achados.md atualizado: {falhas} linha(s) marcada(s) como citação não confere.")
    return 1 if falhas else 0


if __name__ == "__main__":
    sys.exit(main())
