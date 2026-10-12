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
import os
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

def juntar_hifenizacao(texto: str, vocabulario: set[str] | None = None) -> str:
    """Junta 'palavra-\\nresto' em 'palavraresto'.

    Sem vocabulário: junta quando o próximo caractere é letra minúscula.
    Com vocabulário (palavras minúsculas do documento): junta só quando a forma junta está nele;
    caso contrário (ex.: 'qui-quadrado') deixa hífen e quebra como extraídos.
    """
    if vocabulario is None:
        def _junta(m: re.Match) -> str:
            return m.group(1) + m.group(2) if m.group(2).islower() else m.group(0)

        return re.sub(r"(\w)-\n(\w)", _junta, texto)

    def _junta_voc(m: re.Match) -> str:
        junta = m.group(1) + m.group(2)
        return junta if junta.lower() in vocabulario else m.group(0)

    return re.sub(r"(\w+)-\n(\w+)", _junta_voc, texto)


def limpar_texto(texto: str, vocabulario: set[str] | None = None) -> str:
    """Espaços múltiplos -> um; linhas vazias repetidas -> uma; hifenização de quebra juntada."""
    texto = juntar_hifenizacao(texto, vocabulario)
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


GAP_SEGMENTO = 10  # vão (pt) que separa segmentos de uma mesma linha
LARGA = 0.60  # linha com mais de 60% da largura da página é "larga" (título, resumo)


def linhas_largas(page) -> list[dict]:
    """Segmentos de linha mais largos que LARGA da página, em ordem de leitura.

    Agrupa palavras por altura (tolerância de 3pt) e quebra a linha onde há vão maior que
    GAP_SEGMENTO (uma calha): duas colunas lado a lado não formam uma linha larga.
    """
    palavras = sorted(page.extract_words(), key=lambda w: (w["top"], w["x0"]))
    grupos: list[list[dict]] = []
    for w in palavras:
        if grupos and abs(w["top"] - grupos[-1][0]["top"]) <= 3:
            grupos[-1].append(w)
        else:
            grupos.append([w])
    limite = LARGA * float(page.width)
    saida: list[dict] = []
    for g in grupos:
        g.sort(key=lambda w: w["x0"])
        segmentos: list[list[dict]] = [[g[0]]]
        for w in g[1:]:
            if w["x0"] - segmentos[-1][-1]["x1"] > GAP_SEGMENTO:
                segmentos.append([w])
            else:
                segmentos[-1].append(w)
        for seg in segmentos:
            x0, x1 = seg[0]["x0"], seg[-1]["x1"]
            if x1 - x0 > limite:
                saida.append({"x0": x0, "x1": x1, "top": min(w["top"] for w in seg),
                              "bottom": max(w["bottom"] for w in seg), "text": " ".join(w["text"] for w in seg)})
    return sorted(saida, key=lambda l: l["top"])


def _em_linha(w: dict, l: dict) -> bool:
    return w["x0"] >= l["x0"] - 1 and w["x1"] <= l["x1"] + 1 and w["top"] >= l["top"] - 1 and w["bottom"] <= l["bottom"] + 1


def detectar_colunas(page) -> float | None:
    """Devolve o x do meio da calha entre duas colunas, ou None.

    Divide a página em FAIXAS faixas verticais e conta quantas palavras cruzam cada faixa.
    Calha = faixa entre 35% e 65% da largura cruzada por menos de LIMIAR_CALHA das palavras,
    com pelo menos MIN_LADO das palavras de cada lado. Palavras de linhas largas (título,
    resumo) ficam fora da contagem.
    """
    largas = linhas_largas(page)
    palavras = [w for w in page.extract_words() if not any(_em_linha(w, l) for l in largas)]
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


def extrair_pagina(page, vocabulario: set[str] | None = None) -> Pagina:
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
        largas = linhas_largas(corpo)
        resto = corpo
        for l in largas:
            resto = resto.outside_bbox((l["x0"], l["top"], l["x1"], l["bottom"]))
        x0, top, x1, bottom = resto.bbox
        blocos = [
            "\n".join(l["text"] for l in largas),
            resto.crop((x0, top, x_calha, bottom)).extract_text() or "",
            resto.crop((x_calha, top, x1, bottom)).extract_text() or "",
        ]
        # cada bloco é limpo à parte: hífen no fim de uma coluna não se junta à outra
        texto = "\n".join(b for b in (limpar_texto(b, vocabulario) for b in blocos) if b)
    else:
        texto = limpar_texto(corpo.extract_text() or "", vocabulario)

    if not tipos:
        tipos.append("texto")
    return Pagina(n, tipos, texto, tabelas_md)


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


