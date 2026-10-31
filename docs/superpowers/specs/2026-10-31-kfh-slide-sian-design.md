# kfh-slide-sian — Design

**Data:** 31/10/2026
**Status:** Aprovado pelo usuário em 31/10/2026

## 1. Objetivo

Toda apresentação nova da SIAN deve sair com a mesma cara, sem começar do zero. O usuário pede a apresentação ("monta uma apresentação sobre X com estes pontos") e o Claude monta um HTML usando peças prontas, tiradas da apresentação de referência `solucoes-e-analytics-em-2026.html` (pasta `9 - Apresentação SIAN`).

Quem usa as peças é o Claude, não o usuário. O usuário só pede, revisa e apresenta.

O que se aproveita da referência é o **visual e a identidade da marca**, nunca o texto nem os números.

## 2. Metas, não-metas e anti-metas

**Metas**
- Uma skill `kfh-slide-sian` que o Claude aciona quando o usuário pedir uma apresentação no padrão SIAN.
- Uma base fixa (estrutura do arquivo, navegação, animações, capa, cabeçalho, logo, canto, numeração, barra de progresso, tela cheia, edição no navegador, impressão) que se repete em toda apresentação.
- Um catálogo de blocos visuais, cada um com HTML/CSS de exemplo preenchido com texto genérico e instrução de quando usar.
- O resultado é um único `.html` que funciona sem internet (fonte e imagens embutidas).

**Não-metas**
- Não gera `.pptx`. Slides no PowerPoint continuam com a skill `ppt-sian`.
- Não é para o usuário montar ou editar slides abrindo os arquivos da skill. (A edição de texto no navegador, que já existe na referência, continua.)
- Não copia o conteúdo da apresentação de referência.

**Anti-metas (o que torna a skill um fracasso, mesmo funcionando)**
- **Cor ou fonte fora do padrão SIAN** (dito pelo usuário). Toda cor sai das quatro oficiais e do branco (inclusive suas versões transparentes); toda fonte é Supreme.
- Duplicar a identidade em dois lugares que podem divergir.

## 3. Decisões tomadas

| Decisão | Escolha | Quem decidiu |
|---|---|---|
| Nome | `kfh-slide-sian` | usuário |
| Onde fica | `C:\Users\kaique.souza\Desktop\kfh-harness\kfh-skills\kfh-slide-sian\` (repo `kfh-skills`, empacotado com `empacotar.py` como as outras) | usuário |
| Quem monta | O Claude, a partir do pedido | usuário |
| O que se aproveita | Visual e identidade, não texto | usuário |
| Formato | HTML 16:9 (1920×1080 escalado), igual à referência | Claude (segue a referência) |
| Skills obrigatórias | Toda execução da `kfh-slide-sian` usa **`kfh-marca-sian`** e **`frontend-slides`**; o `SKILL.md` registra isso no topo como obrigatório | usuário |
| Cores, fonte, logos, canto | Lidos da skill `kfh-marca-sian`, não copiados | Claude |
| Embutir fonte e imagens | Script da skill troca marcadores pelos arquivos da `kfh-marca-sian` em base64 | Claude |

## 4. Relação com a `kfh-marca-sian`

A `kfh-marca-sian` continua sendo a única fonte de cores, fonte, logos e grafismo de canto. A `kfh-slide-sian`:
- manda ler a `kfh-marca-sian` antes de montar;
- usa no `:root` exatamente os HEX de lá (`#24286E`, `#FF6934`, `#94958B`, `#C7C3BD`), mais o branco `#FFFFFF`;
- **só cores oficiais (decisão do usuário).** Os dois neutros da referência (`#F5F4F2` fundo de cartão claro, `#E6E3DF` divisor) **saem**. Os tons claros passam a ser versões transparentes das cores oficiais sobre o branco, declaradas como tokens no `:root` a partir das variáveis oficiais (por exemplo, `--fundo-cartao` = Cinza Claro com opacidade baixa; `--divisor` = Cinza Claro com opacidade média). **Chamada do Claude:** os valores exatos de opacidade são escolhidos ao implementar, comparando com a referência, e ficam registrados no `SKILL.md`;
- transparências das cores oficiais (branco a 18% nas linhas sobre o painel azul, halo laranja a 16% nos pontos da linha do tempo, listrado de azul) contam como dentro do padrão;
- **regra para o Claude:** nenhum HEX ou `rgb()` escrito à mão nos blocos; toda cor sai de uma variável do `:root`, e toda variável do `:root` sai de uma das quatro cores oficiais ou do branco. A conferência final (seção 7, passo 5) procura cor literal fora do `:root`.
- puxa os arquivos (`Supreme-Variable.woff2`, `sian-logo-original.png`, `sian-icone-canto.png`) da pasta `assets/` da `kfh-marca-sian` na hora de montar, sem cópia dentro da `kfh-slide-sian`.

