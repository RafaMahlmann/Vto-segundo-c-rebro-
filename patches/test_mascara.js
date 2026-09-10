function aplicarMascaraData(valorAtual) {
    var val = valorAtual.replace(/\D/g, '');
    if (val.length > 8) val = val.slice(0, 8);
    var formatado = '';
    if (val.length >= 5) {
        formatado = val.slice(0, 2) + '/' + val.slice(2, 4) + '/' + val.slice(4);
    } else if (val.length >= 3) {
        formatado = val.slice(0, 2) + '/' + val.slice(2);
    } else {
        formatado = val;
    }
    return formatado;
}

function testar(input, esperado, desc) {
    var resultado = aplicarMascaraData(input);
    var ok = resultado === esperado;
    console.log((ok ? 'OK' : 'FALHA') + ' | ' + desc + ' | "' + input + '" -> "' + resultado + '"' + (ok ? '' : ' (esperado: "' + esperado + '")'));
    return ok;
}

var tudoOk = true;
tudoOk = testar('13032026', '13/03/2026', 'digita 13032026 completo') && tudoOk;
tudoOk = testar('2026', '20/26', 'digita 2026 (so ano parcial)') && tudoOk;
tudoOk = testar('130320', '13/03/20', 'digita 130320 (6 digitos -> mantem 20)') && tudoOk;
tudoOk = testar('13', '13', 'digita so dia') && tudoOk;
tudoOk = testar('1303', '13/03', 'digita dia+mes') && tudoOk;
tudoOk = testar('13/03/2026', '13/03/2026', 'ja formatado nao muda') && tudoOk;
tudoOk = testar('13032020', '13/03/2020', 'ano 2020 ja completo') && tudoOk;
tudoOk = testar('', '', 'vazio fica vazio') && tudoOk;

console.log('\n' + (tudoOk ? 'TODOS OS TESTES PASSARAM' : 'ALGUM TESTE FALHOU'));
process.exit(tudoOk ? 0 : 1);
