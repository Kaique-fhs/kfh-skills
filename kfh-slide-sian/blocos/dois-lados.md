# Dois lados
- **Serve para:** confrontar duas posições, perfis ou opções lado a lado, com um "×" no meio.
- **Quando usar:** duas partes com lista curta de pontos cada (2 a 3 itens por lado).
- **Quando não usar:** mais de duas partes, ou comparação com números (use dois cenários).
- **Passos de clique:** 1) lado destacado entra pela esquerda; 2) "×" cresce e o lado claro entra pela direita.
- **Editáveis:** `.lado .quem, .lado .nome, .lado li`
## CSS
```css
.lados { display: grid; grid-template-columns: 1fr 140px 1fr; align-items: stretch; }
.lado { border-radius: 28px; padding: 44px 52px; position: relative; }
.lado.destaque { background: var(--azul); color: var(--branco); }
.lado.claro { background: var(--fundo-cartao); border: 3px solid var(--cinza-claro); }
.lado .quem { font-size: 23px; font-weight: 700; letter-spacing: .12em; text-transform: uppercase; color: var(--laranja); }
.lado .nome { font-size: 52px; font-weight: 800; margin-top: 4px; }
.lado ul { list-style: none; margin-top: 22px; }
.lado li { font-size: 30px; line-height: 1.32; padding-left: 34px; position: relative; margin-top: 14px; }
.lado li::before { content: ""; position: absolute; left: 0; top: 13px; width: 14px; height: 14px; border-radius: 50%; background: var(--laranja); }
.versus { display: flex; align-items: center; justify-content: center; }
.versus span { width: 92px; height: 92px; border-radius: 50%; background: var(--branco); border: 3px solid var(--cinza-claro); display: flex; align-items: center; justify-content: center; font-size: 44px; font-weight: 800; color: var(--laranja); }
```
## HTML
```html
<div class="lados">
  <div class="lado destaque reveal da-esquerda" data-passo="1" style="--d:.05s">
    <div class="quem">Papel A</div>
    <div class="nome">Posição A</div>
    <ul>
      <li>Primeiro ponto da posição A</li>
      <li>Segundo ponto da posição A</li>
    </ul>
  </div>
  <div class="versus"><span class="reveal cresce" data-passo="2" style="--d:.35s">×</span></div>
  <div class="lado claro reveal da-direita" data-passo="2" style="--d:.05s">
    <div class="quem">Papel B</div>
    <div class="nome">Posição B</div>
    <ul>
      <li>Primeiro ponto da posição B</li>
      <li>Segundo ponto da posição B</li>
    </ul>
  </div>
</div>
```
