with open('index.html', 'r', encoding='utf-8') as f:
    s = f.read()

# === ETAPA 1: Dilacao Simples — auto-calcular ===

# Remove botao "Calcular Data Final" e troca por um resultado sempre visivel
old_botao = '            <button class="btn-calcular" onclick="calcularDilacao()">Calcular Data Final</button>\n            <div id="resultadoDilacao"><h3>Resultado</h3><div class="data-final" id="dataFinalDilacao"></div><div class="info" id="infoAdicionalDilacao"></div></div>'

new_resultado = '            <div id="resultadoDilacao" style="margin-top:18px;display:none"><div class="data-final" id="dataFinalDilacao"></div><div class="info" id="infoAdicionalDilacao"></div></div>'

s = s.replace(old_botao, new_resultado)

# Adiciona oninput no campo dataInicialDilacao
s = s.replace(
    'id="dataInicialDilacao" placeholder="DD/MM/AAAA" maxlength="10"><button type="button" class="btn-calendario" onclick="abrirCalendario(\'dataInicialDilacao\')"',
    'id="dataInicialDilacao" placeholder="DD/MM/AAAA" maxlength="10" oninput="calcularDilacao()"><button type="button" class="btn-calendario" onclick="abrirCalendario(\'dataInicialDilacao\')"'
)

# Adiciona oninput no campo quantidadeDilacao
s = s.replace(
    'id="quantidadeDilacao" class="input-dias-manual" placeholder="Outro" min="1" oninput="validarDiasDilacao(this)">',
    'id="quantidadeDilacao" class="input-dias-manual" placeholder="Outro" min="1" oninput="validarDiasDilacao(this); calcularDilacao();">'
)

# Modifica setDiasDilacao para chamar calcularDilacao()
s = s.replace(
    'function setDiasDilacao(valor) {\n    document.getElementById(\'quantidadeDilacao\').value = valor;\n    document.querySelectorAll(\'.btn-dia-rapido\').forEach(btn => btn.classList.remove(\'ativo\'));\n    const btn = Array.from(document.querySelectorAll(\'.btn-dia-rapido\')).find(b => parseInt(b.textContent) === valor);\n    if (btn) btn.classList.add(\'ativo\');\n}',
    'function setDiasDilacao(valor) {\n    document.getElementById(\'quantidadeDilacao\').value = valor;\n    document.querySelectorAll(\'.btn-dia-rapido\').forEach(btn => btn.classList.remove(\'ativo\'));\n    const btn = Array.from(document.querySelectorAll(\'.btn-dia-rapido\')).find(b => parseInt(b.textContent) === valor);\n    if (btn) btn.classList.add(\'ativo\');\n    calcularDilacao();\n}'
)

# Modifica calcularDilacao para nao dar alert com campos vazios e mostrar resultado automatico
old_calc = '''function calcularDilacao() {
    const dataInicialTxt = document.getElementById('dataInicialDilacao').value;
    const dataInicial = textoParaISODate(dataInicialTxt);
    const quantidade = parseInt(document.getElementById('quantidadeDilacao').value);
    if (!dataInicial || isNaN(quantidade) || quantidade < 1) { alert('Preencha todos os campos.'); return; }
    const data = new Date(dataInicial + 'T12:00:00');
    const dataFinal = new Date(data);
    dataFinal.setDate(dataFinal.getDate() + quantidade);
    document.getElementById('dataFinalDilacao').innerHTML = dataFinal.toLocaleDateString('pt-BR') + ' <span class="badge badge-corridos">DIAS CORRIDOS</span>';
    document.getElementById('infoAdicionalDilacao').innerHTML = '<strong>' + dataFinal.toLocaleDateString('pt-BR',{weekday:'long',year:'numeric',month:'long',day:'numeric'}) + '</strong><br>Dilacao de <strong>' + quantidade + ' dia(s) corrido(s)</strong> a partir de ' + new Date(dataInicial + 'T12:00:00').toLocaleDateString('pt-BR') + '.';
    document.getElementById('resultadoDilacao').style.display = 'block';
}'''

new_calc = '''function calcularDilacao() {
    const dataInicialTxt = document.getElementById('dataInicialDilacao').value;
    const dataInicial = textoParaISODate(dataInicialTxt);
    const quantidade = parseInt(document.getElementById('quantidadeDilacao').value);
    if (!dataInicial || isNaN(quantidade) || quantidade < 1) {
        document.getElementById('resultadoDilacao').style.display = 'none';
        return;
    }
    const data = new Date(dataInicial + 'T12:00:00');
    const dataFinal = new Date(data);
    dataFinal.setDate(dataFinal.getDate() + quantidade);
    document.getElementById('dataFinalDilacao').innerHTML = dataFinal.toLocaleDateString('pt-BR') + ' <span class="badge badge-corridos">DIAS CORRIDOS</span>';
    document.getElementById('infoAdicionalDilacao').innerHTML = '<strong>' + dataFinal.toLocaleDateString('pt-BR',{weekday:'long',year:'numeric',month:'long',day:'numeric'}) + '</strong><br>Dilacao de <strong>' + quantidade + ' dia(s) corrido(s)</strong> a partir de ' + new Date(dataInicial + 'T12:00:00').toLocaleDateString('pt-BR') + '.';
    document.getElementById('resultadoDilacao').style.display = 'block';
}'''

s = s.replace(old_calc, new_calc)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(s)

print('Etapa 1 (Dilacao Simples auto-calcular) concluida.')
