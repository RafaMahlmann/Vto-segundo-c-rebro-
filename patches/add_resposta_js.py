with open('index.html', 'r', encoding='utf-8') as f:
    s = f.read()

# Atualiza a funcao calcularDilacaoCasoEspecial para gerar o texto
old_final = '''    document.getElementById('prazoFinalPedido').textContent = dataFinalPedido.toLocaleDateString('pt-BR',{weekday:'long',year:'numeric',month:'long',day:'numeric'});
    document.getElementById('notaRecomendacao').style.display = 'block';
    document.getElementById('resultadoCasoEspecial').style.display = 'block';
}

// ===== ABA 4: MATRICULAS ====='''

new_final = '''    document.getElementById('prazoFinalPedido').textContent = dataFinalPedido.toLocaleDateString('pt-BR',{weekday:'long',year:'numeric',month:'long',day:'numeric'});
    document.getElementById('notaRecomendacao').style.display = 'block';
    document.getElementById('resultadoCasoEspecial').style.display = 'block';

    // Gera resposta para o cliente
    const matricula = document.getElementById('matriculaCasoEspecial').value.trim() || '________';
    const dataVencStr = dataVencimento.toLocaleDateString('pt-BR',{weekday:'long',year:'numeric',month:'long',day:'numeric'});
    const resposta = 'Prezado cliente,' + '\\n\\n' +
        'A respeito da matricula ' + matricula + ', informamos que foi concedido prazo de ' + diasConceder + ' dias para regularizacao, conforme solicitado.' + '\\n\\n' +
        'O prazo vencera em ' + dataVencStr + '.' + '\\n\\n' +
        'Caso necessite de prazo adicional, solicitamos que protocolize novo pedido proximo ao final deste prazo, informando que ja possui um prazo em vigor que esta proximo do vencimento, e que necessita de prazo maior, com a devida justificativa.' + '\\n\\n' +
        'Para facilitar a apreciacao da equipe tecnica, lembre-se de anexar ao novo pedido:' + '\\n' +
        '- Orcamentos;' + '\\n' +
        '- Fotos do local (especialmente em caso de dificuldade tecnica);' + '\\n' +
        '- Resumo detalhado da situacao.' + '\\n\\n' +
        'Informamos que a Sanepar concede inicialmente prazo de ate 90 dias para que o cliente se organize e resolva a questao. Apos esse periodo, mediante apresentacao da documentacao completa, sera avaliada a possibilidade de concessao de prazo especial.' + '\\n\\n' +
        'Atenciosamente,' + '\\n' +
        'Sanepar';
    document.getElementById('respostaCasoEspecial').value = resposta;
    document.getElementById('respostaGeradaWrap').style.display = 'block';
}

function copiarRespostaCasoEspecial() {
    var ta = document.getElementById('respostaCasoEspecial');
    ta.select();
    ta.setSelectionRange(0, 999999);
    try {
        document.execCommand('copy');
        alert('Texto copiado para a area de transferencia.');
    } catch (err) {
        alert('Nao foi possivel copiar automaticamente. Selecione o texto e use Ctrl+C.');
    }
}

// ===== ABA 4: MATRICULAS ====='''

s = s.replace(old_final, new_final)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(s)

print('JS atualizado com geracao de resposta e funcao copiar.')
