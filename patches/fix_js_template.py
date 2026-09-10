with open('index.html', 'r', encoding='utf-8') as f:
    s = f.read()

# Encontra o inicio e fim da funcao calcularDilacaoCasoEspecial
inicio = s.find('function calcularDilacaoCasoEspecial() {')
fim = s.find('function copiarRespostaCasoEspecial() {')

if inicio == -1 or fim == -1:
    print('Nao encontrou a funcao.')
    exit(1)

nova_func = '''function calcularDilacaoCasoEspecial() {
    const dataPedidoTxt = document.getElementById('dataPedidoOriginal').value;
    const dataPedido = textoParaISODate(dataPedidoTxt);
    const diasTotais = parseInt(document.getElementById('diasTotaisSolicitados').value);
    const diasConceder = parseInt(document.getElementById('diasConcederAgora').value);
    if (!dataPedido || isNaN(diasTotais) || diasTotais < 1 || isNaN(diasConceder) || diasConceder < 1) {
        alert('Preencha todos os campos do Caso Especial.'); return;
    }
    const hoje = new Date();
    const hojeIso = hoje.getFullYear() + '-' + String(hoje.getMonth()+1).padStart(2,'0') + '-' + String(hoje.getDate()).padStart(2,'0');
    const decorridos = calcularDiferencaDias(dataPedido, hojeIso);
    if (decorridos < 0) { alert('A data do pedido do documento nao pode ser no futuro.'); return; }
    const restantes = Math.max(0, diasTotais - decorridos);
    const faltarao = Math.max(0, restantes - diasConceder);
    const dataVencimento = new Date(hoje);
    dataVencimento.setDate(dataVencimento.getDate() + diasConceder);
    const dataFinalPedido = new Date(dataPedido + 'T12:00:00');
    dataFinalPedido.setDate(dataFinalPedido.getDate() + diasTotais);
    document.getElementById('ceDecorridos').textContent = decorridos + ' dia(s)';
    document.getElementById('ceRestantes').textContent = restantes + ' dia(s)';
    document.getElementById('ceConcedidos').textContent = diasConceder + ' dia(s)';
    document.getElementById('ceFaltarao').textContent = faltarao + ' dia(s)';
    document.getElementById('ceVencimento').textContent = dataVencimento.toLocaleDateString('pt-BR',{weekday:'long',year:'numeric',month:'long',day:'numeric'});
    document.getElementById('prazoFinalPedido').textContent = dataFinalPedido.toLocaleDateString('pt-BR',{weekday:'long',year:'numeric',month:'long',day:'numeric'});
    document.getElementById('notaRecomendacao').style.display = 'block';
    document.getElementById('resultadoCasoEspecial').style.display = 'block';

    // Dados comuns
    const matricula = document.getElementById('matriculaCasoEspecial').value.trim() || '________';
    const protocolo = document.getElementById('protocoloCasoEspecial').value.trim() || '________';
    const dataVencStr = dataVencimento.toLocaleDateString('pt-BR',{weekday:'long',year:'numeric',month:'long',day:'numeric'});
    var resposta = '';

    if (diasConceder >= diasTotais) {
        // MODELO 2: Prazo especial direto (orgaos publicos, escolas, habite-se, convenio, interesse social)
        resposta = `Prezado cliente,\n\nA respeito da matricula ${matricula}, informamos que sua solicitacao foi aceita e foi concedido prazo de ${diasConceder} dias para regularizacao, conforme protocolo ${protocolo}.\n\nO prazo vencera em ${dataVencStr}.\n\nAtenciosamente,\nSanepar`;
    } else {
        // MODELO 1: Prazo inicial (padrao 90 dias)
        resposta = `Prezado cliente,\n\nA respeito da matricula ${matricula}, informamos que foi concedido prazo inicial de ${diasConceder} dias para regularizacao, conforme solicitado.\n\nO prazo vencera em ${dataVencStr}.\n\nCaso necessite de prazo adicional, protocolize novo pedido proximo ao final deste prazo, informando que ja possui um prazo em vigor que esta proximo do vencimento e que necessita de prazo maior, com a devida justificativa.\n\nPara facilitar a nova apreciacao, se necessario, lembre-se de anexar ao novo pedido:\n- Orcamentos;\n- Comprovantes e documentos que reforcem e esclarecam a necessidade e as dificuldades tecnicas envolvidas;\n- Fotos do local;\n- Resumo detalhado da situacao.\n\nInformamos que a Sanepar concede inicialmente prazo de ate 90 dias para que o cliente se organize e resolva a situacao. Apos esse periodo, mediante apresentacao da documentacao completa, sera avaliada a possibilidade de concessao de prazo especial.\n\nAtenciosamente,\nSanepar`;
    }
    document.getElementById('respostaCasoEspecial').value = resposta;
    document.getElementById('respostaGeradaWrap').style.display = 'block';
}

'''

s = s[:inicio] + nova_func + s[fim:]

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(s)

print('Funcao JS corrigida com template literals.')
