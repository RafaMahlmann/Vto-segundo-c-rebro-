with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Substituir a funcao calcularDilacao() original por uma versao simplificada (sempre corridos)
old_func = '''function calcularDilacao() {
    const dataInicialTxt = document.getElementById('dataInicialDilacao').value;
    const dataInicial = textoParaISODate(dataInicialTxt);
    const quantidade = parseInt(document.getElementById('quantidadeDilacao').value);
    const tipoDias = document.getElementById('tipoDiasDilacao').value;
    if (!dataInicial || isNaN(quantidade) || quantidade < 1) { alert('Preencha todos os campos.'); return; }
    const data = new Date(dataInicial + 'T12:00:00');
    let dataFinal, diasUsados = 0;
    if (tipoDias === 'corridos') { dataFinal = new Date(data); dataFinal.setDate(dataFinal.getDate() + quantidade); diasUsados = quantidade; }
    else { dataFinal = new Date(data); let d = 0; while (d < quantidade) { dataFinal.setDate(dataFinal.getDate() + 1); if (dataFinal.getDay() !== 0 && dataFinal.getDay() !== 6) d++; } diasUsados = d; }
    const badgeClass = tipoDias === 'uteis' ? 'badge-util' : 'badge-corridos';
    document.getElementById('dataFinalDilacao').innerHTML = dataFinal.toLocaleDateString('pt-BR') + ' <span class="badge ' + badgeClass + '">' + (tipoDias === 'uteis' ? 'DIAS UTEIS' : 'DIAS CORRIDOS') + '</span>';
    document.getElementById('infoAdicionalDilacao').innerHTML = '<strong>' + dataFinal.toLocaleDateString('pt-BR',{weekday:'long',year:'numeric',month:'long',day:'numeric'}) + '</strong><br>Dilacao de <strong>' + diasUsados + ' ' + (tipoDias === 'uteis' ? 'dia(s) util(eis)' : 'dia(s) corrido(s)') + '</strong> a partir de ' + new Date(dataInicial + 'T12:00:00').toLocaleDateString('pt-BR') + '.';
    document.getElementById('resultadoDilacao').style.display = 'block';
}'''

new_func = '''function calcularDilacao() {
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

if old_func in content:
    content = content.replace(old_func, new_func)
    print('Funcao calcularDilacao() atualizada com sucesso.')
else:
    print('ERRO: Funcao original nao encontrada!')
    exit(1)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)
