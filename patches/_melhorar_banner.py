#!/usr/bin/env python3
"""Melhora o banner de nova versao com botao de download."""
import re

path = r'C:\Users\xrafa\Programas\vto-repo\index.html'
with open(path, encoding='utf-8') as f:
    t = f.read()

# 1. Adicionar CSS para o botao de download (antes do comentario ESTATISTICAS)
css_antigo = '#bannerVersao .banner-fechar:hover{color:#533f03}\n\n/* ===== ESTATISTICAS ===== */'
css_novo = '''#bannerVersao .banner-fechar:hover{color:#533f03}
#bannerVersao .banner-baixar{background:#28a745;color:white;border:none;border-radius:6px;padding:6px 14px;font-size:.8rem;font-weight:700;cursor:pointer;margin-right:8px;transition:background .2s;font-family:inherit}
#bannerVersao .banner-baixar:hover{background:#218838}

/* ===== ESTATISTICAS ===== */'''

t = t.replace(css_antigo, css_novo)
print('CSS do banner atualizado.')

# 2. Modificar HTML do banner
html_antigo = '''<div id="bannerVersao">
    <span class="banner-texto" id="bannerVersaoTexto"></span>
    <button class="banner-fechar" onclick="fecharBannerVersao()" title="Fechar aviso">&times;</button>
</div>'''

html_novo = '''<div id="bannerVersao">
    <span class="banner-texto" id="bannerVersaoTexto"></span>
    <button class="banner-baixar" onclick="baixarNovaVersao()" id="bannerBtnBaixar" style="display:none">Baixar vNova</button>
    <button class="banner-fechar" onclick="fecharBannerVersao()" title="Fechar aviso">&times;</button>
</div>'''

t = t.replace(html_antigo, html_novo)
print('HTML do banner atualizado.')

# 3. Modificar o JS do verificador
js_antigo = '''const URL_VERSAO = 'https://raw.githubusercontent.com/RafaMahlmann/Vto-segundo-c-rebro-/main/version.json';

(function verificarNovaVersao() {
    const banner = document.getElementById('bannerVersao');
    if (!banner) return;
    
    fetch(URL_VERSAO + '?t=' + Date.now(), { cache: 'no-store' })
        .then(r => r.json())
        .then(d => {
            if (d.versao && d.versao !== VERSAO_LOCAL) {
                document.getElementById('bannerVersaoTexto').textContent = 
                    'Nova versao disponivel: v' + d.versao + '  —  Atualize a pagina (F5 ou Ctrl+F5)';
                banner.classList.add('ativo');
            }
        })
        .catch(() => { /* offline — sem banner */ });
})();

function fecharBannerVersao() {
    document.getElementById('bannerVersao').classList.remove('ativo');
}'''

js_novo = '''const URL_VERSAO = 'https://raw.githubusercontent.com/RafaMahlmann/Vto-segundo-c-rebro-/main/version.json';
const URL_INDEX_HTML = 'https://raw.githubusercontent.com/RafaMahlmann/Vto-segundo-c-rebro-/main/index.html';
let VERSAO_REMOTA = null;

(function verificarNovaVersao() {
    const banner = document.getElementById('bannerVersao');
    if (!banner) return;
    
    fetch(URL_VERSAO + '?t=' + Date.now(), { cache: 'no-store' })
        .then(r => r.json())
        .then(d => {
            if (d.versao && d.versao !== VERSAO_LOCAL) {
                VERSAO_REMOTA = d.versao;
                document.getElementById('bannerVersaoTexto').textContent = 
                    'Nova versao v' + d.versao + ' disponivel! Baixe e substitua seu arquivo.';
                const btn = document.getElementById('bannerBtnBaixar');
                if (btn) { btn.textContent = 'Baixar v' + d.versao; btn.style.display = 'inline-block'; }
                banner.classList.add('ativo');
            }
        })
        .catch(() => { /* offline — sem banner */ });
})();

function fecharBannerVersao() {
    document.getElementById('bannerVersao').classList.remove('ativo');
}

function baixarNovaVersao() {
    if (!VERSAO_REMOTA) return;
    const btn = document.getElementById('bannerBtnBaixar');
    if (btn) btn.textContent = 'Baixando...';
    fetch(URL_INDEX_HTML + '?t=' + Date.now(), { cache: 'no-store' })
        .then(r => r.text())
        .then(html => {
            const blob = new Blob([html], { type: 'text/html' });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'vto-segundo-cerebro-v' + VERSAO_REMOTA + '.html';
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            URL.revokeObjectURL(url);
            fecharBannerVersao();
        })
        .catch(() => {
            if (btn) btn.textContent = 'Erro :(';
            setTimeout(() => { if (btn) btn.textContent = 'Baixar v' + VERSAO_REMOTA; }, 2000);
        });
}'''

t = t.replace(js_antigo, js_novo)
print('JS do verificador atualizado.')

with open(path, 'w', encoding='utf-8') as f:
    f.write(t)

print('Tudo salvo no index.html!')
