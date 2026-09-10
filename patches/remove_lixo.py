with open('index.html', 'r', encoding='utf-8') as f:
    s = f.read()

# Remove o bloco de lixo que ficou entre o primeiro "Atenciosamente," e o final
old_lixo = '''Atenciosamente,
\t- Orcamentos;
\t- Comprovantes e documentos que reforcem e esclarecam a necessidade e as dificuldades tecnicas envolvidas;
\t- Fotos do local;
\t- Resumo detalhado da situacao.

Informamos que a Sanepar concede inicialmente prazo de ate 90 dias para que o cliente se organize e resolva a situacao. Apos esse periodo, mediante apresentacao da documentacao completa, sera avaliada a possibilidade de concessao de prazo especial.

Atenciosamente,
Sanepar`;'''

new_lixo = '''Atenciosamente,
Sanepar`;'''

if old_lixo in s:
    s = s.replace(old_lixo, new_lixo)
    print('Lixo removido com sucesso.')
else:
    print('Bloco de lixo nao encontrado exatamente. Tentando com tabs...')
    # Vamos tentar encontrar de outra forma
    import re
    pattern = r'(Atenciosamente,\n)\t- Orcamentos;\n\t- Comprovantes.*?Sanepar`;'
    replacement = r'\1Sanepar`;'
    result = re.sub(pattern, replacement, s, flags=re.DOTALL)
    if result != s:
        s = result
        print('Lixo removido via regex.')
    else:
        print('Regex tambem nao encontrou.')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(s)
