# Barra empilhada
- **Serve para:** mostrar como um total se divide em partes proporcionais, numa barra única com legenda dentro de cada parte.
- **Quando usar:** de 2 a 5 categorias com valores somados (horas, orçamento, entregas). A largura de cada parte é `style="flex:<valor>"`, proporcional ao valor.
- **Quando não usar:** mais de 5 categorias: avise o usuário em vez de inventar cor, pois só existem `.cat-1` a `.cat-5` na base. Também não serve para comparar dois totais (use dois cenários).
- **Passos de clique:** um pedaço da barra por clique, da esquerda para a direita (o rótulo entra junto com o primeiro).
- **Editáveis:** `.rotulo-linha .t, .rotulo-linha .v, .empilhada div`
## CSS
```css
.barra-emp { width: 100%; flex-shrink: 0; }
.empilhada { display: flex; gap: 4px; border-radius: 14px; overflow: hidden; }
.empilhada div { display: flex; align-items: center; justify-content: center; font-weight: 700; white-space: nowrap; overflow: hidden; }
.rotulo-linha { display: flex; justify-content: space-between; align-items: baseline; margin-bottom: 12px; }
.rotulo-linha .t { font-size: 22px; font-weight: 700; letter-spacing: .1em; text-transform: uppercase; color: var(--cinza-escuro); }
.rotulo-linha .v { font-size: 30px; font-weight: 700; }
.rotulo-linha .v b { font-size: 40px; font-weight: 800; color: var(--laranja); margin-left: 8px; }
.empilhada.grande { height: 88px; }
.empilhada.grande div { flex-direction: column; font-size: 25px; line-height: 1.1; }
.empilhada.grande div small { font-size: 19px; font-weight: 600; opacity: .85; }
.empilhada.grande div.estreito { font-size: 18px; }
.empilhada.grande div.estreito small { font-size: 17px; }
```
## HTML
```html
<div class="barra-emp">
  <div class="rotulo-linha reveal" data-passo="1" style="--d:.05s"><span class="t">Como o total se divide</span><span class="v">Total <b>100h</b></span></div>
  <div class="empilhada grande">
    <div class="cat-1 estica" data-passo="1" style="flex:40">Categoria 1<small>40h · 40%</small></div>
    <div class="cat-2 estica" data-passo="2" style="flex:30">Categoria 2<small>30h · 30%</small></div>
    <div class="cat-3 estica" data-passo="3" style="flex:20">Categoria 3<small>20h · 20%</small></div>
    <div class="cat-4 estreito estica" data-passo="4" style="flex:6">Cat. 4<small>6h · 6%</small></div>
    <div class="cat-5 estreito estica" data-passo="5" style="flex:4">Cat. 5<small>4h · 4%</small></div>
  </div>
</div>
```
