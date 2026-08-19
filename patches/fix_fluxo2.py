with open('index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Lines are 0-indexed, so line 435 is index 434, line 436 is index 435
# Replace lines 435 and 436 (indices 434 and 435)
# Insert correct HTML

new_lines = lines[:434]  # Up to line 434 (index 433), keep </div> at line 434
new_lines.append('\n')  # blank line
new_lines.append('<!-- ABA 3: FLUXO DE VISTORIAS -->\n')
new_lines.append('<div id="aba-fluxo" class="tab-content">\n')
new_lines.append('    <div class="card">\n')
new_lines.append('        <h2>Fluxo de Vistorias VTO</h2>\n')
# Skip the corrupted lines 435-436 (indices 434-435) and continue from line 437 (index 436)
# But we also need to remove the extra </div> and <div class="card"> that were in the corrupted line
new_lines.extend(lines[437:])  # From line 438 onwards

with open('index.html', 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print('Arquivo corrigido!')
