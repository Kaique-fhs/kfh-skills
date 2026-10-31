---
name: kfh-slide-sian
description: Use quando o usuário pedir uma apresentação, slides ou deck em HTML no padrão SIAN ("monta uma apresentação", "faz os slides da reunião", "deck da SIAN em HTML"). Monta o arquivo .html autossuficiente a partir de uma base (palco 16:9, navegação, modo de edição, capa, encerramento) e de blocos prontos (cartões, linha do tempo, comparações, barras), só com cores e fonte da marca. Não gera .pptx; para PowerPoint use a ppt-sian.
---

# kfh-slide-sian

Kit de apresentações HTML no padrão visual da SIAN: uma base, 11 blocos prontos e dois scripts. Você escolhe os blocos, cola o que precisa na base e gera um `.html` que abre em qualquer máquina, sem esta skill instalada.

## Obrigatório

Antes de qualquer coisa, carregue (leia) as duas skills abaixo. Sem elas, não monte nada.

1. **`kfh-marca-sian`**: fonte única de cores, fonte Supreme, logos e grafismo de canto.
2. **`frontend-slides`** (plugin): o motor das apresentações HTML.

Se alguma não estiver instalada, avise o usuário. O `embutir.py` também falha com "instale a kfh-marca-sian" ou "instale o plugin frontend-slides".

## Como as duas se encaixam

| Vem da `frontend-slides` (mecânica) | Não vem dela |
| --- | --- |
| Fase 1 (descoberta de conteúdo); `viewport-base.css` (lido na hora de embutir, não copiado); `html-template.md` (estrutura, JS, qualidade); `animation-patterns.md`; modos de densidade; Modo C (alterar apresentação existente); Fases 4 a 6 (conversão de PPT, entrega, exportação para PDF) | **Fase 2 inteira**: não ofereça presets de estilo nem prévias. O estilo é sempre SIAN, mesmo que a `frontend-slides` peça essa fase por padrão |

Em conflito: no **visual** (cor, fonte, grafismo, layout) vale a `kfh-marca-sian` e o catálogo desta skill; na **mecânica** (palco, troca de slides, impressão) vale a `frontend-slides`.

## Regras críticas

- Só as cores oficiais (Azul Naval, Laranja Elétrico, Cinza Escuro, Cinza Claro e branco) e transparências delas. Os neutros `#F5F4F2` e `#E6E3DF` da referência antiga não existem aqui.
- Toda cor literal fica só no `:root` da base. Blocos e slides usam `var(--...)`. Nunca escreva HEX ou `rgb()` num bloco.
- Só a fonte Supreme (com `sans-serif` de reserva).
- O grafismo de canto (`sian-icone-canto.png`) fica sempre no canto inferior **esquerdo**.
- Painel azul: título laranja e texto branco.
- Nada de texto, nomes de pessoas ou números da apresentação de referência. Os textos dos blocos são genéricos; troque tudo pelo conteúdo do usuário.
- Mais de 5 categorias de cor (`.cat-1` a `.cat-5` são as únicas): avise o usuário em vez de inventar cor.
- Slide refeito: some 1 no `data-v` da `<section>` dele. É assim que a edição guardada no navegador cede à versão nova.

## Tokens do `:root`

Já estão na `base/modelo.html`. Não crie outros sem aprovação.

| Token | Valor |
| --- | --- |
| `--azul` / `--laranja` / `--cinza-escuro` / `--cinza-claro` / `--branco` | `#24286E` / `#FF6934` / `#94958B` / `#C7C3BD` / `#FFFFFF` |
| `--fundo-cartao` (cartão claro) | `rgba(199,195,189,.18)` |
| `--divisor` | `rgba(199,195,189,.46)` |
| `--branco-18` (linhas sobre azul) | `rgba(255,255,255,.18)` |
| `--branco-55` (dica de navegação) | `rgba(255,255,255,.55)` |
| `--laranja-16` (halo de pontos) / `--laranja-60` (contorno da edição) | `rgba(255,105,52,.16)` / `rgba(255,105,52,.6)` |
| `--azul-07` / `--azul-20` (listrado) / `--azul-85` (botão tela cheia) | `rgba(36,40,110,.07)` / `rgba(36,40,110,.20)` / `rgba(36,40,110,.85)` |
| `--stage-bg` (faixa fora do slide) | `var(--azul)` (preto não é cor da marca) |
| `--slide-bg` | `var(--branco)` |
| `.cat-1` a `.cat-5` (categorias) | azul/branco, laranja/branco, cinza-escuro/branco, cinza-claro/azul, listrado `--azul-20`/`--azul-07` com texto azul |

