import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Find and fix the corrupted fluxo tab start
old_bad = '''<!-- ABA 3: FLUXO DE VISTORIAS -->
<div id=aba-dilacao class=aba-dilacao    <div class=aba-dilacao        <h2>Fluxo de Vistorias VTO</h2>'''

new_good = '''<!-- ABA 3: FLUXO DE VISTORIAS -->
<div id="aba-fluxo" class="tab-content">
    <div class="card">
        <h2>Fluxo de Vistorias VTO</h2>'''

if old_bad in content:
    content = content.replace(old_bad, new_good)
    print('Correcao aplicada com sucesso!')
else:
    print('Padrao nao encontrado. Verificando conteudo...')
    # Show what's around line 435
    lines = content.split('\n')
    for i, line in enumerate(lines[430:445], start=431):
        print(f'{i}: {line}')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)
