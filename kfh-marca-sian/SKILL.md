---
name: kfh-marca-sian
description: Use quando for produzir qualquer material com a identidade visual da SIAN (slide, página HTML, artifact, relatório, documento, gráfico, e-mail, banner) ou quando o usuário pedir "padrão SIAN", "cores da SIAN", "logo da SIAN", "fonte da SIAN", "marca SIAN". Traz cores oficiais (HEX/RGB/CMYK), fonte Supreme (woff2), logos em PNG, grafismo de canto de slide e as regras de uso do manual da marca. Não inventa cor, fonte ou variação de logo que não esteja aqui.
---

# kfh-marca-sian

Fonte única da identidade visual da SIAN. Tudo aqui foi tirado do manual oficial (`assets/manual-da-marca-sian.pdf`) e dos arquivos entregues pelo usuário. A página citada é a do PDF, com o número impresso entre parênteses.

**Regra principal: não invente.** Se precisar de algo que não está nesta skill (outra cor, outra versão de logo, tamanho mínimo, área de proteção), diga que o manual não define e pergunte ao usuário.

## Assets

Caminho base: `~/.claude/skills/kfh-marca-sian/assets/`

| Arquivo | O que é |
| --- | --- |
| `logos/sian-logo-original.png` | Assinatura com tagline: "sian" e arcos em Azul Naval, tagline em Laranja Elétrico. Fundo transparente, 1080×676. |
| `logos/sian-logo-branca.png` | A mesma assinatura com tagline toda em branco (logo e tagline). Fundo transparente, 1154×676. |
| `grafismos/sian-icone-canto.png` | Recorte da estampa de semicírculos com "i" (azul e laranja), fundo transparente, 574×280. Uso: canto inferior direito de slide, quando fizer sentido. |
| `fontes/Supreme-*.woff2` | Família Supreme completa (Thin a Extrabold, com itálicos e variável). |
| `manual-da-marca-sian.pdf` | Manual da marca, 36 páginas. |

Não existe PNG da assinatura **sem** tagline; ela aparece só como imagem dentro do manual (p. 20 (21)). Se for necessária, avise o usuário em vez de recortar ou redesenhar.

## Cores (manual p. 21 (22))

| Nome | Atributo | HEX | RGB | CMYK |
| --- | --- | --- | --- | --- |
| Azul Naval | Confiança | `#24286E` | 36, 40, 110 | C100 M95 Y25 K10 |
| Laranja Elétrico | Imaginativo | `#FF6934` | 255, 105, 52 | C0 M70 Y80 K0 |
| Cinza Escuro | Entusiasmado | `#94958B` | 148, 149, 139 | C45 M30 Y40 K15 |
| Cinza Claro | Profissional | `#C7C3BD` | 199, 195, 189 | C25 M20 Y25 K0 |

No mosaico do manual o Azul Naval ocupa a maior área, o Laranja vem em seguida e os dois cinzas são menores. Nas páginas do manual o padrão é painel azul com títulos em laranja e texto em branco, ao lado de área branca.

```css
:root {
  --sian-azul-naval: #24286E;
  --sian-laranja-eletrico: #FF6934;
  --sian-cinza-escuro: #94958B;
  --sian-cinza-claro: #C7C3BD;
}
```

## Logo sobre fundo colorido (manual p. 22 (23))

Vale para a assinatura com tagline, sem tagline e para o avatar:

| Fundo | Logotipo | Tagline |
| --- | --- | --- |
| Azul Naval ou Cinza Claro | branco | laranja |
| Laranja Elétrico ou Cinza Escuro | azul | branco |
| Branco (p. 20 (21)) | azul | laranja → use `sian-logo-original.png` |

Atenção: `sian-logo-branca.png` tem a tagline em branco, o que **não** segue a regra do fundo azul/cinza claro (tagline laranja). Ela serve onde a versão toda branca for aceita; quando a regra tiver de ser seguida à risca, avise o usuário que falta o arquivo branco com tagline laranja.

Uso das assinaturas (p. 20 (21)): **com tagline** para aplicações em destaque; **sem tagline** para aplicações em espaços diversos.

## Tipografia

**Use sempre a Supreme** (decisão do usuário). O manual cita a Axia como fonte principal (p. 23 (24)), mas a Axia não foi entregue e não deve ser usada. O manual indica a Supreme para uso geral e interno, sites e aplicativos (p. 24 (25)); pesos mostrados lá: Light, Regular, Bold e Extra Bold.

Em HTML, embuta os woff2 (base64 ou arquivo junto) em vez de depender de CDN:

```css
@font-face { font-family: "Supreme"; src: url("Supreme-Variable.woff2") format("woff2"); font-weight: 100 800; font-style: normal; }
@font-face { font-family: "Supreme"; src: url("Supreme-VariableItalic.woff2") format("woff2"); font-weight: 100 800; font-style: italic; }
body { font-family: "Supreme", sans-serif; }
```

Para Office (PowerPoint/Word), a fonte precisa estar instalada na máquina; os woff2 não instalam no Windows. Origem indicada pelo manual: https://www.fontshare.com/fonts/supreme. Para slides no modelo oficial, use também a skill `ppt-sian`.

## Grafismos e iconografia

- **Ícone base** (p. 25 (26)): dois semicírculos com o "i", que representam a inteligência. Pode ser usado isolado, em conjunto (estampa) ou formando palavras.
- **Estampa** (p. 26 (27)): vários ícones base conectados, em configurações livres. Não preencher todo o espaço; deixar sempre área de respiro.
- **Canto de slide**: `grafismos/sian-icone-canto.png` no canto inferior direito, quando for o caso (indicação do usuário).
- **Ícones** (p. 27 (28)): base no Google Material Icons (https://fonts.google.com/icons), com os semicírculos inseridos para dar personalidade.

## Fotografia (p. 28 (29))

Use: pessoas em ambiente corporativo, semblante sereno ou feliz, de preferência trabalhando; elementos em azul ou laranja na foto; planos americano ou médio (deixam espaço para os grafismos).
Evite: semblante sério, preocupado ou infeliz; ambientes muito informais; cores muito saturadas fora da paleta; enquadramentos muito distantes ou em detalhe.

## Texto e tom de voz (manual p. 9–14)

Para escrever o conteúdo, não só o visual:

- **Personalidade:** confiável, técnica, imaginativa.
- **Tom de voz:** profissional (respeitoso, competente, experiente; nunca inoportuno, jocoso, ignorante), prático (eficiente, sincero, resolutivo; nunca negligente, preguiçoso, difícil), entusiasmado (simpático, criativo, positivo; nunca sisudo, austero, apático).
- **Tagline:** "Soluções inteligentes de apoio a negócios".
- **Missão:** prover serviços, estratégias e inteligência para evoluir negócios. **Propósito:** impulsionar resultados para desenvolver negócios.
- **Arquétipo:** O Sábio (p. 17–18).

## O que o manual não define

Área de proteção do logo, tamanho mínimo, usos proibidos do logo, cores secundárias ou de apoio, cores para gráficos além das quatro. Não preencha essas lacunas sem dizer ao usuário que são escolha sua.
