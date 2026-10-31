# Destaque e lista
- **Serve para:** um cartão azul de destaque (título, total e linhas de detalhe) ao lado de uma lista de itens com marcador de cor, nome e valor.
- **Quando usar:** um item principal que merece detalhe, mais 2 a 4 itens secundários com a mesma medida (horas, valores, quantidades).
- **Quando não usar:** itens de mesmo peso (use cartões numerados), ou lista sem item principal.
- **Passos de clique:** 1) cartão de destaque entra; 2) a cada clique, uma linha de detalhe do destaque; depois, a lista e, a cada clique, um item dela.
- **Editáveis:** `.destaque-mes .rot-m, .destaque-mes .tit-m, .destaque-mes .hrs-m, .destaque-mes .sub-m, .destaque-mes .linhas-m span, .lista-mes .rot-l, .lista-mes .nm, .lista-mes .hm`
## CSS
```css
.destaque-lista { flex-shrink: 0; display: grid; grid-template-columns: 660px 1fr; gap: 56px; }
.destaque-mes { background: var(--azul); color: var(--branco); border-radius: 24px; padding: 26px 40px 22px; }
.destaque-mes .rot-m { font-size: 21px; font-weight: 700; letter-spacing: .12em; text-transform: uppercase; color: var(--laranja); }
.destaque-mes .topo-m { display: flex; justify-content: space-between; align-items: baseline; margin-top: 4px; }
.destaque-mes .tit-m { font-size: 42px; font-weight: 800; }
.destaque-mes .hrs-m { font-size: 60px; font-weight: 800; color: var(--laranja); font-variant-numeric: tabular-nums; }
.destaque-mes .sub-m { font-size: 20px; color: var(--cinza-claro); margin-top: 2px; }
.destaque-mes .linhas-m { margin-top: 12px; }
.destaque-mes .linhas-m div { display: flex; justify-content: space-between; font-size: 26px; font-weight: 600; padding: 8px 0; border-top: 2px solid var(--branco-18); }
.destaque-mes .linhas-m div span:last-child { font-weight: 800; font-variant-numeric: tabular-nums; }
.lista-mes .rot-l { font-size: 22px; font-weight: 700; letter-spacing: .1em; text-transform: uppercase; color: var(--cinza-escuro); margin-bottom: 6px; }
.lista-mes .item { display: grid; grid-template-columns: 34px 1fr auto; align-items: center; gap: 0 14px; padding: 14px 0; border-bottom: 2px solid var(--divisor); }
.lista-mes .item i { width: 26px; height: 26px; border-radius: 7px; }
.lista-mes .nm { font-size: 28px; font-weight: 700; line-height: 1.15; }
.lista-mes .nm small { display: block; font-size: 18px; font-weight: 500; color: var(--cinza-escuro); margin-top: 2px; }
.lista-mes .hm { font-size: 40px; font-weight: 800; font-variant-numeric: tabular-nums; }
```
## HTML
```html
<div class="destaque-lista">
  <div class="destaque-mes reveal" data-passo="1" style="--d:.05s">
    <div class="rot-m">Prioridade 1 · até dd/mm</div>
    <div class="topo-m"><span class="tit-m">Item principal</span><span class="hrs-m" data-conta>70h</span></div>
    <div class="sub-m">Descrição curta do item principal</div>
    <div class="linhas-m">
      <div class="reveal" data-passo="2" style="--d:.15s"><span>Etapa A</span><span data-conta>30h</span></div>
      <div class="reveal" data-passo="3" style="--d:.15s"><span>Etapa B</span><span data-conta>20h</span></div>
      <div class="reveal" data-passo="4" style="--d:.15s"><span>Etapa C</span><span data-conta>20h</span></div>
    </div>
  </div>
  <div class="lista-mes reveal" data-passo="5" style="--d:.05s">
    <div class="rot-l">O restante · 50h</div>
    <div class="item reveal" data-passo="5" style="--d:.15s"><i class="cat-2"></i><div class="nm">Item 2<small>Detalhe do item 2</small></div><div class="hm" data-conta>20h</div></div>
    <div class="item reveal" data-passo="6" style="--d:.15s"><i class="cat-3"></i><div class="nm">Item 3<small>Detalhe do item 3</small></div><div class="hm" data-conta>20h</div></div>
    <div class="item reveal" data-passo="7" style="--d:.15s"><i class="cat-4"></i><div class="nm">Item 4</div><div class="hm" data-conta>10h</div></div>
  </div>
</div>
```
