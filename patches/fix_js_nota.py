with open('index.html', 'r', encoding='utf-8') as f:
    s = f.read()

# Remove a linha do ceNovaDataBase e a variavel novaDataBase
old_js = '''    const dataVencimento = new Date(hoje);
    dataVencimento.setDate(dataVencimento.getDate() + diasConceder);
    const novaDataBase = new Date(dataVencimento);
    document.getElementById('ceDecorridos').textContent = decorridos + ' dia(s)';
    document.getElementById('ceRestantes').textContent = restantes + ' dia(s)';
    document.getElementById('ceConcedidos').textContent = diasConceder + ' dia(s)';
    document.getElementById('ceFaltarao').textContent = faltarao + ' dia(s)';
    document.getElementById('ceVencimento').textContent = dataVencimento.toLocaleDateString('pt-BR',{weekday:'long',year:'numeric',month:'long',day:'numeric'});
    document.getElementById('ceNovaDataBase').textContent = novaDataBase.toLocaleDateString('pt-BR');
    document.getElementById('resultadoCasoEspecial').style.display = 'block';'''

new_js = '''    const dataVencimento = new Date(hoje);
    dataVencimento.setDate(dataVencimento.getDate() + diasConceder);
    const dataFinalPedido = new Date(dataPedido + 'T12:00:00');
    dataFinalPedido.setDate(dataFinalPedido.getDate() + diasTotais);
    document.getElementById('ceDecorridos').textContent = decorridos + ' dia(s)';
    document.getElementById('ceRestantes').textContent = restantes + ' dia(s)';
    document.getElementById('ceConcedidos').textContent = diasConceder + ' dia(s)';
    document.getElementById('ceFaltarao').textContent = faltarao + ' dia(s)';
    document.getElementById('ceVencimento').textContent = dataVencimento.toLocaleDateString('pt-BR',{weekday:'long',year:'numeric',month:'long',day:'numeric'});
    document.getElementById('prazoFinalPedido').textContent = dataFinalPedido.toLocaleDateString('pt-BR',{weekday:'long',year:'numeric',month:'long',day:'numeric'});
    document.getElementById('notaRecomendacao').style.display = 'block';
    document.getElementById('resultadoCasoEspecial').style.display = 'block';'''

if old_js in s:
    s = s.replace(old_js, new_js)
    print('JS atualizado com sucesso.')
else:
    print('Bloco JS nao encontrado.')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(s)
