---
name: kfh-md-buscar
description: Usar quando o usuário quer localizar informação específica (campos como título, autor, ano, amostra, método, ou perguntas) em arquivos Markdown extraídos de PDF e precisa de cada resposta com arquivo, página e trecho literal de onde foi tirada. Aciona em "acha nesses md", "catalogar os artigos", "onde o texto diz", "preenche a tabela a partir dos md", "cita a página", "qual o ano de cada artigo". Não lê PDF; exige md com marcador de página gerado pela kfh-pdf-para-md.
allowed-tools: Bash(python ${CLAUDE_SKILL_DIR}/scripts/verificar_citacoes.py *) Read Grep Glob Write
argument-hint: "[pasta dos .md] [campos ou perguntas]"
---

# kfh-md-buscar

Localiza informação específica em `.md` extraídos de PDF e devolve cada achado com arquivo, página e trecho literal, numa tabela `achados.md`. Um script confere se cada trecho existe mesmo onde você disse.

A tabela vai ser usada como se fosse o PDF. **Uma citação que não confere é uma invenção com cara de evidência.** Por isso você não entrega `achados.md` com `❌`.

## Pré-condições (pare se falhar)

- Entrada: uma pasta ou lista de `.md` **com marcador de página** no formato `<!-- arquivo.pdf | p. N -->`, mais a lista do que buscar.
- Se receber PDF, ou `.md` sem marcador: pare e diga "rode `kfh-pdf-para-md` primeiro". Não abra PDF, não improvise marcador.
- Se a lista de campos ou perguntas não veio: pergunte antes de buscar. Não escolha campos por conta própria.

## Procedimento

1. **Liste os `.md` e confirme o marcador** em cada um (Grep por `<!-- .* \| p\. [0-9]+ -->`).
2. **Busque campo a campo, arquivo a arquivo.** Use Grep com palavras-chave do campo e leia só o bloco da(s) página(s) onde houve ocorrência. Campos de capa (título, autores, revista, ano) costumam estar na p. 1: leia a p. 1 inteira. Arquivo pequeno (até ~300 linhas) pode ser lido inteiro.
3. **Copie o trecho literal:** uma ou duas frases contíguas, exatamente como estão no `.md`, sem reticências no meio, dentro de uma só página. A página é a do marcador imediatamente acima.
4. **A resposta vem só do trecho.** Se o trecho não sustenta a resposta sozinho, o status não é `encontrado`.
5. **Status:**
   - `encontrado`: o trecho afirma o que o campo pede.
   - `parcial`: achou algo próximo, mas não exatamente o pedido (ex.: ano de submissão, não de publicação). A resposta explica a diferença em poucas palavras.
   - `não encontrado`: nada no arquivo. Resposta, página e trecho ficam **vazios**. Nunca inferir.
   - `conflitante`: dois trechos divergem. Duas linhas, uma por trecho, ambas `conflitante`.
6. **Grave `achados.md`** na pasta dos `.md` (salvo pedido diferente), no formato abaixo.
7. **Verifique:**
   ```bash
   python ${CLAUDE_SKILL_DIR}/scripts/verificar_citacoes.py <pasta>/achados.md --marcar
   ```
   - No app claude.ai (skill enviada por zip) a variável ${CLAUDE_SKILL_DIR} não existe: o script é `scripts/verificar_citacoes.py` dentro da pasta desta skill; use esse caminho relativo.
   Linha marcada `❌ citação não confere`: recopie o trecho da página certa e devolva o status correto, ou mude para `não encontrado` esvaziando resposta, página e trecho. Rode de novo até `0 falha(s)`.
8. **Entregue:** caminho do `achados.md`, contagem por status, e a lista do que ficou `não encontrado` ou `conflitante` para o usuário decidir.

## Formato do `achados.md`

```markdown
---
pasta: C:/.../extraido
arquivos: 3
campos: [título, autor, ano, revista]
gerado_em: 2026-10-12T16:10:00
---

| campo | resposta | arquivo | página | trecho literal | status |
| --- | --- | --- | --- | --- | --- |
| ano | 2021 | artigo.md | 1 | "Recebido em 2020, publicado em março de 2021" | encontrado |
| amostra | | artigo.md | | | não encontrado |
```

- Uma linha por campo por arquivo, na ordem dos campos e depois dos arquivos.
- `trecho literal` entre aspas; `|` dentro do trecho escapado como `\|`.
- O verificador acrescenta `verificado:` ao frontmatter.

## O que esta skill não faz

Ler PDF, extrair texto, OCR, resumir o conteúdo, decidir campos por conta própria, inferir valor que o texto não afirma.