## Fluxo

1. Leia as duas skills obrigatórias.
2. Siga a Fase 1 da `frontend-slides`. **Pule a Fase 2.**
3. Proponha o roteiro (um título e um bloco do índice por slide) e **espere o ok** do usuário.
4. Copie `<skill>/base/modelo.html` para `<projeto>/<nome>.rascunho.html`. `<skill>` é a pasta desta skill: no Claude Code, `~/.claude/skills/kfh-slide-sian/`; no repo, `kfh-slide-sian/`.
5. Monte no rascunho:
   - capa e encerramento (já no modelo; encerramento só quando o usuário quiser; o roteiro da capa lista os slides: até cerca de 8 itens com `class="capa-roteiro"`, de 9 a 12 com `class="capa-roteiro denso"`, e mais que isso pede agrupar seções) e um `<section class="slide" aria-label="<rótulo único>" data-v="1">` por slide (o `aria-label` é a chave da edição salva no navegador: **precisa ser único**, senão slides trocam edições; o `conferir` reprova repetidos), com os blocos dentro do `.corpo`;
   - cole o CSS de cada bloco usado, e só o dos usados, no `<style>`;
   - cole a linha "Editáveis" de cada bloco usado como **uma string** em `EDITAVEIS_BLOCOS`;
   - mantenha os marcadores `{{...}}` do modelo, o script os troca;
   - numeração `<b>NN</b> / TT` em cada slide comum (a capa e o encerramento não levam número); os passos de clique (`data-passo`) seguem a linha "Passos de clique" do bloco.
6. Gere o final: `python <skill>/scripts/embutir.py <rascunho.html> <final.html>`. Ele embute fonte, logos, canto e o `viewport-base.css` e define a chave de edição pelo nome do arquivo final.
7. Confira: `python <skill>/scripts/conferir.py <final.html>`. Imprime `OK` ou a lista de problemas (cor fora do padrão, fonte que não é Supreme). Corrija no rascunho e rode de novo os dois scripts.
8. Abra o final no navegador e veja se o console está sem erro. `?passo=99#N` na URL abre o slide N com todos os itens à mostra, útil para conferir e capturar.

Dois ou três blocos no mesmo `.corpo` ficam empilhados; confira que não se sobrepõem.

## Índice dos blocos

Cada arquivo traz quando usar, quando não usar, passos de clique, "Editáveis", CSS e HTML. Leia o arquivo do bloco antes de usá-lo.

| Bloco | Serve para | Arquivo |
| --- | --- | --- |
| Barra empilhada | total dividido em 2 a 5 partes proporcionais | `blocos/barra-empilhada.md` |
| Cartões numerados | 3 a 5 frentes ou objetivos lado a lado, o primeiro em destaque | `blocos/cartoes-numerados.md` |
| Chips | rótulos curtos em pílulas, complemento de outro bloco | `blocos/chips.md` |
| Cronograma com balões | 5 a 12 entregas datadas, em duas frentes | `blocos/cronograma-baloes.md` |
| Destaque e lista | um item principal com detalhe, mais 2 a 4 secundários | `blocos/destaque-lista.md` |
| Dois cenários | duas alternativas numéricas com equação e barra | `blocos/dois-cenarios.md` |
| Dois lados | duas posições ou perfis frente a frente | `blocos/dois-lados.md` |
| Etapas em trilho | sequência de 3 etapas, a última destacada | `blocos/etapas-trilho.md` |
| Faixa de conta | 3 a 6 números encadeados até o resultado | `blocos/faixa-conta.md` |
| Faixa de destaque | frase de síntese abaixo de outro bloco | `blocos/faixa-destaque.md` |
| Linha do tempo com cartões | 3 a 5 marcos datados, um cartão por marco | `blocos/linha-tempo-cartoes.md` |

Limites conhecidos:
- O cronograma com balões tem 600px de altura: só cabe sozinho no `.corpo`.
- A linha do tempo com cartões tem 5 colunas fixas: não passe de 5 marcos (para mais, cronograma com balões).

## Quando não usar

- O usuário quer `.pptx` ou PowerPoint: use a `ppt-sian`.
- O pedido não cabe em nenhum bloco: diga isso ao usuário e proponha um bloco novo, montado só com os tokens da base. Ele entra no catálogo (`blocos/`) depois de aprovado; até lá, fica só naquela apresentação.
