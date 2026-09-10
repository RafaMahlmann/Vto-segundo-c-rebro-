import re

with open('index.html', 'r', encoding='utf-8') as f:
    s = f.read()

# 1. Texto na dica-box
s = s.replace('<strong>Caso especial</strong>', '<strong>Casos especiais, sugestao de procedimento</strong>')

# 2. Titulo da secao
s = s.replace('<h3 class="secao-titulo">Caso especial', '<h3 class="secao-titulo">Casos especiais, sugestao de procedimento')

# 3. Label do input
s = s.replace('<label for="dataPedidoOriginal">Data do Pedido Original</label>', '<label for="dataPedidoOriginal">Data do Pedido do Documento</label>')

# 4. Mensagem de erro no JS
s = s.replace("A data do pedido original nao pode ser no futuro.", "A data do pedido do documento nao pode ser no futuro.")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(s)

print('Textos alterados com sucesso.')
