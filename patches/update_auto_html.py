with open('index.html', 'r', encoding='utf-8') as f:
    s = f.read()

# 1. Adiciona oninput nos campos e remove o botao calcular
s = s.replace(
    '<div class="campo"><label for="dataPedidoOriginal">Data do Pedido do Documento</label><div class="data-input-wrap"><input type="text" id="dataPedidoOriginal" placeholder="DD/MM/AAAA" maxlength="10"><button type="button" class="btn-calendario" onclick="abrirCalendario(\'dataPedidoOriginal\')" title="Abrir calendario">&#128197;</button></div></div>',
    '<div class="campo"><label for="dataPedidoOriginal">Data do Pedido do Documento</label><div class="data-input-wrap"><input type="text" id="dataPedidoOriginal" placeholder="DD/MM/AAAA" maxlength="10" oninput="calcularDilacaoCasoEspecial()"><button type="button" class="btn-calendario" onclick="abrirCalendario(\'dataPedidoOriginal\')" title="Abrir calendario">&#128197;</button></div></div>'
)

s = s.replace(
    '<div class="campo"><label for="diasTotaisSolicitados">Dias totais do pedido antigo</label><input type="number" id="diasTotaisSolicitados" placeholder="Ex: 365" min="1"></div>',
    '<div class="campo"><label for="diasTotaisSolicitados">Dias totais do pedido antigo</label><input type="number" id="diasTotaisSolicitados" placeholder="Ex: 365" min="1" oninput="calcularDilacaoCasoEspecial()"></div>'
)

s = s.replace(
    '<div class="campo"><label for="diasConcederAgora">Dias para dar agora (padrao: 90)</label><input type="number" id="diasConcederAgora" value="90" min="1"></div>',
    '<div class="campo"><label for="diasConcederAgora">Dias para dar agora (padrao: 90)</label><input type="number" id="diasConcederAgora" value="90" min="1" oninput="calcularDilacaoCasoEspecial()"></div>'
)

s = s.replace(
    '<div class="campo"><label for="matriculaCasoEspecial">Numero da matricula (8 digitos)</label><input type="text" id="matriculaCasoEspecial" placeholder="Ex: 12345678" maxlength="8" oninput="this.value = this.value.replace(/\\D/g,\'\').slice(0,8)"></div>',
    '<div class="campo"><label for="matriculaCasoEspecial">Numero da matricula (8 digitos)</label><input type="text" id="matriculaCasoEspecial" placeholder="Ex: 12345678" maxlength="8" oninput="this.value = this.value.replace(/\\D/g,\'\').slice(0,8); calcularDilacaoCasoEspecial();"></div>'
)

s = s.replace(
    '<div class="campo"><label for="protocoloCasoEspecial">Numero do protocolo</label><input type="text" id="protocoloCasoEspecial" placeholder="Ex: 2026-00012345"></div>',
    '<div class="campo"><label for="protocoloCasoEspecial">Numero do protocolo</label><input type="text" id="protocoloCasoEspecial" placeholder="Ex: 2026-00012345" oninput="calcularDilacaoCasoEspecial()"></div>'
)

# 2. Remove o botao calcular
s = s.replace(
    '            <button class="btn-calcular btn-calcular--secundario" onclick="calcularDilacaoCasoEspecial()">Calcular prazo parcial</button>\n',
    ''
)

# 3. Remove display:none dos elementos de resultado
s = s.replace(
    '<div id="resultadoCasoEspecial"><h3>Resultado do Caso Especial</h3>',
    '<div id="resultadoCasoEspecial"><h3>Resultado do Caso Especial</h3>'
)

s = s.replace(
    '                <div class="nota-recomendacao" id="notaRecomendacao" style="display:none">',
    '                <div class="nota-recomendacao" id="notaRecomendacao">'
)

s = s.replace(
    '                <div class="resposta-gerada-wrap" id="respostaGeradaWrap" style="display:none">',
    '                <div class="resposta-gerada-wrap" id="respostaGeradaWrap">'
)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(s)

print('HTML atualizado: campos com oninput, botao removido, areas visiveis.')
