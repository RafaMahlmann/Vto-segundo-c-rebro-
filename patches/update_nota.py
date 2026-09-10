with open('index.html', 'r', encoding='utf-8') as f:
    s = f.read()

old_nota = '''                <div class="nota-recomendacao" id="notaRecomendacao" style="display:none">
                    Se for servidor publico, habite-se, convenio com prefeitura ou interesse social, lance no sistema o valor total que ele pediu.<br>
                    Prazo final do pedido original: <span class="data-negrito" id="prazoFinalPedido">—</span>
                </div>'''

new_nota = '''                <div class="nota-recomendacao" id="notaRecomendacao" style="display:none">
                    <strong>Orientacao:</strong> casos especiais (orgaos publicos, escolas, habite-se, convenio com prefeitura ou interesse social) recebem prazo total direto. Demais casos comecam com 90 dias e, se necessario, analisam prazo maior depois.<br>
                    Prazo final do pedido original: <span class="data-negrito" id="prazoFinalPedido">—</span>
                </div>'''

if old_nota in s:
    s = s.replace(old_nota, new_nota)
    print('Nota atualizada.')
else:
    print('Nota nao encontrada.')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(s)
