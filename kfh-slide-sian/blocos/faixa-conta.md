# Faixa de conta
- **Serve para:** mostrar uma conta em sequência (de um total até o resultado) numa faixa de caixas lado a lado.
- **Quando usar:** 3 a 6 números encadeados, em que o último é o resultado (caixa azul com o valor em laranja).
- **Quando não usar:** números sem relação de conta entre si (use cartões numerados), ou mais de 6 caixas.
- **Passos de clique:** 1) a faixa inteira entra de uma vez.
- **Editáveis:** `.faixa-conta b, .faixa-conta span`
## CSS
```css
.faixa-conta { display: flex; flex-shrink: 0; border: 2px solid var(--divisor); border-radius: 20px; overflow: hidden; }
.faixa-conta > div { flex: 1; padding: 16px 28px; border-right: 2px solid var(--divisor); }
.faixa-conta > div:last-child { border-right: none; background: var(--azul); }
.faixa-conta b { display: block; font-size: 40px; font-weight: 800; line-height: 1.05; font-variant-numeric: tabular-nums; }
.faixa-conta span { font-size: 19px; font-weight: 600; color: var(--cinza-escuro); }
.faixa-conta > div:last-child b { color: var(--laranja); }
.faixa-conta > div:last-child span { color: var(--cinza-claro); }
```
## HTML
```html
<div class="faixa-conta reveal" data-passo="1" style="--d:.05s">
  <div><b data-conta>22</b><span>legenda do total</span></div>
  <div><b data-conta>100h</b><span>legenda da base</span></div>
  <div><b data-conta>− 10h</b><span>legenda do ajuste</span></div>
  <div><b data-conta>90h</b><span>legenda do subtotal</span></div>
  <div><b data-conta>72h</b><span>legenda do resultado</span></div>
</div>
```
