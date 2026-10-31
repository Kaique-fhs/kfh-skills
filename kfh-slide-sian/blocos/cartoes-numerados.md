# Cartões numerados
- **Serve para:** apresentar de 3 a 5 frentes, objetivos ou etapas lado a lado, cada uma com número, nome, descrição e uma lista curta.
- **Quando usar:** visão geral de itens paralelos, em que o primeiro merece destaque (cartão azul) e os demais seguem em cartões claros.
- **Quando não usar:** mais de 5 itens, ou itens que dependem de ordem no tempo (use etapas em trilho ou linha do tempo).
- **Passos de clique:** um cartão por clique, na ordem de leitura (1 a N).
- **Editáveis:** `.cn .on, .cn .onome, .cn .odesc, .cn .oquando, .cn .olista span`
## CSS
```css
.cartoes-n { display: grid; grid-template-columns: 1.2fr 1fr 1fr 1fr 1fr; gap: 24px; }
.cn { background: var(--fundo-cartao); border-radius: 22px; padding: 0 30px 30px; overflow: hidden; min-height: 560px; }
.cn .cor { display: block; height: 14px; margin: 0 -30px; }
.cn.um { background: var(--azul); color: var(--branco); }
.cn.um .cor { background: var(--laranja); }
.cn .on { font-size: 60px; font-weight: 800; line-height: 1; margin-top: 28px; color: var(--laranja); font-variant-numeric: tabular-nums; }
.cn .onome { font-size: 34px; font-weight: 800; line-height: 1.12; margin-top: 16px; min-height: 76px; }
.cn .odesc { font-size: 21px; line-height: 1.35; color: var(--cinza-escuro); margin-top: 10px; min-height: 85px; }
.cn.um .odesc { color: var(--cinza-claro); }
.cn .oquando { font-size: 24px; font-weight: 700; margin-top: 18px; padding-top: 16px; border-top: 2px solid var(--divisor); }
.cn.um .oquando { border-top-color: var(--branco-18); }
.cn .oquando small { display: block; font-size: 18px; font-weight: 700; letter-spacing: .1em; text-transform: uppercase; color: var(--laranja); margin-bottom: 4px; }
.cn .olista div { display: flex; justify-content: space-between; gap: 12px; font-size: 23px; font-weight: 700; padding: 10px 0; border-bottom: 2px solid var(--divisor); }
.cn.um .olista div { border-bottom-color: var(--branco-18); }
.cn .olista div span:nth-child(2) { font-weight: 600; color: var(--cinza-escuro); font-variant-numeric: tabular-nums; }
.cn.um .olista div span:nth-child(2) { color: var(--laranja); font-weight: 800; }
```
## HTML
```html
<div class="cartoes-n">
  <div class="cn um reveal" data-passo="1" style="--d:.05s">
    <i class="cor"></i>
    <div class="on">01</div>
    <div class="onome">Item 1</div>
    <div class="odesc">Descrição curta do item 1</div>
    <div class="oquando"><small>Entregas</small></div>
    <div class="olista">
      <div><span>Etapa A</span><span>dd/mm</span></div>
      <div><span>Etapa B</span><span>dd/mm</span></div>
    </div>
  </div>
  <div class="cn reveal" data-passo="2" style="--d:.05s">
    <i class="cor cat-2"></i>
    <div class="on">02</div>
    <div class="onome">Item 2</div>
    <div class="odesc">Descrição curta do item 2</div>
    <div class="oquando"><small>Entregas</small></div>
    <div class="olista">
      <div><span>Etapa A</span></div>
      <div><span>Etapa B</span></div>
    </div>
  </div>
  <div class="cn reveal" data-passo="3" style="--d:.05s">
    <i class="cor cat-3"></i>
    <div class="on">03</div>
    <div class="onome">Item 3</div>
    <div class="odesc">Descrição curta do item 3</div>
    <div class="oquando"><small>Quando</small>Período 1</div>
  </div>
  <div class="cn reveal" data-passo="4" style="--d:.05s">
    <i class="cor cat-4"></i>
    <div class="on">04</div>
    <div class="onome">Item 4</div>
    <div class="odesc">Descrição curta do item 4</div>
    <div class="oquando"><small>Quando</small>Período 2</div>
  </div>
  <div class="cn reveal" data-passo="5" style="--d:.05s">
    <i class="cor cat-5"></i>
    <div class="on">05</div>
    <div class="onome">Item 5</div>
    <div class="odesc">Descrição curta do item 5</div>
    <div class="oquando"><small>Quando</small>Período 3</div>
  </div>
</div>
```
