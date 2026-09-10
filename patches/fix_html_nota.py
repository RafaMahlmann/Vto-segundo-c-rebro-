with open('index.html', 'r', encoding='utf-8') as f:
    s = f.read()

# Remove a linha "Nova data base para proximo pedido" e adiciona a nota no lugar
old_block = '''                    <div class="info-item destaque"><span class="info-label">Data de vencimento (prazo atual):</span><span class="info-valor" id="ceVencimento">—</span></div>
                    <div class="info-item"><span class="info-label">Nova data base para proximo pedido:</span><span class="info-valor" id="ceNovaDataBase">—</span></div>
                </div>
            </div>'''

new_block = '''                    <div class="info-item destaque"><span class="info-label">Data de vencimento (prazo atual):</span><span class="info-valor" id="ceVencimento">—</span></div>
                </div>
                <div class="nota-recomendacao" id="notaRecomendacao" style="display:none">
                    Se for servidor publico, habite-se, convenio com prefeitura ou interesse social, lance no sistema o valor total que ele pediu.<br>
                    Prazo final do pedido original: <span class="data-negrito" id="prazoFinalPedido">—</span>
                </div>
            </div>'''

if old_block in s:
    s = s.replace(old_block, new_block)
    print('HTML atualizado com sucesso.')
else:
    print('Bloco nao encontrado no HTML.')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(s)
