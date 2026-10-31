# kfh-slide-sian Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Criar a skill `kfh-slide-sian`: base HTML + catálogo de blocos + scripts que montam apresentações HTML no padrão SIAN, usando obrigatoriamente `kfh-marca-sian` e `frontend-slides`.

**Architecture:** O Claude monta um rascunho HTML a partir de `base/modelo.html` e dos blocos em `blocos/*.md`; `scripts/embutir.py` troca marcadores pelo `viewport-base.css` da `frontend-slides` e pelos assets da `kfh-marca-sian` em base64, gerando um `.html` autossuficiente; `scripts/conferir.py` barra cor ou fonte fora do padrão.

**Tech Stack:** Python 3 (stdlib) + pytest; HTML/CSS/JS sem dependências; Chrome headless para conferência visual.

**Spec:** `docs/superpowers/specs/2026-10-31-kfh-slide-sian-design.md`

## Global Constraints

- Repo: `C:\Users\kaique.souza\Desktop\kfh-harness\kfh-skills`. Pasta da skill: `kfh-slide-sian/`. Tudo em português do Brasil (textos, nomes de função, mensagens).
- Commit sempre por caminho explícito (`git add <arquivos>`), nunca `git add -A`/`.`: há mudança alheia não commitada em `kfh-marca-sian/SKILL.md` que não pode entrar.
- Mensagens de commit terminam com `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`.
- Cores: só as oficiais `#24286E` (36,40,110), `#FF6934` (255,105,52), `#94958B` (148,149,139), `#C7C3BD` (199,195,189) e branco `#FFFFFF` (255,255,255), inclusive em `rgba()` com esses mesmos RGB. Os neutros da referência `#F5F4F2` e `#E6E3DF` **saem**.
- Toda cor literal fica só no `:root`; blocos e base usam `var(--…)`.
- Fonte: só `"Supreme"` (com `sans-serif` de reserva).
- Canto (`sian-icone-canto.png`) sempre no canto inferior **esquerdo**.
- Nada copiado de `kfh-marca-sian` nem de `frontend-slides` para dentro da skill; são lidos na hora de embutir.
- Referência visual: `C:\Users\kaique.souza\Documents\0 - Projetos\9 - Apresentação SIAN\solucoes-e-analytics-em-2026.html` (692 KB por causa de base64). Para ler: `sed -E 's/base64,[A-Za-z0-9+\/=]{100,}/base64,.../g' <arquivo> > <scratch>/ref.html` (mesma numeração de linhas). CSS nas linhas 8–383, HTML 385–866, JS 869–1197. Aproveita-se o visual, **nunca** texto, nomes de pessoas ou números.
- Testes: `python -m pytest kfh-slide-sian/tests -q`, rodado da raiz do repo.

## Tokens do `:root` (valores fixados)

| Token | Valor |
|---|---|
| `--azul` / `--laranja` / `--cinza-escuro` / `--cinza-claro` / `--branco` | `#24286E` / `#FF6934` / `#94958B` / `#C7C3BD` / `#FFFFFF` |
| `--fundo-cartao` (era `#F5F4F2`) | `rgba(199,195,189,.18)` |
| `--divisor` (era `#E6E3DF`) | `rgba(199,195,189,.46)` |
| `--branco-18` (linhas sobre azul; unifica .16/.18/.2) | `rgba(255,255,255,.18)` |
| `--branco-55` (dica de navegação) | `rgba(255,255,255,.55)` |
| `--laranja-16` (halo de pontos) / `--laranja-60` (contorno da edição) | `rgba(255,105,52,.16)` / `rgba(255,105,52,.6)` |
| `--azul-07` / `--azul-20` (listrado) / `--azul-85` (botão tela cheia) | `rgba(36,40,110,.07)` / `rgba(36,40,110,.20)` / `rgba(36,40,110,.85)` |
| `--stage-bg` (faixa fora do slide; era `#000`) | `var(--azul)` |
| `--slide-bg` | `var(--branco)` |
| Categorias `.cat-1`…`.cat-5` (eram `.d-sgc`…`.d-emg`) | azul/branco, laranja/branco, cinza-escuro/branco, cinza-claro/azul, listrado `--azul-20`/`--azul-07` com texto azul |

