# Linha do tempo com cartões
- **Serve para:** mostrar marcos numa linha do tempo horizontal, com um cartão de data, nome e detalhe por marco logo abaixo.
- **Quando usar:** de 3 a 5 marcos com data e um período total conhecido (início e fim). Posição de cada marco: `left = (dias desde o início ÷ dias do período) × 100%`. Exemplo: início em 01/01, período de 60 dias, marco em 16/01 (15 dias) fica em `left:25%`. Os cartões seguem a ordem das datas, um por clique.
- **Quando não usar:** mais de 5 marcos (use cronograma com balões), ou etapas sem data (use etapas em trilho).
- **Passos de clique:** um marco e o cartão correspondente por clique, em ordem de data (o início e o trilho já aparecem).
- **Editáveis:** `.lt-mes, .lt-marco span, .lc-data, .lc-nome, .lc-desc, .lc-etapas div`
## CSS
```css
.linha-tempo { position: relative; height: 120px; margin: 0 40px; }
.linha-tempo .lt-trilho { position: absolute; top: 56px; left: 0; right: 0; height: 6px; border-radius: 3px; background: var(--cinza-claro); }
.linha-tempo .lt-mes { position: absolute; top: 0; font-size: 20px; font-weight: 700; letter-spacing: .12em; text-transform: uppercase; color: var(--cinza-escuro); }
.linha-tempo .lt-div { position: absolute; top: 34px; width: 2px; height: 50px; background: var(--cinza-claro); }
.linha-tempo .lt-marco { position: absolute; top: 44px; width: 0; }
.lt-marco i { position: absolute; left: -15px; width: 30px; height: 30px; border-radius: 50%; background: var(--laranja); box-shadow: 0 0 0 8px var(--laranja-16); }
.lt-marco span { position: absolute; top: 42px; left: -60px; width: 120px; text-align: center; font-size: 24px; font-weight: 800; font-variant-numeric: tabular-nums; }
.lt-marco.inicio i { background: var(--branco); border: 5px solid var(--cinza-claro); box-shadow: none; }
.lt-marco.inicio span { color: var(--cinza-escuro); font-weight: 700; left: -15px; text-align: left; }
.lt-marco.fim span { left: auto; right: -15px; text-align: right; }
.lc-cards { display: grid; grid-template-columns: repeat(5, 1fr); gap: 24px; margin-top: 40px; }
.lc { background: var(--fundo-cartao); border-radius: 22px; border-top: 12px solid var(--cinza-escuro); padding: 26px 28px 30px; min-height: 340px; }
.lc-etapas div { font-size: 19px; line-height: 1.3; color: var(--azul); margin-top: 8px; }
.lc-etapas b { display: block; font-size: 16px; font-weight: 800; letter-spacing: .06em; color: var(--laranja); }
.lc-data { font-size: 52px; font-weight: 800; color: var(--laranja); line-height: 1; font-variant-numeric: tabular-nums; }
.lc-data small { display: block; font-size: 18px; font-weight: 700; letter-spacing: .1em; text-transform: uppercase; color: var(--cinza-escuro); margin-bottom: 6px; }
.lc-nome { font-size: 32px; font-weight: 800; line-height: 1.15; margin-top: 22px; }
.lc-desc { font-size: 21px; line-height: 1.35; color: var(--cinza-escuro); margin-top: 10px; }
```
## HTML
```html
<!-- Período fictício de 60 dias, de 01/01 a 02/03. Posição: (dias desde o início ÷ 60) × 100% -->
<div class="linha-tempo reveal" style="--d:.3s">
  <div class="lt-trilho"></div>
  <div class="lt-mes" style="left:5%">Período 1</div>
  <div class="lt-mes" style="left:55%">Período 2</div>
  <div class="lt-div" style="left:50%"></div>
  <div class="lt-marco inicio" style="left:0%"><i></i><span>01/01</span></div>
  <div class="lt-marco reveal cresce" data-passo="1" style="left:25%; --d:.05s"><i></i><span>16/01</span></div>
  <div class="lt-marco reveal cresce" data-passo="2" style="left:40%; --d:.05s"><i></i><span>25/01</span></div>
  <div class="lt-marco reveal cresce" data-passo="3" style="left:70%; --d:.05s"><i></i><span>12/02</span></div>
  <div class="lt-marco fim reveal cresce" data-passo="4" style="left:100%; --d:.05s"><i></i><span>02/03</span></div>
</div>
<div class="lc-cards">
  <div class="lc reveal" data-passo="1" style="--d:.15s">
    <div class="lc-data"><small>até</small>16/01</div>
    <div class="lc-nome">Marco 1</div>
    <div class="lc-etapas">
      <div><b>dd a dd/mm</b>Etapa A</div>
      <div><b>dd/mm</b>Etapa B</div>
    </div>
  </div>
  <div class="lc reveal" data-passo="2" style="--d:.15s">
    <div class="lc-data"><small>até</small>25/01</div>
    <div class="lc-nome">Marco 2</div>
    <div class="lc-desc">Descrição curta do marco 2</div>
  </div>
  <div class="lc reveal" data-passo="3" style="--d:.15s">
    <div class="lc-data"><small>até</small>12/02</div>
    <div class="lc-nome">Marco 3</div>
    <div class="lc-desc">Descrição curta do marco 3</div>
  </div>
  <div class="lc reveal" data-passo="4" style="--d:.15s">
    <div class="lc-data"><small>até</small>02/03</div>
    <div class="lc-nome">Marco 4</div>
    <div class="lc-desc">Descrição curta do marco 4</div>
  </div>
</div>
```
