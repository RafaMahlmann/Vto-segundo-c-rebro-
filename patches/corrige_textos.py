with open('index.html', 'r', encoding='utf-8') as f:
    s = f.read()

# === CORRECAO 1: Frase final do Modelo 1 ===
# De: "Informamos que a Sanepar concede inicialmente..." 
# Para: "Informamos que concedemos inicialmente prazo de ate 90 dias para que o cliente se organize e resolva a situacao."
# (tira a parte "Apos esse periodo...")

old_final_m1 = 'Informamos que a Sanepar concede inicialmente prazo de ate 90 dias para que o cliente se organize e resolva a situacao. Apos esse periodo, mediante apresentacao da documentacao sugerida, sera avaliada a possibilidade de concessao de prazo especial.'
new_final_m1 = 'Informamos que concedemos inicialmente prazo de ate 90 dias para que o cliente se organize e resolva a situacao.'

s = s.replace(old_final_m1, new_final_m1)

# === CORRECAO 2: Protocolo condicional em AMBOS os modelos ===

# Modelo 2 - com dados
old_m2_com = '''modelo2Texto = `Prezado cliente,

A respeito da matricula ${matricula}, informamos que sua solicitacao foi aceita e foi concedido prazo de ${diasConceder} dias para regularizacao, conforme protocolo ${protocolo}.

O prazo vencera em ${dataVencStr}.

Atenciosamente,
Sanepar`;'''

new_m2_com = '''const proto2 = (protocolo !== '________') ? (', conforme protocolo ' + protocolo + '.') : '.';
            modelo2Texto = `Prezado cliente,\n\nA respeito da matricula ${matricula}, informamos que sua solicitacao foi aceita e foi concedido prazo de ${diasConceder} dias para regularizacao` + proto2 + `\n\nO prazo vencera em ${dataVencStr}.\n\nAtenciosamente,\nSanepar`;'''

s = s.replace(old_m2_com, new_m2_com)

# Modelo 2 - vazio (placeholders)
old_m2_vazio = '''modelo2Texto = `Prezado cliente,

A respeito da matricula ${matricula}, informamos que sua solicitacao foi aceita e foi concedido prazo de ______ dias para regularizacao, conforme protocolo ${protocolo}.

O prazo vencera em ______.

Atenciosamente,
Sanepar`;'''

new_m2_vazio = '''const proto2e = (protocolo !== '________') ? (', conforme protocolo ' + protocolo + '.') : '.';
        modelo2Texto = `Prezado cliente,\n\nA respeito da matricula ${matricula}, informamos que sua solicitacao foi aceita e foi concedido prazo de ______ dias para regularizacao` + proto2e + `\n\nO prazo vencera em ______.\n\nAtenciosamente,\nSanepar`;'''

s = s.replace(old_m2_vazio, new_m2_vazio)

# Modelo 1 - com dados (substitui "conforme solicitado" por "conforme protocolo" quando ha protocolo)
old_m1_com = '''modelo1Texto = `Prezado cliente,

A respeito da matricula ${matricula}, informamos que foi concedido prazo inicial de ${diasConceder} dias para regularizacao, conforme solicitado.

O prazo vencera em ${dataVencStr}.

Caso necessite de prazo adicional, protocolize novo pedido proximo ao final deste prazo, informando que ja possui um prazo em vigor que esta proximo do vencimento e que necessita de prazo maior, com a devida justificativa.

Para facilitar a nova apreciacao, sugerimos anexar ao pedido comprovantes de orcamentos, fotos do local e um resumo da situacao.

Informamos que concedemos inicialmente prazo de ate 90 dias para que o cliente se organize e resolva a situacao.

Atenciosamente,
Sanepar`;'''

new_m1_com = '''const proto1 = (protocolo !== '________') ? (', conforme protocolo ' + protocolo + '.') : ', conforme solicitado.';
            modelo1Texto = `Prezado cliente,\n\nA respeito da matricula ${matricula}, informamos que foi concedido prazo inicial de ${diasConceder} dias para regularizacao` + proto1 + `\n\nO prazo vencera em ${dataVencStr}.\n\nCaso necessite de prazo adicional, protocolize novo pedido proximo ao final deste prazo, informando que ja possui um prazo em vigor que esta proximo do vencimento e que necessita de prazo maior, com a devida justificativa.\n\nPara facilitar a nova apreciacao, sugerimos anexar ao pedido comprovantes de orcamentos, fotos do local e um resumo da situacao.\n\nInformamos que concedemos inicialmente prazo de ate 90 dias para que o cliente se organize e resolva a situacao.\n\nAtenciosamente,\nSanepar`;'''

s = s.replace(old_m1_com, new_m1_com)

# Modelo 1 - vazio (placeholders)
old_m1_vazio = '''modelo1Texto = `Prezado cliente,

A respeito da matricula ${matricula}, informamos que foi concedido prazo inicial de ______ dias para regularizacao, conforme solicitado.

O prazo vencera em ______.

Caso necessite de prazo adicional, protocolize novo pedido proximo ao final deste prazo, informando que ja possui um prazo em vigor que esta proximo do vencimento e que necessita de prazo maior, com a devida justificativa.

Para facilitar a nova apreciacao, sugerimos anexar ao pedido comprovantes de orcamentos, fotos do local e um resumo da situacao.

Informamos que concedemos inicialmente prazo de ate 90 dias para que o cliente se organize e resolva a situacao.

Atenciosamente,
Sanepar`;'''

new_m1_vazio = '''const proto1e = (protocolo !== '________') ? (', conforme protocolo ' + protocolo + '.') : ', conforme solicitado.';
        modelo1Texto = `Prezado cliente,\n\nA respeito da matricula ${matricula}, informamos que foi concedido prazo inicial de ______ dias para regularizacao` + proto1e + `\n\nO prazo vencera em ______.\n\nCaso necessite de prazo adicional, protocolize novo pedido proximo ao final deste prazo, informando que ja possui um prazo em vigor que esta proximo do vencimento e que necessita de prazo maior, com a devida justificativa.\n\nPara facilitar a nova apreciacao, sugerimos anexar ao pedido comprovantes de orcamentos, fotos do local e um resumo da situacao.\n\nInformamos que concedemos inicialmente prazo de ate 90 dias para que o cliente se organize e resolva a situacao.\n\nAtenciosamente,\nSanepar`;'''

s = s.replace(old_m1_vazio, new_m1_vazio)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(s)

print('Correcoes aplicadas: frase final do Modelo 1 e protocolo condicional em ambos os modelos.')
