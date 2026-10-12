---
name: kfh-pdf-para-md
description: Usar quando o usuário tem um ou mais arquivos PDF e quer o conteúdo em Markdown fiel, com a página de origem de cada trecho, antes de ler, resumir, catalogar ou buscar. Aciona em pedidos como "extrai esse PDF", "converte os PDFs da pasta para md", "passa esse artigo para markdown", "PDF escaneado", "lote de PDFs", "preciso do texto desses artigos". Não faz OCR nem resume.
allowed-tools: Bash(python ${CLAUDE_SKILL_DIR}/scripts/extrair_pdf.py *) Read Glob
argument-hint: "[caminho do PDF ou da pasta] [--saida DIR]"
---

# kfh-pdf-para-md

Extrai PDFs para Markdown fiel: um `.md` por PDF, um marcador por página. O script faz a extração e a limpeza mecânica. Você só confere.

O `.md` vai ser citado por outra pessoa, ou por outra skill, como se fosse o PDF. **Qualquer palavra que você acrescentar vira uma citação falsa.** Por isso as regras abaixo não têm exceção.

## O que você pode e o que nunca pode fazer no texto extraído

**Pode:**
- remover cabeçalho ou rodapé repetido que o script deixou passar;
- juntar palavra hifenizada na quebra de linha;
- normalizar espaço;
- reordenar blocos de uma página em coluna dupla que saiu embaralhada.

**Nunca:**
- acrescentar palavra, mesmo "óbvia";
- completar frase cortada;
- resumir, parafrasear ou traduzir;
- preencher página marcada como não extraída;
- corrigir "erro" do autor;
- remover trecho por achar irrelevante.

Se o pedido for "extrai e resume", extraia com esta skill e trate o resumo como outra tarefa, depois, fora dela, dizendo isso ao usuário.

## Procedimento

1. **Identifique entrada e saída.** Entrada: um ou mais `.pdf`, ou uma pasta (sem recursão). Saída padrão: pasta `extraido/` ao lado dos PDFs. Se o usuário não disse onde salvar, use o padrão e avise.
2. **Rode o script:**
   ```bash
   python ${CLAUDE_SKILL_DIR}/scripts/extrair_pdf.py <pdf ou pasta> [outros...] [--saida DIR] [--sobrescrever]
   ```
   - Código 0: todos os PDFs abriram. Código 1: algum não abriu (protegido, corrompido, caminho errado); o `stderr` diz qual. Continue com os que abriram e relate os outros.
   - Página não extraída (escaneada) **não** é erro: o script segue e marca.
   - `.md` que já existe é pulado; só regrave com `--sobrescrever` se o usuário pediu.
3. **Confira só o que precisa.** Para cada `.md`, leia o frontmatter: `tipos_por_pagina`, `paginas_nao_extraidas`, `removido_repetido`. Abra apenas as páginas marcadas `coluna-dupla` ou `tabelas` e veja se a ordem de leitura faz sentido. Se uma frase está cortada e continua no bloco errado, mova o bloco. Não reescreva a frase.
4. **Relate ao usuário**, nesta ordem: a tabela de resumo do script; páginas não extraídas (arquivo e página); o que foi removido como repetição (para ele conferir que não era texto legítimo); páginas que você reordenou.
5. **Pedidos fora do escopo:** OCR, resumo, tradução. Diga que esta skill não faz e, no caso de OCR, liste as páginas afetadas para o usuário resolver fora.

## Formato de saída (contrato com `kfh-md-buscar`)

```markdown
---
fonte: artigo.pdf
caminho: C:/.../artigo.pdf
paginas: 12
extraido_em: 2026-10-12T15:40:00
ferramenta: kfh-pdf-para-md (pdfplumber 0.11.10)
tipo_detectado: coluna-dupla
tipos_por_pagina: {1: texto, 2: coluna-dupla, 9: escaneado}
paginas_nao_extraidas: [9]
removido_repetido: ["Revista X, v. 2", "numeração de página"]
---

<!-- artigo.pdf | p. 1 -->
texto da página 1...

<!-- artigo.pdf | p. 2 -->
texto da coluna esquerda...
texto da coluna direita...

<!-- tabela 1 -->
| col | col |
| --- | --- |
```

O marcador é sempre `<!-- <arquivo> | p. <N> -->`. Nunca altere, apague ou renumere um marcador.

Dois textos fixos podem aparecer no lugar do texto de uma página: `[não extraído: página sem camada de texto, provável escaneado]` (página escaneada, sem OCR) e `[página sem conteúdo]` (página realmente vazia no PDF). Nenhum dos dois é erro e nenhum dos dois pode ser preenchido, removido ou reescrito.

## O que esta skill não faz

OCR (página sem camada de texto sai como `[não extraído: página sem camada de texto, provável escaneado]`; página vazia sai como `[página sem conteúdo]`), resumo, tradução, busca de informação (isso é a `kfh-md-buscar`), recursão em subpastas.
