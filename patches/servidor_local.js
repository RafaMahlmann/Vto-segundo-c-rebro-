// Servidor local estatico para o app VTO (uso local, sem dependencias).
// Uso: node patches/servidor_local.js [porta]   (padrao 7100)
const http = require('http');
const fs = require('fs');
const path = require('path');

const RAIZ = path.resolve(__dirname, '..');

// Aceita porta em qualquer formato: --port 7100 | --port=7100 | -p 7100 | 7100 | env PORT
function descobrirPorta() {
  const args = process.argv.slice(2);
  for (let i = 0; i < args.length; i++) {
    const a = args[i];
    if (a === '--port' || a === '-p') { const n = Number(args[i + 1]); if (n > 0) return n; }
    const m = a.match(/^(?:--port=|-p)(\d+)$/); if (m) return Number(m[1]);
    if (/^\d+$/.test(a)) return Number(a);
  }
  const env = Number(process.env.PORT); if (env > 0) return env;
  return 7100;
}
const PORTA = descobrirPorta();

const MIME = {
  '.html': 'text/html; charset=utf-8',
  '.js': 'text/javascript; charset=utf-8',
  '.css': 'text/css; charset=utf-8',
  '.json': 'application/json; charset=utf-8',
  '.webmanifest': 'application/manifest+json',
  '.png': 'image/png',
  '.jpg': 'image/jpeg',
  '.svg': 'image/svg+xml',
  '.ico': 'image/x-icon',
  '.md': 'text/plain; charset=utf-8'
};

http.createServer((req, res) => {
  try {
    let caminho = decodeURIComponent((req.url || '/').split('?')[0]);
    if (caminho === '/') caminho = '/index.html';
    const arquivo = path.normalize(path.join(RAIZ, caminho));
    if (!arquivo.startsWith(RAIZ)) { res.writeHead(403); res.end('proibido'); return; }
    if (!fs.existsSync(arquivo) || !fs.statSync(arquivo).isFile()) { res.writeHead(404); res.end('nao achado'); return; }
    res.writeHead(200, { 'Content-Type': MIME[path.extname(arquivo).toLowerCase()] || 'application/octet-stream', 'Cache-Control': 'no-store' });
    fs.createReadStream(arquivo).pipe(res);
  } catch (e) {
    res.writeHead(500); res.end('erro');
  }
}).listen(PORTA, () => console.log('VTO no ar: http://localhost:' + PORTA + '/'));