`--stage-bg: var(--azul)` é chamada do plano (preto não é cor da marca); o usuário pode reverter.

## Review Focus

- Nome de saída com acento e espaço (`Reunião de Março.html`) → chave de edição `sian-reuniao-de-marco` e arquivo gravado. Teste na Task 1.
- Duas versões da `frontend-slides` no cache (`2.1.0` e `2.10.0`) → usa `2.10.0` (comparação numérica, não de texto). Teste na Task 1.
- Cor escrita com caixa ou espaços diferentes (`#ff6934`, `rgba( 255 , 105 , 52 , .16 )`) → reconhecida como oficial; `#F5F4F2` em qualquer lugar → reprovada. Teste na Task 2.
- Apresentação só com capa e um slide → numeração `01 / 01`, progresso e navegação sem erro no console. Verificação na Task 3.
- Dois ou três blocos empilhados no mesmo `.corpo` → sem sobreposição. Slide da demonstração na Task 8.

---

### Task 1: `embutir.py`

**Files:**
- Create: `kfh-slide-sian/scripts/__init__.py` (vazio), `kfh-slide-sian/scripts/embutir.py`
- Create: `kfh-slide-sian/tests/conftest.py` (põe `scripts/` no `sys.path`, como `kfh-md-buscar/tests/conftest.py`), `kfh-slide-sian/tests/test_embutir.py`

**Interfaces:**
- Produces:
  - `class DependenciaAusente(Exception)`; `class MarcadorDesconhecido(Exception)`
  - `achar_marca(raiz_skill: Path, home: Path) -> Path` — devolve a pasta `assets/` da `kfh-marca-sian`: primeiro `raiz_skill.parent / "kfh-marca-sian" / "assets"`, depois `home/.claude/skills/kfh-marca-sian/assets`. Exige `fontes/Supreme-Variable.woff2`, `logos/sian-logo-original.png`, `logos/sian-logo-branca.png`, `grafismos/sian-icone-canto.png`; senão `DependenciaAusente("instale a kfh-marca-sian: faltam ...")`.
  - `achar_viewport_base(home: Path) -> Path` — maior versão numérica em `home/.claude/plugins/cache/frontend-slides/frontend-slides/<versão>/skills/frontend-slides/viewport-base.css`; nenhuma → `DependenciaAusente("instale o plugin frontend-slides")`.
  - `data_uri(arquivo: Path, mime: str) -> str` — `data:<mime>;base64,<...>`
  - `chave_edicao(saida: Path) -> str` — `"sian-" +` nome sem extensão, minúsculo, sem acento, não alfanumérico → `-`, sem `-` repetido nas pontas.
  - `embutir(rascunho: str, assets: Path, viewport: Path, saida: Path) -> str` — troca: `/* {{VIEWPORT_BASE}} */` → `/* viewport-base:inicio */\n<conteúdo>\n/* viewport-base:fim */`; `{{FONTE_SUPREME}}` (font/woff2); `{{LOGO_ORIGINAL}}`, `{{LOGO_BRANCA}}`, `{{CANTO}}` (image/png); `{{CHAVE_EDICAO}}`. Sobrou `{{[A-Z_]+}}` → `MarcadorDesconhecido` com os nomes.
  - `main(argv: list[str]) -> int` — `python embutir.py <rascunho.html> <saida.html>`; usa `Path.home()` e a pasta da skill; grava UTF-8; imprime `OK: <saida>` e devolve 0; erro → mensagem em stderr, devolve 1.

