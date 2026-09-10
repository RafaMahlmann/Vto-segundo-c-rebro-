const fs = require('fs');
const html = fs.readFileSync('index.html', 'utf8');

// Extrai o conteudo do script
const match = html.match(/<script>([\s\S]*?)<\/script>/);
if (!match) {
    console.error('Nenhum script encontrado');
    process.exit(1);
}

const js = match[1];

// Tenta parsear
new Function(js);
console.log('Sintaxe JS OK — zero erros de parse.');
