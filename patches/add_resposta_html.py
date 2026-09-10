with open('index.html', 'r', encoding='utf-8') as f:
    s = f.read()

# 1. Adiciona campo matricula antes do botao calcular
old_campos = '''            <div class="campo"><label for="diasConcederAgora">Dias para dar agora (padrao: 90)</label><input type="number" id="diasConcederAgora" value="90" min="1"></div>
            <button class="btn-calcular btn-calcular--secundario" onclick="calcularDilacaoCasoEspecial()">Calcular prazo parcial</button>'''

new_campos = '''            <div class="campo"><label for="diasConcederAgora">Dias para dar agora (padrao: 90)</label><input type="number" id="diasConcederAgora" value="90" min="1"></div>
            <div class="campo"><label for="matriculaCasoEspecial">Numero da matricula (8 digitos)</label><input type="text" id="matriculaCasoEspecial" placeholder="Ex: 12345678" maxlength="8" oninput="this.value = this.value.replace(/\\D/g,'').slice(0,8)"></div>
            <button class="btn-calcular btn-calcular--secundario" onclick="calcularDilacaoCasoEspecial()">Calcular prazo parcial</button>'''

s = s.replace(old_campos, new_campos)

# 2. Adiciona area de texto gerado dentro do resultadoCasoEspecial
old_resultado = '''                <div class="nota-recomendacao" id="notaRecomendacao" style="display:none">
                    Se for servidor publico, habite-se, convenio com prefeitura ou interesse social, lance no sistema o valor total que ele pediu.<br>
                    Prazo final do pedido original: <span class="data-negrito" id="prazoFinalPedido">—</span>
                </div>
            </div>'''

new_resultado = '''                <div class="nota-recomendacao" id="notaRecomendacao" style="display:none">
                    Se for servidor publico, habite-se, convenio com prefeitura ou interesse social, lance no sistema o valor total que ele pediu.<br>
                    Prazo final do pedido original: <span class="data-negrito" id="prazoFinalPedido">—</span>
                </div>
                <div class="resposta-gerada-wrap" id="respostaGeradaWrap" style="display:none">
                    <div class="resposta-gerada-header">
                        <span>Resposta para o cliente</span>
                        <button type="button" class="btn-copiar" onclick="copiarRespostaCasoEspecial()">Copiar texto</button>
                    </div>
                    <textarea id="respostaCasoEspecial" class="resposta-gerada-texto" readonly></textarea>
                </div>
            </div>'''

s = s.replace(old_resultado, new_resultado)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(s)

print('HTML atualizado com campo matricula e area de resposta.')