- [ ] **Step 1: Escrever os testes** (fixtures em `tmp_path` com bytes falsos: `b"FONTE"`, `b"LOGO"` etc.)
  - `test_embutir_troca_todos_os_marcadores`: rascunho com os 6 marcadores → resultado contém `data:font/woff2;base64,` + `base64(b"FONTE")`, os três `data:image/png;base64,`, `/* viewport-base:inicio */` e `sian-apresentacao` (saida `apresentacao.html`); não contém `{{`.
  - `test_marcador_desconhecido_falha`: `{{XYZ}}` → `MarcadorDesconhecido` com `"XYZ"` na mensagem.
  - `test_chave_edicao_com_acento_e_espaco`: `chave_edicao(Path("Reunião de Março.html")) == "sian-reuniao-de-marco"`.
  - `test_achar_marca_prefere_irma_no_repo` e `test_achar_marca_cai_para_home`; `test_achar_marca_sem_arquivo_falha` → `DependenciaAusente` com `"kfh-marca-sian"`.
  - `test_viewport_pega_maior_versao_numerica`: versões `2.1.0` e `2.10.0` → caminho com `2.10.0`; `test_viewport_ausente_falha` → mensagem com `"frontend-slides"`.
  - `test_main_grava_saida`: `main([rascunho, saida]) == 0` e arquivo existe (monkeypatch de `Path.home` e da raiz da skill).
- [ ] **Step 2:** `python -m pytest kfh-slide-sian/tests/test_embutir.py -q` → FAIL (módulo não existe).
- [ ] **Step 3:** Implementar as funções acima em `scripts/embutir.py` (só stdlib: `base64`, `re`, `unicodedata`, `pathlib`).
- [ ] **Step 4:** Mesmo comando → todos PASS.
- [ ] **Step 5:** Commit `kfh-slide-sian: embutir.py (marcadores, dependências e chave de edição)`.

### Task 2: `conferir.py`

**Files:**
- Create: `kfh-slide-sian/scripts/conferir.py`, `kfh-slide-sian/tests/test_conferir.py`

**Interfaces:**
- Produces:
  - `OFICIAIS_HEX = {"#24286E", "#FF6934", "#94958B", "#C7C3BD", "#FFFFFF"}`; `OFICIAIS_RGB = {(36,40,110), (255,105,52), (148,149,139), (199,195,189), (255,255,255)}`
  - `cores_literais(html: str) -> list[str]` — cores literais (`#hex` de 3–8 dígitos, `rgb()/rgba()/hsl()/hsla()`) em valores de declaração CSS dentro de `<style>` e de atributos `style=""`, **ignorando** blocos `:root {…}`, a região `/* viewport-base:inicio */…/* viewport-base:fim */` e URIs `data:`. Seletores de id (`#deckStage`) não contam.
  - `paleta_root_invalida(html: str) -> list[str]` — cores literais dentro de `:root` que não são oficiais (hex sem diferenciar caixa; `rgba` comparando o RGB, aceitando espaços).
  - `fontes_invalidas(html: str) -> list[str]` — famílias em `font-family` e no atalho `font:` fora de `Supreme`, `sans-serif`, `inherit` (fora da região do viewport-base).
  - `main(argv: list[str]) -> int` — `python conferir.py <arquivo.html>`; imprime cada problema com o tipo; 1 se houver, senão `OK` e 0.

- [ ] **Step 1: Testes**
  - `test_cor_literal_fora_do_root_reprovada`: `<style>.a{color:#F5F4F2}</style>` → `["#F5F4F2"]`.
  - `test_root_e_viewport_ignorados`: `:root{--x:#24286E}` e `#000` dentro da região do viewport-base → `[]`.
  - `test_id_e_data_uri_nao_contam`: `#deckStage{left:0}` e `src="data:image/png;base64,AAAA#fff"` → `[]`.
  - `test_style_inline_reprovado`: `<div style="background:rgba(0,0,0,.5)">` → 1 item.
  - `test_root_aceita_oficiais_com_caixa_e_espacos`: `:root{--a:#ff6934;--b:rgba( 255 , 105 , 52 , .16 )}` → `paleta_root_invalida == []`.
  - `test_root_reprova_neutro_antigo`: `:root{--d:#E6E3DF}` → `["#E6E3DF"]`.
  - `test_fontes`: `font-family:"Supreme",sans-serif` e `font:600 15px "Supreme", sans-serif` → `[]`; `font-family:Arial` → `["Arial"]`.
  - `test_main_codigo_de_saida`: arquivo limpo → 0; arquivo com `#F5F4F2` → 1.
