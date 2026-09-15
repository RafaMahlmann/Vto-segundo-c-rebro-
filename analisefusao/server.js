// Servidor estatico minimo para o preview do checklist.
// Sem dependencias. Aceita --host/--port (ou -H/-p) e a env PORT.
const http = require('http');
const fs = require('fs');
const path = require('path');

const args = process.argv.slice(2);
function arg(nomes, padrao) {
  for (let i = 0; i < args.length; i++) {
    if (nomes.includes(args[i]) && args[i + 1]) return args[i + 1];
    const comValor = args[i].split('=');
    if (nomes.includes(comValor[0]) && comValor[1]) return comValor[1];
  }
  return padrao;
}
const host = arg(['--host', '-H'], '127.0.0.1');
const port = parseInt(arg(['--port', '-p'], process.env.PORT || '7100'), 10);
const raiz = __dirname;

const MIME = {
  '.html': 'text/html; charset=utf-8',
  '.css': 'text/css; charset=utf-8',
  '.js': 'text/javascript; charset=utf-8',
  '.png': 'image/png',
  '.jpg': 'image/jpeg',
  '.svg': 'image/svg+xml',
  '.json': 'application/json; charset=utf-8',
  '.ico': 'image/x-icon'
};

http.createServer((req, res) => {
  let caminho = decodeURIComponent(req.url.split('?')[0]);
  if (caminho === '/' || caminho === '') caminho = '/checklist-fusao.html';
  const alvo = path.normalize(path.join(raiz, caminho));
  if (!alvo.startsWith(raiz)) { res.writeHead(403); res.end('forbidden'); return; }
  fs.readFile(alvo, (err, dados) => {
    if (err) { res.writeHead(404); res.end('nao encontrado: ' + caminho); return; }
    res.writeHead(200, { 'Content-Type': MIME[path.extname(alvo).toLowerCase()] || 'application/octet-stream' });
    res.end(dados);
  });
}).listen(port, host, () => {
  console.log('checklist-fusao em http://' + host + ':' + port + '/');
});
