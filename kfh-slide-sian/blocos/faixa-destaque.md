# Faixa de destaque
- **Serve para:** fechar um slide com uma frase de síntese em faixa, com barra laranja à esquerda.
- **Quando usar:** logo abaixo de outro bloco (dois cenários, dois lados), para dizer o que muda ou o que concluir.
- **Quando não usar:** como bloco único do slide, ou com mais de duas linhas de texto.
- **Passos de clique:** 1) a faixa sobe e aparece (use um número de passo depois dos blocos acima).
- **Editáveis:** `.faixa`
## CSS
```css
.faixa { background: var(--fundo-cartao); border-left: 8px solid var(--laranja); border-radius: 0 14px 14px 0; padding: 18px 30px; font-size: 25px; line-height: 1.35; }
.faixa b { font-weight: 800; }
```
## HTML
```html
<div class="faixa reveal" data-passo="3" style="--d:.05s"><b>Em resumo:</b> frase curta que explica a diferença ou a conclusão do slide.</div>
```
