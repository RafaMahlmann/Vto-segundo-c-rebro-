with open('index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Encontra a linha do segundo input.addEventListener('input'
idx_inicio = None
idx_fim = None
contador_input = 0
for i, line in enumerate(lines):
    if "input.addEventListener('input', function(e)" in line:
        contador_input += 1
        if contador_input == 2:
            idx_inicio = i
    if idx_inicio is not None and "// Ao perder foco" in line:
        idx_fim = i
        break

if idx_inicio is not None and idx_fim is not None:
    # Remove as linhas do segundo listener, deixando uma linha em branco antes do blur
    novas_linhas = lines[:idx_inicio] + lines[idx_fim:]
    with open('index.html', 'w', encoding='utf-8') as f:
        f.writelines(novas_linhas)
    print(f'Removido bloco duplicado: linhas {idx_inicio+1} ate {idx_fim}')
else:
    print(f'Nao encontrou bloco duplicado. contador_input={contador_input}, inicio={idx_inicio}, fim={idx_fim}')