Regras da marca que a skill repete por serem críticas: canto sempre no inferior **esquerdo**; painel azul com título laranja e texto branco; logo azul+laranja em fundo branco.

## 4b. Relação com a `frontend-slides`

Uso obrigatório (decisão do usuário). A `frontend-slides` (plugin, v2.1.0) é o motor; a `kfh-slide-sian` é o estilo fixo e o catálogo. Na prática (**chamada do Claude** de como as duas se encaixam):

- **Vem da `frontend-slides`:** o `viewport-base.css` completo (palco 16:9, troca de slides por `.active`/`.visible`, impressão, movimento reduzido), as regras de `html-template.md` (estrutura, JS, qualidade de código), `animation-patterns.md`, os modos de densidade de conteúdo, as regras de modificação de apresentação existente (Modo C), a conversão de PPT (Fase 4), a entrega (Fase 5) e a exportação para PDF (Fase 6). A referência já foi feita assim: o CSS dela traz o `viewport-base.css` inteiro.
- **Não vem da `frontend-slides`:** a Fase 2 inteira (as três prévias de estilo, os `STYLE_PRESETS.md` e o `bold-template-pack`). O estilo é sempre o SIAN; oferecer outros estilos violaria a anti-meta. O `SKILL.md` diz isso com todas as letras, porque a `frontend-slides` pede essa fase por padrão.
- **Conflito:** onde as duas divergirem em visual (cor, fonte, grafismo, layout), vale a `kfh-marca-sian` e o catálogo da `kfh-slide-sian`; onde divergirem em mecânica (palco, troca de slides, impressão), vale a `frontend-slides`.
- **Sem cópia:** o `viewport-base.css` é lido da pasta da `frontend-slides` na hora de montar, como os assets da marca, para que uma atualização do plugin chegue às apresentações novas.

## 5. A base (vai em toda apresentação)

Extraída da referência, sem conteúdo:

- **Palco 16:9 fixo:** `.deck-viewport` / `.deck-stage` 1920×1080 escalado para a tela, faixa preta fora.
- **Navegação:** setas, espaço, Enter, PageUp/Down, Home/End, clique, roda do mouse, toque; `F` tela cheia (com botão que aparece ao mexer o mouse); barra de progresso laranja no topo que conta slides e passos.
- **Passos por clique:** `data-passo="n"` faz o elemento entrar no n-ésimo clique; sem `data-passo`, entra com o slide.
- **Animações:** `.reveal` (sobe), `.da-esquerda`, `.da-direita`, `.cresce`, `.estica` (barra cresce da esquerda), atraso por `style="--d:.3s"`; respeita `prefers-reduced-motion`.
- **Números que contam:** `data-conta` (lê o próprio texto) e `data-minutos` (formato H:MM).
- **Edição no navegador:** tecla `E` ou canto superior esquerdo liga a edição; `Ctrl+S` baixa o HTML editado. As edições ficam guardadas no navegador (`localStorage`), slide a slide, casando pelo `aria-label` do slide e pela versão `data-v`: quando um slide é refeito no arquivo, o `data-v` dele sobe e a versão nova aparece, enquanto os outros slides mantêm as edições. **Chamadas do Claude:** todo slide novo nasce com `data-v="1"` e o Claude soma 1 a cada vez que refaz aquele slide; a chave de gravação (`sian-banco-horas-v5` na referência) passa a ser única por apresentação, derivada do nome do arquivo, para uma apresentação não herdar edições de outra; a lista de seletores editáveis é montada a partir dos blocos usados (cada bloco declara os seus).
- **Impressão:** um slide por página, tudo visível.
- **Elementos comuns de slide:** logo no canto superior direito, canto no inferior esquerdo, cabeçalho (`.kicker` laranja em caixa alta + `h1`), numeração `01 / 05` no inferior direito, nota de rodapé (`.nota3`).
- **Capa:** esquerda branca com logo, kicker, título grande e subtítulo; painel azul à direita com faixa laranja e roteiro numerado.
- **Encerramento** (**chamada do Claude**, a referência não tem): slide final que espelha a capa, com painel azul ocupando a maior parte, logo e uma frase de fecho ou contato. Usado só quando o usuário quiser fechar com um slide próprio.

## 6. Catálogo de blocos

Cada bloco vira um arquivo em `blocos/` com: para que serve, quando usar, HTML de exemplo com texto genérico, CSS próprio e quais passos de clique ele costuma ter. Nomes de classe genéricos (sem "rayssa", "sgc" etc.).

