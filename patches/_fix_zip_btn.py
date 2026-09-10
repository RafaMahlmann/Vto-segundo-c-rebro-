import re

path = r'C:/Users/xrafa/Programas/vto-repo/index.html'
with open(path, encoding='utf-8') as f:
    t = f.read()

old = '    <button class="btn-ajuda" id="btnAjuda" onclick="toggleAjuda()">&#10067; Ajuda</button>'
new = '    <button class="btn-ajuda" id="btnAjuda" onclick="toggleAjuda()">&#10067; Ajuda</button>\n    <button class="btn-zip" onclick="gerarZipPortatil()" title="Gerar ZIP para compartilhar">&#128230; ZIP</button>'

if old in t:
    print('String encontrada!')
    t = t.replace(old, new, 1)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(t)
    print('Substituida com sucesso.')
else:
    print('String NAO encontrada.')
    # Procurar algo proximo
    idx = t.find('btnAjuda')
    if idx != -1:
        print('Encontrado btnAjuda em:', repr(t[idx-30:idx+100]))