- [ ] **Step 2:** `python -m pytest kfh-slide-sian/tests/test_conferir.py -q` → FAIL.
- [ ] **Step 3:** Implementar com `re` (só stdlib).
- [ ] **Step 4:** Mesmo comando → PASS.
- [ ] **Step 5:** Commit `kfh-slide-sian: conferir.py (cor e fonte fora do padrão)`.

### Task 3: `base/modelo.html`

**Files:**
- Create: `kfh-slide-sian/base/modelo.html`, `kfh-slide-sian/tests/test_modelo.py`

**Interfaces:**
- Consumes: marcadores e `embutir()` da Task 1; `cores_literais`, `paleta_root_invalida`, `fontes_invalidas` da Task 2.
- Produces (classes que os blocos usam e a SKILL documenta):
  - Estrutura: `.deck-viewport > main.deck-stage#deckStage > .progresso#progresso + section.slide[aria-label][data-v="1"]…`; `#dica.deck-controls`; botões `#telaCheia`, `#editToggle`, `#editHotzone`, `#aviso`.
  - Slide comum: `img.logo` (`{{LOGO_ORIGINAL}}`, canto superior direito), `.cab > .kicker + h1`, `.corpo` (área de conteúdo: `position:absolute; top:230px; left:110px; right:110px; bottom:150px; display:flex; flex-direction:column; gap:40px`), `p.nota` (era `.nota3`), `img.canto` (`{{CANTO}}`, inferior esquerdo), `.num`.
  - Capa: `.capa-logo`, `.capa-texto > .kicker + .capa-titulo + .capa-sub`, `.capa-painel > .capa-rot + ol.capa-roteiro > li > b`.
  - Encerramento (novo): `section.slide.encerramento` com painel azul ocupando ~2/3 à direita e faixa laranja (mesmo desenho do `.capa-painel`), `img` `{{LOGO_ORIGINAL}}` na área branca, `.enc-titulo` (frase de fecho, laranja sobre azul) e `.enc-sub` (contato, branco); canto no inferior esquerdo; sem `.num`.
  - Animação: `.reveal`, `.da-esquerda`, `.da-direita`, `.cresce`, `.fixo`, `.estica`, `data-passo="n"`, `style="--d:.3s"`; números `data-conta` e `data-minutos`; listas com bolinha usam `ul.marcadores` (o `normalizarMarcadores` passa a agir em `.marcadores li`).
  - JS: classe `SlidePresentation` da referência (linhas 869–1197), com `this.chave = '{{CHAVE_EDICAO}}'` e `this.editaveis = [EDITAVEIS_BASE, ...EDITAVEIS_BLOCOS].join(', ')`, onde `const EDITAVEIS_BASE = '.kicker, h1, .nota, .capa-titulo, .capa-sub, .capa-rot, .capa-roteiro li, .enc-titulo, .enc-sub'` e `const EDITAVEIS_BLOCOS = [ /* o Claude cola aqui a linha "Editáveis" de cada bloco usado */ ];`.

- [ ] **Step 1: Testes**
  - `test_modelo_tem_marcadores`: contém `/* {{VIEWPORT_BASE}} */`, `{{FONTE_SUPREME}}`, `{{LOGO_ORIGINAL}}`, `{{CANTO}}`, `{{CHAVE_EDICAO}}`.
  - `test_modelo_embutido_passa_na_conferencia`: `embutir()` com fixtures falsas → `cores_literais == []`, `paleta_root_invalida == []`, `fontes_invalidas == []`.
  - `test_modelo_sem_conteudo_da_referencia`: sem `rayssa|kaíque|kaique|marcelo|sgc|sco|banco de horas` (regex, sem caixa) e sem `#F5F4F2`/`#E6E3DF`.
  - `test_modelo_tem_capa_slide_e_encerramento`: 3 `<section class="slide`, uma com `capa`, uma com `encerramento`, todas com `data-v="1"`.
  - `test_canto_a_esquerda`: CSS de `.canto` tem `left: 0` e não tem `right`.
