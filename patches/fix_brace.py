with open('index.html', 'r', encoding='utf-8') as f:
    s = f.read()

# Remove o } solitario entre copiarTexto e adicionarMatricula
old_bloco = '''function copiarTexto(id) {
    var ta = document.getElementById(id);
    ta.select();
    ta.setSelectionRange(0, 999999);
    try {
        document.execCommand('copy');
        alert('Texto copiado para a area de transferencia.');
    } catch (err) {
        alert('Nao foi possivel copiar automaticamente. Selecione o texto e use Ctrl+C.');
    }
}

}

// ===== ABA 4: MATRICULAS ====='''

new_bloco = '''function copiarTexto(id) {
    var ta = document.getElementById(id);
    ta.select();
    ta.setSelectionRange(0, 999999);
    try {
        document.execCommand('copy');
        alert('Texto copiado para a area de transferencia.');
    } catch (err) {
        alert('Nao foi possivel copiar automaticamente. Selecione o texto e use Ctrl+C.');
    }
}

// ===== ABA 4: MATRICULAS ====='''

if old_bloco in s:
    s = s.replace(old_bloco, new_bloco)
    print('} extra removido.')
else:
    print('Bloco nao encontrado.')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(s)