# ---------- arquivo ----------

def tipo_arquivo(paginas: list[Pagina]) -> str:
    tipos = {"+".join(p.tipos) for p in paginas if "vazia" not in p.tipos}
    if not tipos:
        return "vazia"
    return tipos.pop() if len(tipos) == 1 else "misto"


def montar_md(caminho: Path, paginas: list[Pagina], removidos: list[str]) -> str:
    nome = caminho.name
    nao = [p.numero for p in paginas if not p.extraida]
    tipos_pg = ", ".join(f"{p.numero}: {'+'.join(p.tipos)}" for p in paginas)
    rem = ", ".join('"' + r.replace('"', "'") + '"' for r in removidos)
    front = [
        "---",
        f"fonte: {nome}",
        f"caminho: {caminho.absolute().as_posix()}",  # absolute(), não resolve(): nome com '|' quebra resolve() no Windows
        f"paginas: {len(paginas)}",
        f"extraido_em: {dt.datetime.now().isoformat(timespec='seconds')}",
        f"ferramenta: kfh-pdf-para-md (pdfplumber {pdfplumber.__version__})",
        f"tipo_detectado: {tipo_arquivo(paginas)}",
        f"tipos_por_pagina: {{{tipos_pg}}}",
        f"paginas_nao_extraidas: [{', '.join(map(str, nao))}]",
        f"removido_repetido: [{rem}]",
        "---",
        "",
    ]
    corpo: list[str] = []
    for p in paginas:
        corpo.append(marcador(nome, p.numero))
        corpo.append(p.texto)
        for k, t in enumerate(p.tabelas, start=1):
            corpo.append("")
            corpo.append(f"<!-- tabela {k} -->")
            corpo.append(t)
        corpo.append("")
    return "\n".join(front + corpo).rstrip() + "\n"


def abrir_pdf(caminho: Path):
    """Abre com pdfplumber; se falhar, tenta desbloquear com pypdf e senha vazia.

    Devolve (pdf, caminho_temporario_ou_None). Lança ValueError("protegido") ou ValueError("invalido").
    """
    try:
        return pdfplumber.open(str(caminho)), None
    except Exception:
        pass
    try:
        from pypdf import PdfReader, PdfWriter

        leitor = PdfReader(str(caminho))
        if leitor.is_encrypted and not leitor.decrypt(""):
            raise ValueError("protegido")
        tmp = tempfile.NamedTemporaryFile(suffix=".pdf", delete=False)
        try:
            PdfWriter(clone_from=leitor).write(tmp)
            tmp.close()
            return pdfplumber.open(tmp.name), Path(tmp.name)
        except Exception:
            tmp.close()
            Path(tmp.name).unlink(missing_ok=True)
            raise
    except ValueError:
        raise
    except Exception as e:
        raise ValueError("invalido") from e


@dataclass
class Resumo:
    fonte: str
    saida: Path | None
    paginas: int
    tipo: str
    nao_extraidas: list[int]
    observacoes: list[str]
    erro: str | None = None


