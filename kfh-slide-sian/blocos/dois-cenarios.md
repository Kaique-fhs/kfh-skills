# Dois cenários
- **Serve para:** comparar dois cenários numéricos, cada um com equação, barra de proporção e linhas de detalhe.
- **Quando usar:** duas alternativas com resultado em números (valor inicial, ajuste, valor final).
- **Quando não usar:** comparação só de texto (use dois lados), ou mais de dois cenários.
- **Passos de clique:** 1) cenário A (base); 2) cenário B (comparativo).
- **Editáveis:** `.cenario .rot-c, .cenario .tit-c, .termo .legenda, .linha span`
## CSS
```css
.cenarios { display: grid; grid-template-columns: minmax(0, 1fr) minmax(0, 1fr); gap: 40px; }
.cenario { border-radius: 26px; padding: 30px 40px 24px; }
.cenario.a { background: var(--azul); color: var(--branco); }
.cenario.b { background: var(--fundo-cartao); border: 3px solid var(--cinza-claro); }
.cenario .rot-c { font-size: 21px; font-weight: 700; letter-spacing: .12em; text-transform: uppercase; color: var(--laranja); }
.cenario .tit-c { font-size: 38px; font-weight: 800; margin-top: 4px; }
.equacao { display: grid; grid-template-columns: 1fr 36px 1fr 36px 1fr; align-items: center; margin-top: 22px; }
.termo { text-align: center; }
.termo .valor { font-size: 52px; font-weight: 800; line-height: 1; font-variant-numeric: tabular-nums; }
.termo .legenda { font-size: 19px; margin-top: 8px; color: var(--cinza-escuro); }
.cenario.a .termo .legenda { color: var(--cinza-claro); }
.termo.final .valor { color: var(--laranja); }
.op { text-align: center; font-size: 54px; font-weight: 300; color: var(--cinza-escuro); }
.cenario.a .op { color: var(--cinza-claro); }
.barra-saldo { display: flex; height: 46px; gap: 4px; margin-top: 22px; border-radius: 10px; overflow: hidden; }
.barra-saldo div { display: flex; align-items: center; padding: 0 18px; font-size: 19px; font-weight: 700; white-space: nowrap; }
.barra-saldo .parte { background: var(--laranja); color: var(--branco); }
.barra-saldo .resto { flex: 1; background: var(--cinza-claro); color: var(--azul); justify-content: flex-end; }
.linhas-c { margin-top: 14px; }
.linha { display: flex; justify-content: space-between; align-items: baseline; font-size: 25px; padding: 9px 0; border-bottom: 2px solid var(--divisor); }
.cenario.a .linha { border-bottom-color: var(--branco-18); }
.linha span:last-child { font-weight: 700; font-variant-numeric: tabular-nums; }
.linha.total { border-bottom: none; }
.linha.total span { font-weight: 800; }
.linha.total span:last-child { color: var(--laranja); }
```
## HTML
```html
<div class="cenarios">
  <div class="cenario a reveal" data-passo="1" style="--d:.05s">
    <div class="rot-c">Cenário A · base</div>
    <div class="tit-c">Título do cenário A</div>
    <div class="equacao">
      <div class="termo"><div class="valor" data-minutos="6000">100h00m</div><div class="legenda">valor inicial</div></div>
      <div class="op">−</div>
      <div class="termo"><div class="valor" data-minutos="3000">50h00m</div><div class="legenda">ajuste</div></div>
      <div class="op">=</div>
      <div class="termo final"><div class="valor" data-minutos="3000">50h00m</div><div class="legenda">valor final</div></div>
    </div>
    <div class="barra-saldo estica" data-passo="1" style="--d:.3s">
      <div class="parte" style="width:50%">50h00m ajustadas · 50%</div>
      <div class="resto">50h00m ficam · 50%</div>
    </div>
    <div class="linhas-c">
      <div class="linha"><span>Primeira linha de detalhe</span><span data-conta>40</span></div>
      <div class="linha"><span>Segunda linha de detalhe</span><span data-conta>30h</span></div>
      <div class="linha total"><span>Total do cenário</span><span data-conta>~200h</span></div>
    </div>
  </div>
  <div class="cenario b reveal" data-passo="2" style="--d:.05s">
    <div class="rot-c">Cenário B · comparativo</div>
    <div class="tit-c">Título do cenário B</div>
    <div class="equacao">
      <div class="termo"><div class="valor" data-minutos="6000">100h00m</div><div class="legenda">valor inicial</div></div>
      <div class="op">−</div>
      <div class="termo"><div class="valor" data-minutos="2400">40h00m</div><div class="legenda">ajuste</div></div>
      <div class="op">=</div>
      <div class="termo final"><div class="valor" data-minutos="3600">60h00m</div><div class="legenda">valor final</div></div>
    </div>
    <div class="barra-saldo estica" data-passo="2" style="--d:.3s">
      <div class="parte" style="width:40%">40h00m ajustadas · 40%</div>
      <div class="resto">60h00m ficam · 60%</div>
    </div>
    <div class="linhas-c">
      <div class="linha"><span>Primeira linha de detalhe</span><span data-conta>30</span></div>
      <div class="linha"><span>Segunda linha de detalhe</span><span data-conta>20h</span></div>
      <div class="linha total"><span>Total do cenário</span><span data-conta>~220h</span></div>
    </div>
  </div>
</div>
```
