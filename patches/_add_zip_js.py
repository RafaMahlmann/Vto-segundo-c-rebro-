path = r'C:/Users/xrafa/Programas/vto-repo/index.html'
with open(path, encoding='utf-8') as f:
    t = f.read()

# Código JS para inserir antes de "// Inicializa"
js_code = '''
// ===== GERAR ZIP PORTATIL =====
function gerarZipPortatil() {
    const btn = document.querySelector('.btn-zip');
    const original = btn.textContent;
    btn.textContent = '...';

    // Tenta obter HTML original via fetch (se em servidor)
    // Fallback: serializa o DOM atual
    let html;
    try {
        const xhr = new XMLHttpRequest();
        xhr.open('GET', window.location.href, false);
        xhr.send();
        if (xhr.status === 0 || xhr.status === 200) {
            html = xhr.responseText;
        }
    } catch (e) {
        html = null;
    }
    if (!html) {
        html = '<!DOCTYPE html>\\n' + document.documentElement.outerHTML;
    }

    // Gera ZIP stored
    const zip = criarZipStored('index.html', html);

    // Dispara download
    const blob = new Blob([zip], { type: 'application/zip' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'vto-segundo-cerebro.zip';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);

    btn.textContent = original;
}

function criarZipStored(nome, conteudo) {
    const enc = new TextEncoder();
    const nomeBytes = enc.encode(nome);
    const dados = enc.encode(conteudo);
    const crc = calcularCrc32(conteudo);
    const t = dados.length;
    const n = nomeBytes.length;

    // helpers little-endian
    const u16 = v => [v & 0xFF, (v >> 8) & 0xFF];
    const u32 = v => [v & 0xFF, (v >> 8) & 0xFF, (v >> 16) & 0xFF, (v >> 24) & 0xFF];

    // Local file header (30 + n)
    const lf = new Uint8Array(30 + n);
    let p = 0;
    const w = (arr) => { lf.set(arr, p); p += arr.length; };
    w([0x50, 0x4B, 0x03, 0x04]);
    w(u16(10));   // version needed
    w(u16(0));    // flags
    w(u16(0));    // compression = stored
    w(u16(0));    // mod time
    w(u16(0));    // mod date
    w(u32(crc));
    w(u32(t));    // compressed size
    w(u32(t));    // uncompressed size
    w(u16(n));
    w(u16(0));    // extra field length
    lf.set(nomeBytes, p);

    // Central directory (46 + n)
    const cd = new Uint8Array(46 + n);
    p = 0;
    const x = (arr) => { cd.set(arr, p); p += arr.length; };
    x([0x50, 0x4B, 0x01, 0x02]);
    x(u16(10));   // version made by
    x(u16(10));   // version needed
    x(u16(0));    // flags
    x(u16(0));    // compression
    x(u16(0));    // mod time
    x(u16(0));    // mod date
    x(u32(crc));
    x(u32(t));
    x(u32(t));
    x(u16(n));
    x(u16(0));    // extra length
    x(u16(0));    // comment length
    x(u16(0));    // disk number
    x(u16(0));    // internal attr
    x(u32(0));    // external attr
    x(u32(0));    // local header offset
    cd.set(nomeBytes, p);

    // End of central directory (22)
    const eocd = new Uint8Array(22);
    p = 0;
    const y = (arr) => { eocd.set(arr, p); p += arr.length; };
    y([0x50, 0x4B, 0x05, 0x06]);
    y(u16(0));    // disk number
    y(u16(0));    // disk with CD
    y(u16(1));    // entries on disk
    y(u16(1));    // total entries
    y(u32(cd.length));
    y(u32(lf.length + t));
    y(u16(0));    // comment length

    // Monta ZIP final
    const out = new Uint8Array(lf.length + t + cd.length + eocd.length);
    let o = 0;
    out.set(lf, o); o += lf.length;
    out.set(dados, o); o += t;
    out.set(cd, o); o += cd.length;
    out.set(eocd, o);
    return out;
}

function calcularCrc32(str) {
    const tabela = new Uint32Array(256);
    for (let i = 0; i < 256; i++) {
        let c = i;
        for (let j = 0; j < 8; j++) {
            c = (c & 1) ? (0xEDB88320 ^ (c >>> 1)) : (c >>> 1);
        }
        tabela[i] = c;
    }
    let crc = 0 ^ (-1);
    for (let i = 0; i < str.length; i++) {
        crc = (crc >>> 8) ^ tabela[(crc ^ str.charCodeAt(i)) & 0xFF];
    }
    return (crc ^ (-1)) >>> 0;
}

'''

# Inserir antes de "// Inicializa"
marker = 'function fecharBannerVersao() {\n    document.getElementById(\'bannerVersao\').classList.remove(\'ativo\');\n}\n\n// Inicializa'
replacement = 'function fecharBannerVersao() {\n    document.getElementById(\'bannerVersao\').classList.remove(\'ativo\');\n}\n\n' + js_code + '// Inicializa'

if marker in t:
    t = t.replace(marker, replacement, 1)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(t)
    print('Codigo JS inserido com sucesso.')
else:
    print('Marcador nao encontrado.')