- [ ] **Step 2:** `python -m pytest kfh-slide-sian/tests/test_modelo.py -q` → FAIL.
- [ ] **Step 3:** Escrever `modelo.html` a partir da referência: CSS das linhas 8–95 e 355–382 (sem as linhas 38–55, que vêm do marcador `VIEWPORT_BASE`), `:root` com os tokens da tabela acima, capa (CSS 234–246, HTML 403–425) com texto genérico, um slide comum com `.corpo` vazio, o encerramento e o JS. Toda cor via `var()`.
- [ ] **Step 4:** Mesmo comando → PASS.
- [ ] **Step 5: Verificação no navegador.** `python kfh-slide-sian/scripts/embutir.py kfh-slide-sian/base/modelo.html <scratch>/modelo.html`; depois, para cada slide N de 1 a 3: `"C:\Program Files\Google\Chrome\Application\chrome.exe" --headless=new --window-size=1920,1080 --virtual-time-budget=4000 --enable-logging=stderr --screenshot=<scratch>/modelo-N.png "file:///<scratch>/modelo.html?passo=99#N"`. Esperado: nenhuma linha `CONSOLE` de erro no stderr; slide comum mostra `01 / 01`; capa e encerramento sem `.num`; canto no inferior esquerdo nos três.
- [ ] **Step 6:** Commit `kfh-slide-sian: base/modelo.html (palco, capa, encerramento, navegação e edição)`.

### Task 4: formato de bloco + blocos de comparação

**Files:**
- Create: `kfh-slide-sian/scripts/blocos.py`, `kfh-slide-sian/tests/test_blocos.py`
- Create: `kfh-slide-sian/blocos/dois-lados.md`, `etapas-trilho.md`, `dois-cenarios.md`, `faixa-destaque.md`

**Interfaces:**
- Consumes: `cores_literais`, `fontes_invalidas` (Task 2); classes da base (Task 3).
- Produces:
  - Formato de todo `blocos/<nome>.md`:
    ```
    # <Nome do bloco>
    - **Serve para:** …
    - **Quando usar:** …
    - **Quando não usar:** …
    - **Passos de clique:** …
    - **Editáveis:** `.sel-a, .sel-b`
    ## CSS
    ```css … ```
    ## HTML
    ```html … ```   (conteúdo que vai dentro de `.corpo`; nada de `top` absoluto em relação ao slide)
    ```
  - `ler_bloco(caminho: Path) -> dict` com chaves `nome, serve, quando, quando_nao, passos, editaveis, css, html`; campo ausente → `ValueError` com o nome do campo.
  - `classes_definidas(css: str) -> set[str]`; `classes_usadas(html: str) -> set[str]`.
- Origem na referência (CSS / HTML): dois-lados 100–110 / 437–455; etapas-trilho 112–127 / 457–476; dois-cenarios 135–161 / 495–540; faixa-destaque 163–164 / 543.

- [ ] **Step 1: Testes** (parametrizados sobre `sorted(Path("kfh-slide-sian/blocos").glob("*.md"))`)
  - `test_bloco_tem_todos_os_campos`: `ler_bloco` não lança erro; `editaveis` começa com `.`.
  - `test_bloco_sem_cor_literal_nem_fonte`: `cores_literais(f"<style>{css}</style>") == []` e `fontes_invalidas(...) == []`.
  - `test_bloco_sem_conteudo_da_referencia`: mesma regex de nomes da Task 3 em `html` e `css`.
  - `test_classes_do_html_existem`: `classes_usadas(html) - classes_definidas(css) - classes_definidas(css_da_base) == set()`.
  - `test_ler_bloco_campo_ausente`: md sem `**Editáveis:**` → `ValueError` com `"Editáveis"`.
