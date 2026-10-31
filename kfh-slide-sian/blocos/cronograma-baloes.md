# Cronograma com balões
- **Serve para:** mostrar entregas datadas numa linha do tempo, com balões acima (lado azul) e abaixo (lado laranja) da linha, ligados por hastes.
- **Quando usar:** de 5 a 12 entregas de duas frentes ou responsáveis, em um período conhecido. Posição de cada evento: `left = (dias desde o início ÷ dias do período) × 100%`. Exemplo: início em 01/01, período de 64 dias, evento em 17/01 (16 dias) fica em `left:25%`. Os balões entram um por clique, em ordem de data.
- **Chaves opcionais:** `.ev-per` (laranja, abaixo da linha) para uma entrega que cobre um período e tem subetapas, uma por clique (`.ev-etapas`); `--ini` é onde a chave começa, em % da largura do próprio elemento. `.ev-mes` (azul, acima da linha) para várias entregas num intervalo sem data fechada, listadas em `.ev-lin`. Use só quando houver esse caso; no cronograma comum, balões bastam.
- **Quando não usar:** poucos marcos (use linha do tempo com cartões), ou entregas sem data.
- **Passos de clique:** um balão por clique, em ordem de data (faixas de período, início e legenda já aparecem).
- **Editáveis:** `.cr-leg span, .cr-faixa, .cr-ini, .ev-data, .ev-nome, .ev-tag`
## CSS
```css
/* Lados: .ev.a = azul, balão ACIMA da linha; .ev.b = laranja, balão ABAIXO.
   --h = altura da haste: escalone (36px, 100px, 175px) quando datas próximas fariam balões se cruzar.
   .esq = balão abre para a ESQUERDA da haste (use perto do fim do período, para não sair do slide). */
.crono { position: relative; height: 600px; }
.crono .cr-eixo { position: absolute; top: 300px; left: 0; right: 0; height: 0; }
.cr-leg { display: flex; gap: 28px; justify-content: flex-end; font-size: 22px; font-weight: 700; }
.cr-leg span { display: flex; align-items: center; gap: 10px; }
.cr-leg i { width: 22px; height: 22px; border-radius: 6px; }
.cr-leg .a i { background: var(--azul); }
.cr-leg .b i { background: var(--laranja); }
.cr-leg b { color: var(--cinza-escuro); font-weight: 600; }
.crono .cr-faixa { position: absolute; top: -17px; height: 34px; border-radius: 17px; display: flex; align-items: center; padding-left: 22px; font-size: 17px; font-weight: 700; letter-spacing: .14em; text-transform: uppercase; color: var(--cinza-escuro); background: var(--fundo-cartao); border: 2px solid var(--divisor); }
.crono .cr-ini { position: absolute; top: -52px; left: 0; font-size: 20px; font-weight: 700; color: var(--cinza-escuro); font-variant-numeric: tabular-nums; }
.crono .ev { position: absolute; top: 0; width: 0; height: 0; }
.ev::before { content: ""; position: absolute; left: -0.5px; width: 1px; height: var(--h); }
.ev.a::before { bottom: 0; background: var(--azul); }
.ev.b::before { top: 0; background: var(--laranja); }
.ev i { position: absolute; left: -12px; top: -12px; width: 24px; height: 24px; border-radius: 50%; border: 4px solid var(--branco); z-index: 1; }
.ev.a i { background: var(--azul); box-shadow: 0 0 0 2px var(--azul); }
.ev.b i { background: var(--laranja); box-shadow: 0 0 0 2px var(--laranja); }
.ev .ev-card { position: absolute; left: -5px; width: 250px; padding: 12px 18px 14px 16px; border-radius: 16px; background: var(--fundo-cartao); color: var(--azul); border: 1.5px solid; border-left-width: 10px; }
.ev.esq .ev-card { left: auto; right: -0.5px; }
.ev.a .ev-card { bottom: var(--h); border-color: var(--azul); border-bottom-left-radius: 6px; }
.ev.a.esq .ev-card { border-bottom-left-radius: 16px; border-bottom-right-radius: 6px; }
.ev.b .ev-card { top: var(--h); border-color: var(--laranja); border-top-left-radius: 6px; }
.ev.b.esq .ev-card { border-top-left-radius: 16px; border-top-right-radius: 6px; }
.ev-data { font-size: 18px; font-weight: 800; letter-spacing: .08em; text-transform: uppercase; font-variant-numeric: tabular-nums; }
.ev.a .ev-data { color: var(--azul); opacity: .75; }
.ev.b .ev-data { color: var(--laranja); }
.ev-nome { font-size: 23px; font-weight: 800; line-height: 1.15; margin-top: 2px; }
.ev-tag { display: inline-block; margin-top: 8px; font-size: 14px; font-weight: 700; letter-spacing: .08em; text-transform: uppercase; padding: 3px 10px; border-radius: 10px; background: var(--divisor); color: var(--azul); }
/* Chave de período (lado b, ABAIXO da linha): cobre um período e abre um cartão de subetapas.
   Posição e largura do elemento em style="left:..;width:..". --ini = onde a chave começa, em % da largura do próprio elemento. */
.crono .ev-per { position: absolute; top: 0; height: 0; }
.crono .ev-per::before { content: ""; position: absolute; left: var(--ini, 0%); right: 0; top: 20px; height: 14px; border: 1px solid var(--laranja); border-top: 0; border-radius: 0 0 6px 6px; }
.crono .ev-per .ev-card { position: absolute; top: 42px; left: 0; width: 400px; border-color: var(--laranja); }
.crono .ev-per .ev-data { color: var(--laranja); }
.crono .ev-etapas > div { display: grid; grid-template-columns: 112px 1fr; gap: 0 8px; font-size: 19px; font-weight: 700; line-height: 1.25; padding: 5px 0; border-top: 2px solid var(--divisor); margin-top: 6px; }
.crono .ev-etapas b { color: var(--laranja); font-weight: 800; font-variant-numeric: tabular-nums; }
/* Chave de intervalo (lado a, ACIMA da linha): cobre um intervalo sem data fechada e abre um cartão de linhas.
   Posição e largura do elemento em style="left:..;width:..". */
.crono .ev-mes { position: absolute; top: 0; height: 0; }
.crono .ev-mes::before { content: ""; position: absolute; left: 0; right: 0; bottom: 20px; height: 14px; border: 1px solid var(--azul); border-bottom: 0; border-radius: 6px 6px 0 0; }
.crono .ev-mes .ev-card { position: absolute; left: auto; right: 0; bottom: 46px; width: 470px; border-color: var(--azul); }
.crono .ev-mes .ev-data { color: var(--azul); opacity: .75; }
.crono .ev-lin > div { display: flex; justify-content: space-between; align-items: center; font-size: 23px; font-weight: 700; padding: 6px 0; border-top: 2px solid var(--divisor); margin-top: 6px; }
.crono .ev-lin .ev-tag { margin-top: 0; }
```
## HTML
```html
<div class="crono">
  <div class="cr-leg reveal" style="--d:.25s">
    <span class="a"><i></i>Frente A <b data-conta>· 4 entregas</b></span>
    <span class="b"><i></i>Frente B <b data-conta>· 5 entregas</b></span>
  </div>
  <!-- Período fictício de 64 dias, de 01/01 a 06/03. Posição: (dias desde o início ÷ 64) × 100%.
       Faixas de período: posição e largura em style="left:..;width:.." (a soma fecha 100%). -->
  <div class="cr-eixo">
    <div class="cr-faixa reveal" style="left:0; width:calc(50% - 3px); --d:.3s">Período 1</div>
    <div class="cr-faixa reveal" style="left:calc(50% + 3px); width:calc(50% - 3px); --d:.35s">Período 2</div>
    <div class="cr-ini reveal" style="--d:.4s">01/01</div>

    <div class="ev a reveal" data-passo="1" style="left:12.5%; --h:36px; --d:.05s"><i></i>
      <div class="ev-card"><div class="ev-data">09/01</div><div class="ev-nome">Entrega 1</div><span class="ev-tag">Etiqueta</span></div></div>
    <div class="ev b reveal" data-passo="2" style="left:25%; --h:130px; --d:.05s"><i></i>
      <div class="ev-card"><div class="ev-data">17/01</div><div class="ev-nome">Entrega 2</div><span class="ev-tag">Etiqueta</span></div></div>
    <div class="ev a reveal" data-passo="3" style="left:40.625%; --h:36px; --d:.05s"><i></i>
      <div class="ev-card"><div class="ev-data">27/01</div><div class="ev-nome">Entrega 3</div><span class="ev-tag">Etiqueta</span></div></div>
    <div class="ev b reveal" data-passo="4" style="left:50%; --h:36px; --d:.05s"><i></i>
      <div class="ev-card"><div class="ev-data">02/02</div><div class="ev-nome">Entrega 4</div><span class="ev-tag">Etiqueta</span></div></div>
    <div class="ev b reveal" data-passo="5" style="left:75%; --h:160px; --d:.05s"><i></i>
      <div class="ev-card"><div class="ev-data">18/02</div><div class="ev-nome">Entrega 5</div><span class="ev-tag">Etiqueta</span></div></div>
    <div class="ev b esq reveal" data-passo="6" style="left:100%; --h:36px; --d:.05s"><i></i>
      <div class="ev-card"><div class="ev-data">06/03</div><div class="ev-nome">Entrega 6</div><span class="ev-tag">Etiqueta</span></div></div>

    <!-- Chave de período (opcional, abaixo da linha): uma subetapa por clique. Cobre de 0% a 25% do período;
         --ini:37.5% faz a chave começar em 37,5% da largura do elemento (a data da primeira subetapa). -->
    <div class="ev-per reveal" data-passo="7" style="left:0; width:25%; --ini:37.5%; --d:.05s">
      <div class="ev-card"><div class="ev-nome">Entrega com subetapas</div>
        <div class="ev-etapas">
          <div class="reveal" data-passo="7" style="--d:.2s"><b>04 a 06/01</b><span>Subetapa A</span></div>
          <div class="reveal" data-passo="8" style="--d:.05s"><b>07/01</b><span>Subetapa B</span></div>
          <div class="reveal" data-passo="9" style="--d:.05s"><b>17/01</b><span>Subetapa C</span></div>
        </div>
      </div>
    </div>

    <!-- Chave de intervalo (opcional, acima da linha): cobre a metade final do período, sem data fechada. -->
    <div class="ev-mes reveal" data-passo="10" style="left:calc(50% + 3px); width:calc(50% - 3px); --d:.05s">
      <div class="ev-card"><div class="ev-data">Ao longo do período 2</div>
        <div class="ev-lin">
          <div class="reveal" data-passo="10" style="--d:.2s"><span>Entrega A</span><span class="ev-tag">Etiqueta</span></div>
          <div class="reveal" data-passo="11" style="--d:.05s"><span>Entrega B</span><span class="ev-tag">Etiqueta</span></div>
        </div>
      </div>
    </div>
  </div>
</div>
```
