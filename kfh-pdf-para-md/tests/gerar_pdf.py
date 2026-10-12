"""Gerador mínimo de PDF com texto (Helvetica, WinAnsi) e linhas, sem dependências.

Cada página é um dict: {"textos": [(x, y, "texto"), ...], "linhas": [(x1, y1, x2, y2), ...]}
Coordenadas em pontos, origem no canto inferior esquerdo. A4 = 595 x 842.
Validado: pdfplumber lê texto com acentos, intercala colunas em extract_text()
(o problema real) e detecta tabela desenhada com grade.
"""
from __future__ import annotations

LARGURA, ALTURA = 595, 842


def _esc(texto: str) -> bytes:
    b = texto.encode("cp1252", errors="replace")
    return b.replace(b"\\", b"\\\\").replace(b"(", b"\\(").replace(b")", b"\\)")


def _conteudo(pagina: dict) -> bytes:
    partes = [b"BT /F1 11 Tf"]
    for x, y, texto in pagina.get("textos", []):
        partes.append(f"1 0 0 1 {x} {y} Tm (".encode() + _esc(texto) + b") Tj")
    partes.append(b"ET")
    for x1, y1, x2, y2 in pagina.get("linhas", []):
        partes.append(f"{x1} {y1} m {x2} {y2} l S".encode())
    return b"\n".join(partes)


def gerar_pdf(paginas: list[dict]) -> bytes:
    objetos: list[bytes] = []
    n = len(paginas)
    kids = " ".join(f"{4 + 2 * i} 0 R" for i in range(n))
    objetos.append(b"<< /Type /Catalog /Pages 2 0 R >>")
    objetos.append(f"<< /Type /Pages /Kids [{kids}] /Count {n} >>".encode())
    objetos.append(b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica /Encoding /WinAnsiEncoding >>")
    for i, pagina in enumerate(paginas):
        conteudo = _conteudo(pagina)
        objetos.append(
            f"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 {LARGURA} {ALTURA}] "
            f"/Resources << /Font << /F1 3 0 R >> >> /Contents {5 + 2 * i} 0 R >>".encode()
        )
        objetos.append(f"<< /Length {len(conteudo)} >>\nstream\n".encode() + conteudo + b"\nendstream")
    saida = bytearray(b"%PDF-1.4\n")
    offsets = []
    for i, obj in enumerate(objetos, start=1):
        offsets.append(len(saida))
        saida += f"{i} 0 obj\n".encode() + obj + b"\nendobj\n"
    xref = len(saida)
    saida += f"xref\n0 {len(objetos) + 1}\n0000000000 65535 f \n".encode()
    for off in offsets:
        saida += f"{off:010d} 00000 n \n".encode()
    saida += f"trailer\n<< /Size {len(objetos) + 1} /Root 1 0 R >>\nstartxref\n{xref}\n%%EOF\n".encode()
    return bytes(saida)


def linhas_de_texto(x: float, y_topo: float, frases: list[str], passo: float = 14) -> list[tuple]:
    return [(x, y_topo - i * passo, f) for i, f in enumerate(frases)]


def grade(x: float, y_topo: float, larguras: list[float], n_linhas: int, altura_linha: float = 18) -> list[tuple]:
    xs = [x]
    for l in larguras:
        xs.append(xs[-1] + l)
    ys = [y_topo - i * altura_linha for i in range(n_linhas + 1)]
    linhas = [(xs[0], y, xs[-1], y) for y in ys]
    linhas += [(xx, ys[0], xx, ys[-1]) for xx in xs]
    return linhas
