with open('index.html', 'r', encoding='utf-8') as f:
    s = f.read()

old_lixo = '''Atenciosamente,
- Orcamentos;
- Comprovantes e documentos que reforcem e esclarecam a necessidade e as dificuldades tecnicas envolvidas;
- Fotos do local;
- Resumo detalhado da situacao.

Informamos que a Sanepar concede inicialmente prazo de ate 90 dias para que o cliente se organize e resolva a situacao. Apos esse periodo, mediante apresentacao da documentacao completa, sera avaliada a possibilidade de concessao de prazo especial.

Atenciosamente,
Sanepar`;'''

new_lixo = '''Atenciosamente,
Sanepar`;'''

if old_lixo in s:
    s = s.replace(old_lixo, new_lixo)
    print('Lixo removido com sucesso.')
else:
    print('Nao encontrou.')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(s)