def processar_pdf(caminho: Path, saida_dir: Path, sobrescrever: bool) -> Resumo:
    destino = saida_dir / (caminho.stem + ".md")
    destino_real, saida_real = destino, saida_dir
    if os.name == "nt" and len(str(destino.absolute())) >= 250:
        saida_real = Path("\\\\?\\" + str(saida_dir.absolute()))  # prefixo de caminho longo
        destino_real = saida_real / destino.name
    if destino_real.exists() and not sobrescrever:
        return Resumo(caminho.name, destino, 0, "-", [], ["já existia; pulado (use --sobrescrever)"])
    try:
        pdf, tmp = abrir_pdf(caminho)
    except ValueError as e:
        motivo = "protegido" if str(e) == "protegido" else "arquivo inválido"
        return Resumo(caminho.name, None, 0, "-", [], [], erro=f"não extraído: {motivo}")
    try:
        with pdf:
            vocabulario: set[str] = set()
            for pg in pdf.pages:
                vocabulario.update(re.findall(r"\w+", (pg.extract_text() or "").lower()))
            paginas = [extrair_pagina(pg, vocabulario) for pg in pdf.pages]
    except Exception as e:
        return Resumo(caminho.name, None, 0, "-", [], [], erro=f"não extraído: falha ao ler páginas ({type(e).__name__})")
    finally:
        if tmp is not None:
            tmp.unlink(missing_ok=True)
    if not paginas:
        return Resumo(caminho.name, None, 0, "-", [], [], erro="não extraído: arquivo inválido")
    removidos = remover_repetidos(paginas, detectar_repetidos(paginas))
    nao = [p.numero for p in paginas if not p.extraida]
    try:
        saida_real.mkdir(parents=True, exist_ok=True)
        destino_real.write_text(montar_md(caminho, paginas, removidos), encoding="utf-8")
    except OSError as e:
        n_car = len(str(destino.absolute()))
        extra = f"caminho com {n_car} caracteres; o Windows limita a 260, use --saida com pasta curta" if n_car >= 250 else type(e).__name__
        return Resumo(caminho.name, None, len(paginas), tipo_arquivo(paginas), nao, [],
                      erro=f"não extraído: não foi possível gravar em {destino.as_posix()} ({extra})")
    observacoes = [f"removido: {r}" for r in removidos]
    return Resumo(caminho.name, destino, len(paginas), tipo_arquivo(paginas), nao, observacoes)


# ---------- CLI ----------

def coletar_pdfs(entradas: list[str]) -> tuple[list[Path], list[str]]:
    pdfs: list[Path] = []
    mensagens: list[str] = []
    for e in entradas:
        p = Path(e)
        if p.is_dir():
            achados = sorted(q for q in p.iterdir() if q.suffix.lower() == ".pdf")
            if not achados:
                mensagens.append(f"aviso: pasta sem PDF: {p}")
            pdfs.extend(achados)
        elif p.is_file():
            pdfs.append(p)
        else:
            mensagens.append(f"erro: caminho não existe: {p}")
    return pdfs, mensagens


def resumo_markdown(resumos: list[Resumo]) -> str:
    linhas = [
        "| arquivo | páginas | tipo | não extraídas | saída | observações |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for r in resumos:
        obs = r.erro if r.erro else ("; ".join(r.observacoes) or "-")
        nao = ", ".join(map(str, r.nao_extraidas)) or "-"
        saida = r.saida.as_posix() if r.saida else "-"
        linhas.append(f"| {r.fonte} | {r.paginas} | {r.tipo} | {nao} | {saida} | {obs} |")
    return "\n".join(linhas)


def main(argv: list[str] | None = None) -> int:
    for fluxo in (sys.stdout, sys.stderr):
        try:
            fluxo.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass  # stdout substituído (pytest capsys) ou sem suporte
    ap = argparse.ArgumentParser(description="Extrai PDFs para Markdown fiel, com marcador de página. Não faz OCR.")
    ap.add_argument("entradas", nargs="+", help="arquivos .pdf ou pastas (sem recursão)")
    ap.add_argument("--saida", help="pasta de saída (padrão: <pasta do PDF>/extraido/)")
    ap.add_argument("--sobrescrever", action="store_true", help="regrava .md que já existe")
    args = ap.parse_args(argv)

    pdfs, mensagens = coletar_pdfs(args.entradas)
    codigo = 1 if any(m.startswith("erro") for m in mensagens) else 0
    for m in mensagens:
        print(m, file=sys.stderr)

    resumos: list[Resumo] = []
    for pdf in pdfs:
        saida_dir = Path(args.saida) if args.saida else pdf.parent / "extraido"
        r = processar_pdf(pdf, saida_dir, args.sobrescrever)
        if r.erro:
            codigo = 1
            print(f"erro: {r.fonte}: {r.erro}", file=sys.stderr)
        resumos.append(r)
    print(resumo_markdown(resumos))
    return codigo


if __name__ == "__main__":
    sys.exit(main())