- [ ] **Step 2:** `python -m pytest kfh-slide-sian/tests/test_blocos.py -q` → FAIL.
- [ ] **Step 3:** Implementar `blocos.py` e escrever os 4 blocos, com classes e texto genéricos (ex.: `.lado.destaque`/`.lado.claro` no lugar de `.gestor`/`.eu`), fundo claro via `var(--fundo-cartao)` e bordas via `var(--divisor)`.
- [ ] **Step 4:** Mesmo comando → PASS.
- [ ] **Step 5:** Commit `kfh-slide-sian: formato de bloco e blocos de comparação`.

### Task 5: blocos de números e listas

**Files:**
- Create: `kfh-slide-sian/blocos/cartoes-numerados.md`, `faixa-conta.md`, `barra-empilhada.md`, `destaque-lista.md`, `chips.md`

**Interfaces:**
- Consumes: formato e testes da Task 4 (rodam sozinhos sobre os arquivos novos); `.cat-1`…`.cat-5` da base.
- Origem (CSS / HTML): cartoes-numerados 199–214 / 561–615; faixa-conta 327–333 / 632–638; barra-empilhada 180–194 / 641–652; destaque-lista 336–353 / 654–674; chips 231–232 / 727.
- `barra-empilhada` documenta: largura de cada parte = `style="flex:<valor>"`; mais de 5 categorias → avisar o usuário em vez de inventar cor.

- [ ] **Step 1:** Escrever os 5 blocos (os testes da Task 4 já os cobrem).
- [ ] **Step 2:** `python -m pytest kfh-slide-sian/tests/test_blocos.py -q` → PASS para todos os blocos.
- [ ] **Step 3:** Commit `kfh-slide-sian: blocos de números e listas`.

### Task 6: blocos de tempo

**Files:**
- Create: `kfh-slide-sian/blocos/linha-tempo-cartoes.md`, `cronograma-baloes.md`

**Interfaces:**
- Consumes: formato e testes da Task 4.
- Origem (CSS / HTML): linha-tempo-cartoes 251–268 / 750–(fim da seção, ~800); cronograma-baloes 277–321 / seção `aria-label="Divisão das entregas"` (~804–866).
- Cada um documenta a conta de posição: `left = (dias desde o início ÷ dias do período) × 100%`; o cronograma documenta `--h` (altura da haste, escalonada para balões não se cruzarem), `.esq`, e os dois lados como `.ev.a` (azul, acima) e `.ev.b` (laranja, abaixo) no lugar de `.k`/`.r`.

- [ ] **Step 1:** Escrever os 2 blocos.
- [ ] **Step 2:** `python -m pytest kfh-slide-sian/tests/test_blocos.py -q` → PASS.
- [ ] **Step 3:** Commit `kfh-slide-sian: blocos de linha do tempo e cronograma`.

### Task 7: `SKILL.md`

**Files:**
- Create: `kfh-slide-sian/SKILL.md`, `kfh-slide-sian/tests/test_skill.py`

**Interfaces:**
- Consumes: tudo das Tasks 1–6.

Conteúdo obrigatório, nesta ordem:
1. Frontmatter: `name: kfh-slide-sian`; `description` em português começando com "Use quando o usuário pedir uma apresentação, slides ou deck em HTML no padrão SIAN…", dizendo que monta com base e blocos prontos e que não gera .pptx (para isso, `ppt-sian`).
2. Bloco **Obrigatório** no topo: antes de tudo, carregar as skills `kfh-marca-sian` e `frontend-slides`.
3. Como as duas se encaixam (spec §4b): da `frontend-slides` vêm Fase 1, `viewport-base.css`, `html-template.md`, `animation-patterns.md`, densidade, Modo C, Fases 4–6; **pular a Fase 2** (estilo é sempre SIAN; não oferecer presets nem prévias). Visual → vale a marca; mecânica → vale a `frontend-slides`.
4. Regras críticas: só cores oficiais e transparências delas, toda cor via `var()` do `:root`, só Supreme, canto inferior esquerdo, painel azul com título laranja e texto branco, nada de texto da referência.
5. Tabela de tokens (a deste plano).
6. Fluxo (spec §7): ler as duas skills → Fase 1 → propor roteiro (título + bloco por slide) e esperar o ok → copiar `base/modelo.html` para `<projeto>/<nome>.rascunho.html` → montar, colando só o CSS dos blocos usados e as linhas "Editáveis" em `EDITAVEIS_BLOCOS` → `python <skill>/scripts/embutir.py <rascunho> <final>` → `python <skill>/scripts/conferir.py <final>` → abrir no navegador sem erro no console. Ao refazer um slide, somar 1 no `data-v` dele.
7. Índice dos blocos: tabela `bloco | serve para | arquivo`.
8. Pedido que não cabe em nenhum bloco: dizer ao usuário e propor bloco novo, só com tokens da base; entra no catálogo depois de aprovado.
9. Encerramento: só quando o usuário quiser.

