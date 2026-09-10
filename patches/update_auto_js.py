with open('index.html', 'r', encoding='utf-8') as f:
    s = f.read()

# Localiza e substitui a funcao calcularDilacaoCasoEspecial
import re

pattern = r"(function calcularDilacaoCasoEspecial\(\) \{)[\s\S]*?(\n\}\n\nfunction copiarRespostaCasoEspecial)"

new_func = r'''\1
    const dataPedidoTxt = document.getElementById('dataPedidoOriginal').value;
    const dataPedido = textoParaISODate(dataPedidoTxt);
    const diasTotais = parseInt(document.getElementById('diasTotaisSolicitados').value);
    const diasConceder = parseInt(document.getElementById('diasConcederAgora').value);
    const matricula = document.getElementById('matriculaCasoEspecial').value.trim() || '________';
    const protocolo = document.getElementById('protocoloCasoEspecial').value.trim() || '________';

    var decorridos = '—';
    var restantes = '—';
    var faltarao = '—';
    var dataVencStr = '________';
    var dataFinalStr = '________';
    var resposta = '';

    if (dataPedido && !isNaN(diasTotais) && diasTotais >= 1 && !isNaN(diasConceder) && diasConceder >= 1) {
        const hoje = new Date();
        const hojeIso = hoje.getFullYear() + '-' + String(hoje.getMonth()+1).padStart(2,'0') + '-' + String(hoje.getDate()).padStart(2,'0');
        const decorridosNum = calcularDiferencaDias(dataPedido, hojeIso);
        if (decorridosNum >= 0) {
            decorridos = decorridosNum;
            restantes = Math.max(0, diasTotais - decorridosNum);
            faltarao = Math.max(0, restantes - diasConceder);
            const dataVencimento = new Date(hoje);
            dataVencimento.setDate(dataVencimento.getDate() + diasConceder);
            const dataFinalPedido = new Date(dataPedido + 'T12:00:00');
            dataFinalPedido.setDate(dataFinalPedido.getDate() + diasTotais);
            dataVencStr = dataVencimento.toLocaleDateString('pt-BR',{weekday:'long',year:'numeric',month:'long',day:'numeric'});
            dataFinalStr = dataFinalPedido.toLocaleDateString('pt-BR',{weekday:'long',year:'numeric',month:'long',day:'numeric'});

            if (diasConceder >= diasTotais) {
                resposta = `Prezado cliente,\n\nA respeito da matricula ${matricula}, informamos que sua solicitacao foi aceita e foi concedido prazo de ${diasConceder} dias para regularizacao, conforme protocolo ${protocolo}.\n\nO prazo vencera em ${dataVencStr}.\n\nAtenciosamente,\nSanepar`;
            } else {
                resposta = `Prezado cliente,\n\nA respeito da matricula ${matricula}, informamos que foi concedido prazo inicial de ${diasConceder} dias para regularizacao, conforme solicitado.\n\nO prazo vencera em ${dataVencStr}.\n\nCaso necessite de prazo adicional, protocolize novo pedido proximo ao final deste prazo, informando que ja possui um prazo em vigor que esta proximo do vencimento e que necessita de prazo maior, com a devida justificativa.\n\nPara facilitar a nova apreciacao, sugerimos anexar ao pedido comprovantes de orcamentos, fotos do local e um resumo da situacao.\n\nInformamos que a Sanepar concede inicialmente prazo de ate 90 dias para que o cliente se organize e resolva a situacao. Apos esse periodo, mediante apresentacao da documentacao sugerida, sera avaliada a possibilidade de concessao de prazo especial.\n\nAtenciosamente,\nSanepar`;
            }
        }
    }

    if (!resposta) {
        // Texto modelo padrao quando campos estao vazios
        resposta = `Prezado cliente,\n\nA respeito da matricula ${matricula}, informamos que foi concedido prazo inicial de ______ dias para regularizacao, conforme solicitado.\n\nO prazo vencera em ______.\n\nCaso necessite de prazo adicional, protocolize novo pedido proximo ao final deste prazo, informando que ja possui um prazo em vigor que esta proximo do vencimento e que necessita de prazo maior, com a devida justificativa.\n\nPara facilitar a nova apreciacao, sugerimos anexar ao pedido comprovantes de orcamentos, fotos do local e um resumo da situacao.\n\nInformamos que a Sanepar concede inicialmente prazo de ate 90 dias para que o cliente se organize e resolva a situacao. Apos esse periodo, mediante apresentacao da documentacao sugerida, sera avaliada a possibilidade de concessao de prazo especial.\n\nAtenciosamente,\nSanepar`;
    }

    document.getElementById('ceDecorridos').textContent = decorridos + (typeof decorridos === 'number' ? ' dia(s)' : '');
    document.getElementById('ceRestantes').textContent = restantes + (typeof restantes === 'number' ? ' dia(s)' : '');
    document.getElementById('ceConcedidos').textContent = (isNaN(diasConceder) ? '—' : diasConceder + ' dia(s)');
    document.getElementById('ceFaltarao').textContent = faltarao + (typeof faltarao === 'number' ? ' dia(s)' : '');
    document.getElementById('ceVencimento').textContent = dataVencStr;
    document.getElementById('prazoFinalPedido').textContent = dataFinalStr;
    document.getElementById('respostaCasoEspecial').value = resposta;
\2'''

result = re.sub(pattern, new_func, s)

if result != s:
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(result)
    print('Funcao JS atualizada com auto-preenchimento.')
else:
    print('Regex nao encontrou a funcao.')
