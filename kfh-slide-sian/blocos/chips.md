# Chips
- **Serve para:** listar rótulos curtos (itens com data, tags, categorias) em pílulas de contorno azul que quebram de linha.
- **Quando usar:** complemento de um cartão ou de uma lista, com 2 a 6 rótulos de poucas palavras.
- **Quando não usar:** frases longas (use lista com marcadores), ou rótulos que precisam de destaque de cor (use as categorias da base).
- **Passos de clique:** nenhum próprio; entra junto com o elemento que o contém.
- **Editáveis:** `.chips span`
## CSS
```css
.chips { display: flex; flex-wrap: wrap; gap: 8px; margin-top: 14px; }
.chips span { font-size: 18px; font-weight: 700; color: var(--azul); border: 2px solid var(--azul); border-radius: 20px; padding: 3px 14px; }
```
## HTML
```html
<div class="chips"><span>Rótulo 1 · dd/mm</span><span>Rótulo 2 · dd/mm</span><span>Rótulo 3</span></div>
```