| Bloco | Origem na referência | Serve para |
|---|---|---|
| Dois lados (com "×" no meio) | "Como chegamos aqui" (`.lados`) | contrapor duas posições, antes × depois |
| Etapas em trilho | "Como chegamos aqui" (`.tempo`) | 3 momentos em sequência, último em destaque |
| Dois cenários com equação | "A conta das horas" (`.cenarios`) | comparar A × B com conta (a − b = c), barra de proporção e linhas de detalhe |
| Faixa de destaque | `.diferenca` | uma frase de conclusão com borda laranja |
| Cartões numerados | "Objetivos de 2026" (`.obj`) | 3 a 5 itens em ordem de prioridade, o 1º em azul |
| Faixa de conta | `.conta-mes` | sequência de números até um resultado (último em azul) |
| Barra empilhada | `.empilhada` | divisão de um total em partes proporcionais |
| Destaque + lista | `.mes-detalhe` | item principal em painel azul ao lado de lista do restante |
| Linha do tempo proporcional + cartões | "Objetivos da Rayssa" (`.linha-tempo`, `.rs`) | marcos em datas, com cartão por marco |
| Cronograma com balões | "Divisão das entregas" (`.crono`, `.ev`) | entregas de duas pessoas/equipes acima e abaixo de uma linha de datas |
| Chips | `.chips` | etiquetas pequenas dentro de cartões |

As cores das categorias (`.d-sgc`, `.d-sco`…) viram uma paleta genérica de categorias: azul, laranja, cinza escuro, cinza claro e o listrado de azul para "reserva/outros". **Chamada do Claude:** com mais de cinco categorias, a skill avisa o usuário em vez de inventar cor.

## 7. Estrutura da skill

```
kfh-slide-sian/
  SKILL.md              gatilho, fluxo de montagem, regras críticas, índice dos blocos
  base/
    modelo.html         esqueleto completo: CSS da base, JS, capa, um slide vazio, marcadores de fonte/logo/canto
  blocos/
    <bloco>.md          um por bloco do catálogo (HTML + CSS + quando usar)
  scripts/
    embutir.py          troca os marcadores pelos arquivos da kfh-marca-sian em base64 e grava o .html final
```

**Fluxo da skill, quando o usuário pede uma apresentação:**
1. Ler a `kfh-marca-sian` e a `frontend-slides` (obrigatório).
2. Seguir a Fase 1 da `frontend-slides` (descoberta de conteúdo), pular a Fase 2 (estilo é SIAN) e propor o roteiro (um título e um bloco por slide) ao usuário antes de montar.
3. Copiar `base/modelo.html`, montar capa e slides com os blocos escolhidos, incluindo só o CSS dos blocos usados.
4. Rodar `scripts/embutir.py` para gerar o `.html` final na pasta do projeto do usuário.
5. Conferir: só cores do `:root`, só Supreme, canto à esquerda, numeração certa, abrir no navegador sem erro no console.

**Lista de blocos:** é a da tabela acima, que cobre todos os tipos de slide da referência. Pedido que não caiba em nenhum bloco: o Claude diz isso ao usuário e propõe um bloco novo, montado só com as classes e cores da base, que entra no catálogo depois de aprovado.

## 8. Dependência e distribuição

**Chamada do Claude.** A apresentação gerada é um `.html` autossuficiente: abre em qualquer máquina, sem a skill instalada. Quem precisa da `kfh-marca-sian` e da `frontend-slides` é só a `kfh-slide-sian`, na hora de montar. O `SKILL.md` declara as duas como obrigatórias no topo, e o `embutir.py` falha com mensagem clara ("instale a kfh-marca-sian" / "instale o plugin frontend-slides") quando não achar a pasta de alguma. Nenhum asset nem o `viewport-base.css` é copiado para dentro da skill.

## 9. Pronto

**Chamada do Claude.** A skill fica pronta quando:
- o repo tem `kfh-slide-sian/exemplos/demonstracao.html`, gerada pela própria skill com capa, encerramento e todos os blocos, com texto genérico;
- os testes do `embutir.py` passam;
- a demonstração abre no navegador sem erro no console, um print de cada slide é conferido contra a referência, e o usuário olha a demonstração e aprova;
- `python empacotar.py kfh-slide-sian` gera o zip.

## 10. O que fica para quem implementar

- Como nomear e escrever os marcadores de embutir (ex.: `{{FONTE_SUPREME}}`).
- Como o script acha a pasta da `kfh-marca-sian` (ao lado da `kfh-slide-sian` no repo; no Claude Code, `~/.claude/skills/kfh-marca-sian/`).
- Testes do `embutir.py` (o repo já tem `pytest`).
- Uma apresentação de demonstração gerada com todos os blocos, para conferir o visual contra a referência.
