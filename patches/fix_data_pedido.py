with open('index.html', 'r', encoding='utf-8') as f:
    s = f.read()

# Adiciona oninput no campo dataPedidoOriginal
old_input = 'id="dataPedidoOriginal" placeholder="DD/MM/AAAA" maxlength="10"><button type="button" class="btn-calendario" onclick="abrirCalendario(\'dataPedidoOriginal\')"'
new_input = 'id="dataPedidoOriginal" placeholder="DD/MM/AAAA" maxlength="10" oninput="calcularDilacaoCasoEspecial()"><button type="button" class="btn-calendario" onclick="abrirCalendario(\'dataPedidoOriginal\')"'

if old_input in s:
    s = s.replace(old_input, new_input)
    print('oninput adicionado ao dataPedidoOriginal.')
else:
    print('Nao encontrou o campo dataPedidoOriginal.')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(s)
