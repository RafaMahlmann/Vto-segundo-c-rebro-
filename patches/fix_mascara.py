import re

with open('index.html', 'r', encoding='utf-8') as f:
    s = f.read()

old_block = """// ===== MASCARA DD/MM/AAAA =====
function aplicarMascaraData(input) {
    input.addEventListener('input', function(e) {
        let val = this.value.replace(/\\D/g, '');
        if (val.length > 8) val = val.slice(0, 8);
        if (val.length >= 5) {
            this.value = val.slice(0,2) + '/' + val.slice(2,4) + '/' + val.slice(4);
        } else if (val.length >= 3) {
            this.value = val.slice(0,2) + '/' + val.slice(2);
        } else {
            this.value = val;
        }
    });
}

// Aplica mascara em todos os campos de data
['dataSancao','dataFaturamento','dataSolicitacao','dataInicialDilacao'].forEach(function(id) {
    var el = document.getElementById(id);
    if (el) aplicarMascaraData(el);
});"""

new_block = """// ===== MASCARA DD/MM/AAAA =====
function aplicarMascaraData(input) {
    input.addEventListener('input', function(e) {
        // Guarda posicao do cursor
        var cursorPos = this.selectionStart || 0;
        var lenAntes = this.value.length;

        // Remove tudo que nao e digito
        var val = this.value.replace(/\\D/g, '');

        // Converte ano de 2 digitos para 4 ao completar 8 digitos
        if (val.length === 8) {
            var ano = parseInt(val.slice(4, 6), 10);
            // Cutoff: >= 50 => 1900+, < 50 => 2000+
            var anoCompleto = ano >= 50 ? (1900 + ano) : (2000 + ano);
            val = val.slice(0, 4) + String(anoCompleto);
        }
        if (val.length > 8) val = val.slice(0, 8);

        // Reaplica as barras
        var formatado = '';
        if (val.length >= 5) {
            formatado = val.slice(0, 2) + '/' + val.slice(2, 4) + '/' + val.slice(4);
        } else if (val.length >= 3) {
            formatado = val.slice(0, 2) + '/' + val.slice(2);
        } else {
            formatado = val;
        }

        this.value = formatado;

        // Ajusta cursor para nao pular para o fim ao digitar no meio
        var lenDepois = formatado.length;
        var diferenca = lenDepois - lenAntes;
        var novoCursor = Math.max(0, cursorPos + diferenca);
        // Se o cursor caiu em cima de uma barra, avanca 1
        if (formatado.charAt(novoCursor) === '/' && formatado.charAt(cursorPos - 1) !== '/') {
            novoCursor += 1;
        }
        this.setSelectionRange(novoCursor, novoCursor);
    });

    // Ao perder foco, completa ano se sobrar 2 digitos (ex: 13/03/26 -> 13/03/2026)
    input.addEventListener('blur', function() {
        var v = this.value;
        if (/^\\d{2}\/\\d{2}\/\\d{2}$/.test(v)) {
            var partes = v.split('/');
            var ano = parseInt(partes[2], 10);
            var anoCompleto = ano >= 50 ? (1900 + ano) : (2000 + ano);
            this.value = partes[0] + '/' + partes[1] + '/' + anoCompleto;
        }
    });
}

// Aplica mascara em todos os campos de data
['dataSancao','dataFaturamento','dataSolicitacao','dataInicialDilacao','dataPedidoOriginal'].forEach(function(id) {
    var el = document.getElementById(id);
    if (el) aplicarMascaraData(el);
});"""

s = s.replace(old_block, new_block)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(s)

print('Mascara de data atualizada com sucesso.')
