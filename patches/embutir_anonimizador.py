# -*- coding: utf-8 -*-
"""
Embute o conteudo de anonimizador.html dentro do index.html em Base64,
para que o botao "Exportar ZIP" funcione mesmo quando o app e aberto
via file:// (duplo clique), onde XHR/fetch para arquivos locais sao bloqueados.

Estrategia:
1. Le anonimizador.html e converte para Base64.
2. Insere um bloco <script id="anonimizadorFonte" type="application/octet-stream">
   contendo o Base64, logo antes do </body> do index.html.
3. Substitui a funcao gerarZipCompleto() para ler esse Base64 em vez de usar XHR.
"""
import base64
import io
import re
import sys

REPO = r"C:\Users\xrafa\Programas\vto-repo"
INDEX = REPO + r"\index.html"
ANON = REPO + r"\anonimizador.html"

with io.open(ANON, "r", encoding="utf-8") as f:
    anon_html = f.read()

with io.open(INDEX, "r", encoding="utf-8") as f:
    index_html = f.read()

# 1) Base64 do anonimizador
anon_b64 = base64.b64encode(anon_html.encode("utf-8")).decode("ascii")

# 2) Remove bloco antigo, se existir (idempotente)
index_html = re.sub(
    r'\n<!-- ANONIMIZADOR EMBUTIDO \(Base64\) -->.*?<!-- /ANONIMIZADOR EMBUTIDO -->\n',
    '\n', index_html, flags=re.DOTALL)

# 3) Insere o bloco Base64 antes de </body>
bloco = (
    '\n<!-- ANONIMIZADOR EMBUTIDO (Base64) -->\n'
    '<script id="anonimizadorFonte" type="application/octet-stream">'
    + anon_b64 +
    '</script>\n'
    '<!-- /ANONIMIZADOR EMBUTIDO -->\n'
)
index_html = index_html.replace('</body>', bloco + '</body>', 1)

# 4) Substitui a funcao gerarZipCompleto
nova_funcao = '''// ===== GERAR ZIP PORTATIL =====
function gerarZipCompleto() {
    const btn = document.querySelector('.btn-zip');
    const original = btn ? btn.textContent : 'Exportar ZIP';
    if (btn) btn.textContent = '...';

    // Coleta HTML do VTO (DOM atual)
    let htmlVto = '<!DOCTYPE html>\\n' + document.documentElement.outerHTML;

    // Coleta HTML do Anonimizador a partir do bloco Base64 embutido
    // (funciona em file://, onde XHR/fetch para arquivos locais sao bloqueados)
    let htmlAnon = '';
    try {
        const fonte = document.getElementById('anonimizadorFonte');
        if (fonte && fonte.textContent) {
            const b64 = fonte.textContent.trim();
            const bin = atob(b64);
            const bytes = new Uint8Array(bin.length);
            for (let i = 0; i < bin.length; i++) bytes[i] = bin.charCodeAt(i);
            htmlAnon = new TextDecoder('utf-8').decode(bytes);
        }
    } catch (e) {
        htmlAnon = '';
    }

    // Fallback: tenta XHR (funciona quando servido via http)
    if (!htmlAnon) {
        try {
            const xhr = new XMLHttpRequest();
            xhr.open('GET', 'anonimizador.html', false);
            xhr.send();
            if (xhr.status === 0 || xhr.status === 200) htmlAnon = xhr.responseText;
        } catch (e) { /* ignora */ }
    }

    if (!htmlAnon) {
        alert('Nao foi possivel carregar o anonimizador. O arquivo pode estar corrompido.');
        if (btn) btn.textContent = original;
        return;
    }

    // Gera ZIP com os dois arquivos
    const zip = criarZipMulti({
        'index.html': htmlVto,
        'anonimizador.html': htmlAnon
    });

    // Dispara download
    const blob = new Blob([zip], { type: 'application/zip' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'vto-completo.zip';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);

    if (btn) btn.textContent = original;
}
'''

# Localiza a funcao antiga (de "// ===== GERAR ZIP PORTATIL =====" ate o fechamento antes de criarZipMulti)
padrao = re.compile(
    r'// ===== GERAR ZIP PORTATIL =====\s*function gerarZipCompleto\(\)\s*\{.*?\n\}\n',
    re.DOTALL)
if not padrao.search(index_html):
    print("ERRO: nao encontrei a funcao gerarZipCompleto para substituir.")
    sys.exit(1)

index_html = padrao.sub(nova_funcao, index_html, count=1)

with io.open(INDEX, "w", encoding="utf-8", newline="") as f:
    f.write(index_html)

print("OK: anonimizador embutido em Base64 (%d bytes) e gerarZipCompleto atualizada." % len(anon_b64))
