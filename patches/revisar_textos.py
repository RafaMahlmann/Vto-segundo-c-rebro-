import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Dica azul
old_dica = '''        <div class="dica-box">
            <strong>Como usar:</strong><br>
            <strong>1. Dilação simples:</strong> escolha a data base, informe os dias de dilação (use os botões 30/60/90 ou digite um valor manual) e clique em calcular.<br>
            <strong>2. Caso especial (dilação parcial):</strong> use quando o cliente já pediu uma dilação há algum tempo e agora você vai conceder um prazo adicional. Preencha a <em>data do pedido original</em> e os <em>dias totais</em> que ele solicitou. A ferramenta calcula automaticamente quantos dias já se passaram, quantos faltam, e quanto você deve conceder agora (padrão: 90 dias). Ela também mostra a data de vencimento desses 90 dias e quanto ainda faltará pedir depois.
        </div>'''

new_dica = '''        <div class="dica-box">
            <strong>Como usar:</strong><br>
            <strong>Dilação simples</strong> — quando o cliente pede agora pela primeira vez. Escolha a data base e os dias (30, 60, 90 ou outro valor).<br><br>
            <strong>Caso especial</strong> — quando o cliente já tinha pedido dilação antes e você vai dar mais prazo agora. Coloque a data do pedido antigo e os dias totais que ele pediu. Aqui você vê quanto tempo já passou, quanto ainda falta, e quanto dar hoje (padrão: 90 dias). Também mostra quando vence esse prazo novo e quanto faltará pedir depois.
        </div>'''

content = content.replace(old_dica, new_dica)

# 2. Título seção caso especial
content = content.replace('Caso Especial — Data Base Extra', 'Caso especial — dilação parcial')

# 3. Subtítulo
content = content.replace(
    'Use quando o cliente já pediu dilação há algum tempo e você vai conceder prazo adicional agora.',
    'Use quando o cliente já tinha pedido dilação antes e você vai dar mais prazo agora.'
)

# 4. Rótulo dias totais
content = content.replace('Dias Totais Solicitados na Epoca', 'Dias totais do pedido antigo')

# 5. Rótulo dias a conceder
content = content.replace('Dias a Conceder Agora (padrao 1ª vez)', 'Dias para dar agora (padrão: 90)')

# 6. Botão
content = content.replace('Calcular Dilação Parcial', 'Calcular prazo parcial')

# 7. Label resultado
content = content.replace('Dias que ainda faltarão pedir:', 'Quanto ainda falta pedir:')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print('Revisão textual aplicada com sucesso!')
