# Etapas em trilho
- **Serve para:** mostrar uma sequência de três etapas ao longo de um trilho, com a última destacada.
- **Quando usar:** linha do tempo curta (passado, presente, saída) ou passo a passo de 3 etapas.
- **Quando não usar:** mais de 3 etapas, ou etapas com muito texto.
- **Passos de clique:** 1) trilho estica e a primeira etapa aparece; 2) segunda etapa; 3) terceira etapa, destacada, e o trecho final do trilho em laranja.
- **Editáveis:** `.etapa .rot, .etapa p`
## CSS
```css
.tempo { position: relative; }
.tempo .trilho { position: absolute; top: 15px; left: 0; right: 0; height: 4px; background: var(--cinza-claro); border-radius: 2px; }
.tempo .trilho .fim { position: absolute; left: 66.6%; right: 0; top: 0; bottom: 0; background: var(--laranja); border-radius: 2px; }
.tempo .etapas { display: grid; grid-template-columns: repeat(3, 1fr); gap: 40px; position: relative; }
.etapa .ponto { width: 34px; height: 34px; border-radius: 50%; background: var(--branco); border: 5px solid var(--cinza-claro); }
.etapa.destaque .ponto { border-color: var(--laranja); background: var(--laranja); box-shadow: 0 0 0 10px var(--laranja-16); }
.etapa .rot { font-size: 22px; font-weight: 700; letter-spacing: .1em; text-transform: uppercase; color: var(--cinza-escuro); margin-top: 22px; }
.etapa.destaque .rot { color: var(--laranja); }
.etapa p { font-size: 30px; line-height: 1.3; margin-top: 8px; padding-right: 20px; }
.etapa b { font-weight: 800; }
```
## HTML
```html
<div class="tempo">
  <div class="trilho estica" data-passo="1" style="--d:0s"><div class="fim estica" data-passo="3"></div></div>
  <div class="etapas">
    <div class="etapa reveal" data-passo="1" style="--d:.3s">
      <div class="ponto"></div>
      <div class="rot">Etapa um</div>
      <p>Descrição curta da primeira etapa.</p>
    </div>
    <div class="etapa reveal" data-passo="2" style="--d:.05s">
      <div class="ponto"></div>
      <div class="rot">Etapa dois</div>
      <p>Descrição curta da segunda etapa, com um <b data-conta>42</b> em destaque.</p>
    </div>
    <div class="etapa destaque reveal" data-passo="3" style="--d:.05s">
      <div class="ponto"></div>
      <div class="rot">Etapa três</div>
      <p>Descrição curta da etapa final, a que se quer destacar.</p>
    </div>
  </div>
</div>
```