- [ ] **Step 1: Testes**
  - `test_frontmatter`: `name: kfh-slide-sian` e `description:` presentes.
  - `test_obrigatorias_no_topo`: `kfh-marca-sian` e `frontend-slides` aparecem nas primeiras 30 linhas depois do frontmatter.
  - `test_indice_bate_com_pasta`: cada `blocos/*.md` citado no `SKILL.md` e cada `blocos/<x>.md` citado existe.
  - `test_pula_fase_2`: o texto contém "Fase 2".
- [ ] **Step 2:** `python -m pytest kfh-slide-sian/tests/test_skill.py -q` → FAIL.
- [ ] **Step 3:** Escrever o `SKILL.md`.
- [ ] **Step 4:** `python -m pytest kfh-slide-sian/tests -q` → tudo PASS.
- [ ] **Step 5:** Commit `kfh-slide-sian: SKILL.md (obrigatórias, fluxo, regras e índice de blocos)`.

### Task 8: demonstração, conferência visual e zip

**Files:**
- Create: `kfh-slide-sian/exemplos/demonstracao.rascunho.html`, `kfh-slide-sian/exemplos/demonstracao.html`

**Interfaces:**
- Consumes: tudo. Seguir o fluxo do `SKILL.md` como se fosse um pedido real, com texto genérico ("Tema da apresentação", "Item 1"…).

Slides: capa; um slide por bloco (11); um slide empilhando `faixa-conta` + `barra-empilhada` + `destaque-lista` no mesmo `.corpo`; encerramento.

- [ ] **Step 1:** Montar `demonstracao.rascunho.html` e rodar `python kfh-slide-sian/scripts/embutir.py kfh-slide-sian/exemplos/demonstracao.rascunho.html kfh-slide-sian/exemplos/demonstracao.html` → `OK: …`.
- [ ] **Step 2:** `python kfh-slide-sian/scripts/conferir.py kfh-slide-sian/exemplos/demonstracao.html` → `OK`.
- [ ] **Step 3:** Prints com o Chrome headless (comando da Task 3, Step 5) de cada slide em `?passo=99`, em `<scratch>`, e prints da referência dos slides equivalentes do mesmo jeito. Esperado: nenhum erro de console; nada transbordando nem sobreposto (inclusive o slide empilhado); visual de cada bloco igual ao da referência, exceto os dois neutros trocados e a faixa azul fora do palco; numeração `01 / 12` a `12 / 12`.
- [ ] **Step 4:** `python empacotar.py kfh-slide-sian` → `OK: dist/kfh-slide-sian.zip` e a lista inclui `kfh-slide-sian/SKILL.md`, `base/modelo.html`, os 11 blocos e os dois scripts.
- [ ] **Step 5:** Commit dos dois arquivos de `exemplos/` com `kfh-slide-sian: apresentação de demonstração com todos os blocos`. (O zip fica fora: `dist/` está no `.gitignore`.)

Depois da Task 8: o usuário abre `kfh-slide-sian/exemplos/demonstracao.html` e aprova o visual (critério de pronto do spec §9).
