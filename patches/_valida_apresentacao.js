// Validacao estatica da apresentacao de propostas (uso temporario)
const s = require('fs').readFileSync('propostas/2026-10-07/apresentacao.html', 'utf8');
let ok = 0, err = 0;
[...s.matchAll(/<script>([\s\S]*?)<\/script>/g)].forEach((x, i) => {
  try { new Function(x[1]); ok++; } catch (e) { err++; console.log('ERRO no script', i, ':', e.message); }
});
console.log('scripts ok:', ok, '| com erro:', err);
console.log('tem download?', /\.download\s*=|createObjectURL/.test(s));
console.log('tem alert/confirm/prompt?', /[^a-zA-Z](alert|confirm|prompt)\s*\(/.test(s));
console.log('tem recurso externo?', /src\s*=\s*["']https?:|href\s*=\s*["']https?:|@import|url\(https?/.test(s));
const ids = [...s.matchAll(/id="([^"]+)"/g)].map(m => m[1]);
const dup = [...new Set(ids.filter((v, i) => ids.indexOf(v) !== i))];
console.log('ids duplicados:', dup.length ? dup.join(',') : 'nenhum');
console.log('tamanho bytes:', s.length);
