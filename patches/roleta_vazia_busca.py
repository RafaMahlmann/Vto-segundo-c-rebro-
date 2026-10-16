"""
Roleta do Fluxo: casa vazia + busca por codigo + efeito de giro.

Toca em 3 lugares do index.html, todos por ancora:
  1. CSS  - bloco novo depois de ".coluna-3 .roleta-dot.ativo"
  2. JS   - helpers antes de "let _roletaInstances" e setupRoletaGrupo() refeita
  3. JS   - prepararHtmlLimpo() (plano B) ganha a limpeza do que a busca cria

Para se qualquer ancora nao for encontrada exatamente uma vez.
Rodar da raiz do projeto:  python patches/roleta_vazia_busca.py
"""
import sys

with open('index.html', 'r', encoding='utf-8', newline='') as f:
    s = f.read()

if 'roleta-palco' in s:
    sys.exit('PARADO: o patch ja foi aplicado (achei roleta-palco).')

def crlf(t):
    return t.replace('\r\n', '\n').replace('\n', '\r\n')

def troca(s, velho, novo, rotulo):
    velho, novo = crlf(velho), crlf(novo)
    n = s.count(velho)
    if n != 1:
        sys.exit('PARADO: ancora "%s" achada %d vezes (esperado 1).' % (rotulo, n))
    return s.replace(velho, novo)

# ---------------------------------------------------------------- 1. CSS
ANCORA_CSS = ".coluna-3 .roleta-dot.ativo{background:#c2185b}\n"
CSS_NOVO = r'''
/* Roleta: casa vazia, busca por codigo e efeito de giro */
.coluna-1{--rl-cor:#1976d2;--rl-clara:#90caf9;--rl-txt:#1565c0;--rl-tinta:rgba(25,118,210,.35);--rl-anel:rgba(25,118,210,.45)}
.coluna-2{--rl-cor:#f57c00;--rl-clara:#ffcc80;--rl-txt:#e65100;--rl-tinta:rgba(245,124,0,.35);--rl-anel:rgba(245,124,0,.45)}
.coluna-3{--rl-cor:#c2185b;--rl-clara:#f48fb1;--rl-txt:#ad1457;--rl-tinta:rgba(194,24,88,.35);--rl-anel:rgba(194,24,88,.45)}
.roleta-dot.vazio{background:transparent;box-shadow:inset 0 0 0 1.5px rgba(0,0,0,.35)}
.roleta-dot.vazio.ativo{box-shadow:inset 0 0 0 1.5px var(--rl-cor)}
.roleta-mini{width:24px;height:24px;flex-shrink:0;border:none;border-radius:6px;background:rgba(255,255,255,.7);color:#495057;cursor:pointer;font-size:.72rem;display:flex;align-items:center;justify-content:center;transition:transform .15s,background .15s}
.roleta-mini:hover{background:white;transform:scale(1.1)}
.roleta-mini[hidden]{display:none}
.roleta-mini:focus-visible,.roleta-vazio:focus-visible{outline:2px solid var(--rl-cor);outline-offset:2px}
.roleta-palco{position:relative;border-radius:8px}
.roleta-palco.girando{overflow:hidden}
.roleta-palco .servico-btn{position:relative;overflow:hidden;min-height:62px}
.roleta-vazio{display:flex;align-items:center;justify-content:center;gap:8px;width:100%;min-height:62px;margin-bottom:6px;padding:10px 14px;border:2px dashed var(--rl-clara);border-radius:8px;background:rgba(255,255,255,.35);color:var(--rl-txt);font-size:.85rem;font-weight:600;font-family:inherit;cursor:pointer;transition:background .2s,border-color .2s,transform .12s}
.roleta-vazio .dica{font-weight:400;font-size:.78rem;opacity:.75}
.roleta-vazio:hover{background:rgba(255,255,255,.75);border-style:solid;border-color:var(--rl-cor)}
.roleta-vazio:active{transform:scale(.97)}
.roleta-palco .roleta-fantasma{position:absolute;left:0;top:0;width:100%;pointer-events:none}
.rl-entra-baixo{animation:rlEntraBaixo .34s cubic-bezier(.2,.9,.3,1.2)}
.rl-entra-cima{animation:rlEntraCima .34s cubic-bezier(.2,.9,.3,1.2)}
.rl-sai-cima{animation:rlSaiCima .22s ease-in both}
.rl-sai-baixo{animation:rlSaiBaixo .22s ease-in both}
.rl-encaixe{animation:rlEncaixe .42s cubic-bezier(.3,1.5,.5,1)}
.rl-varre::after{content:"";position:absolute;top:0;right:0;bottom:0;left:0;background:linear-gradient(90deg,transparent,var(--rl-tinta),transparent);transform:translateX(-100%);animation:rlVarre .5s ease-out;pointer-events:none}
.rl-anel{animation:rlAnel .5s ease-out}
.rl-treme{animation:rlTreme .32s ease-in-out}
@keyframes rlEntraBaixo{from{transform:translateY(85%);opacity:0}}
@keyframes rlEntraCima{from{transform:translateY(-85%);opacity:0}}
@keyframes rlSaiCima{to{transform:translateY(-85%);opacity:0}}
@keyframes rlSaiBaixo{to{transform:translateY(85%);opacity:0}}
@keyframes rlEncaixe{from{transform:scale(.88)}}
@keyframes rlVarre{to{transform:translateX(100%)}}
@keyframes rlAnel{from{box-shadow:0 0 0 0 var(--rl-anel)}to{box-shadow:0 0 0 14px transparent}}
@keyframes rlTreme{0%,100%{transform:translateX(0)}20%{transform:translateX(-6px)}40%{transform:translateX(5px)}60%{transform:translateX(-3px)}80%{transform:translateX(2px)}}
@keyframes rlAbre{from{opacity:0;transform:translateY(-4px)}}
@keyframes rlLinha{from{opacity:0;transform:translateX(-6px)}}
.roleta-busca{display:none;margin-bottom:6px;padding:6px;background:rgba(255,255,255,.9);border:2px solid var(--rl-cor);border-radius:8px}
.roleta-buscando .roleta-palco{display:none}
.roleta-buscando .roleta-busca{display:block;animation:rlAbre .2s ease-out}
.roleta-busca input{width:100%;padding:9px 10px;font-family:'Courier New',monospace;font-size:1.1rem;font-weight:700;letter-spacing:2px;color:#343a40;background:white;border:2px solid var(--rl-clara);border-radius:6px;outline:none}
.roleta-busca input:focus{border-color:var(--rl-cor);box-shadow:0 0 0 3px var(--rl-tinta)}
.roleta-busca ul{list-style:none;margin-top:6px}
.roleta-busca li{display:flex;gap:10px;align-items:baseline;padding:7px 8px;border-radius:6px;cursor:pointer;font-size:.85rem;color:#495057;animation:rlLinha .18s ease-out backwards}
.roleta-busca li b{min-width:44px;font-family:'Courier New',monospace;font-size:.95rem;color:var(--rl-txt)}
.roleta-busca li .d{margin-left:auto;font-size:.75rem;opacity:.75}
.roleta-busca li.sel{background:var(--rl-cor);color:white}
.roleta-busca li.sel b{color:white}
.roleta-busca mark{background:none;color:inherit;font-weight:900;text-decoration:underline;text-underline-offset:3px}
.roleta-busca .msg{padding:6px 8px;font-size:.8rem;font-weight:600;color:#b71c1c}
.roleta-busca .rodape{margin-top:4px;padding:6px 8px 2px;font-size:.72rem;color:#6c757d;border-top:1px dashed rgba(0,0,0,.12)}
@media (prefers-reduced-motion:reduce){.rl-entra-baixo,.rl-entra-cima,.rl-encaixe,.rl-anel,.rl-treme,.rl-varre::after,.roleta-busca li,.roleta-buscando .roleta-busca{animation:none}}
'''
s = troca(s, ANCORA_CSS, ANCORA_CSS + CSS_NOVO, 'css roleta')

# ---------------------------------------------------------------- 2. JS helpers
ANCORA_INST = "let _roletaInstances = [];\n"
HELPERS = r'''let _roletaInstances = [];
let _roletaArmada = null;
// Efeito visual (giro, encaixe) desliga sozinho se o Windows pediu menos movimento.
function _rolEfeito() { return !(window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches); }
function _rolNorm(s) { return String(s).toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, ''); }
function _rolReflow(el, cls) { el.classList.remove(cls); void el.offsetWidth; el.classList.add(cls); }
function _rolEsc(s) { return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;'); }
// Onde um codigo mora (vistoria + grupo), lido do proprio HTML: nada escrito a mao.
function _rolOnde(cod) {
    const achou = [];
    document.querySelectorAll('.roleta-grupo').forEach(g => {
        if (!g.querySelector('.servico-btn[data-cod="' + cod + '"]')) return;
        const col = g.closest('.coluna-vistoria');
        const titulo = g.querySelector('.servicos-grupo-title');
        achou.push((col ? col.id.replace('coluna', '') + 'a Vistoria' : '') + ' - ' + (titulo ? titulo.textContent : ''));
    });
    return achou;
}
'''
s = troca(s, ANCORA_INST, HELPERS, 'let _roletaInstances')

# ---------------------------------------------------------------- 3. setupRoletaGrupo
ini = s.find(crlf("function setupRoletaGrupo(grupoEl) {\n"))
fim_marca = crlf("// ===== CONTROLE DE VISUALIZACAO DO FLUXO =====\n")
fim = s.find(fim_marca)
if ini < 0 or fim < 0 or s.count(crlf("function setupRoletaGrupo(grupoEl) {\n")) != 1 or fim < ini:
    sys.exit('PARADO: nao achei o inicio/fim de setupRoletaGrupo().')

NOVA_FUNCAO = r'''function setupRoletaGrupo(grupoEl) {
    const btns = Array.from(grupoEl.querySelectorAll('.servico-btn'));
    if (btns.length < 2) return;
    let idx = -1;   // -1 = casa vazia (estado inicial de todo retangulo)
    let aberto = false;
    let ultimoWheel = 0;
    let visiveis = [];
    let selBusca = 0;
    let emErro = false;
    let tLimpa = null;
    let tGira = null;
    // codigo, nome e descricao lidos do proprio botao: o HTML segue sendo a fonte
    const itens = btns.map(b => {
        const desc = b.querySelector('.desc');
        const nome = Array.from(b.childNodes).filter(n => n.nodeType === 3).map(n => n.textContent).join('').replace(/^\s*-\s*/, '').trim();
        return { cod: b.getAttribute('data-cod'), nome: nome, desc: desc ? desc.textContent : '' };
    });

    const nav = document.createElement('div');
    nav.className = 'roleta-nav';
    nav.innerHTML = '<button type="button" class="roleta-seta roleta-cima" aria-label="Servico anterior">&#9650;</button>'
                   + '<div class="roleta-dots"></div>'
                   + '<button type="button" class="roleta-seta roleta-baixo" aria-label="Proximo servico">&#9660;</button>'
                   + '<button type="button" class="roleta-mini roleta-lupa" title="Digitar codigo" aria-label="Digitar codigo">&#128269;</button>'
                   + '<button type="button" class="roleta-mini roleta-limpar" title="Deixar vazio" aria-label="Deixar vazio" hidden>&#10005;</button>';
    grupoEl.insertBefore(nav, btns[0]);
    const dotsWrap = nav.querySelector('.roleta-dots');
    const dotVazio = document.createElement('span');
    dotVazio.className = 'roleta-dot vazio';
    dotsWrap.appendChild(dotVazio);
    btns.forEach(() => {
        const dot = document.createElement('span');
        dot.className = 'roleta-dot';
        dotsWrap.appendChild(dot);
    });
    const dots = Array.from(dotsWrap.querySelectorAll('.roleta-dot:not(.vazio)'));
    const lupa = nav.querySelector('.roleta-lupa');
    const limpar = nav.querySelector('.roleta-limpar');

    // palco: casa vazia + os botoes reais (continuam todos no HTML, so escondidos)
    const palco = document.createElement('div');
    palco.className = 'roleta-palco';
    const vazio = document.createElement('button');
    vazio.type = 'button';
    vazio.className = 'roleta-vazio';
    vazio.innerHTML = '<span>Vazio</span><span class="dica">clique para digitar</span>';
    grupoEl.insertBefore(palco, btns[0]);
    palco.appendChild(vazio);
    btns.forEach(b => palco.appendChild(b));

    const busca = document.createElement('div');
    busca.className = 'roleta-busca';
    busca.innerHTML = '<input type="text" autocomplete="off" spellcheck="false" placeholder="Digite o codigo ou o nome" aria-label="Buscar codigo">'
                    + '<ul></ul><div class="rodape">Enter escolhe - Esc volta - setas descem a lista</div>';
    grupoEl.appendChild(busca);
    const input = busca.querySelector('input');
    const lista = busca.querySelector('ul');

    function atual() { return idx < 0 ? vazio : btns[idx]; }
    function outrosFora() {
        _roletaInstances.forEach(r => { if (r !== inst) { r.desarmar(); r.fecharBusca(); } });
    }
    function armar() {
        outrosFora();
        _roletaArmada = inst;
        grupoEl.classList.add('roleta-armada');
    }
    function desarmar() {
        grupoEl.classList.remove('roleta-armada');
        if (_roletaArmada === inst) _roletaArmada = null;
    }
    function limparAnim() {
        [vazio, palco].concat(btns).forEach(el => el.classList.remove('rl-entra-baixo', 'rl-entra-cima', 'rl-encaixe', 'rl-varre', 'rl-anel'));
    }
    // dir: +1 proximo (sobe), -1 anterior (desce), 0 sem giro. encaixe: codigo caiu na casa.
    function mostrar(novo, dir, encaixe) {
        const antigo = atual();
        idx = novo;
        const prox = atual();
        clearTimeout(tLimpa);
        limparAnim();
        const efeito = _rolEfeito();
        if (efeito && dir !== 0 && antigo !== prox) {
            const f = document.createElement('div');
            f.className = antigo.className.replace(/\brl-\S+/g, '').trim() + ' roleta-fantasma ' + (dir > 0 ? 'rl-sai-cima' : 'rl-sai-baixo');
            f.innerHTML = antigo.innerHTML;
            f.setAttribute('aria-hidden', 'true');
            palco.appendChild(f);
            palco.classList.add('girando');
            clearTimeout(tGira);
            tGira = setTimeout(() => {
                palco.classList.remove('girando');
                palco.querySelectorAll('.roleta-fantasma').forEach(x => x.remove());
            }, 380);
        }
        refresh();
        if (!efeito) return;
        void palco.offsetWidth;
        if (encaixe) { prox.classList.add('rl-encaixe', 'rl-varre'); palco.classList.add('rl-anel'); }
        else if (dir !== 0 && antigo !== prox) { prox.classList.add(dir > 0 ? 'rl-entra-baixo' : 'rl-entra-cima'); }
        tLimpa = setTimeout(limparAnim, 700);
    }
    function mover(dir) {
        if (aberto) fecharBusca();
        const total = btns.length + 1;   // a casa vazia entra no giro
        mostrar(((idx + 1 + dir + total) % total) - 1, dir, false);
        armar();
    }
    function confirmar() {
        const b = btns[idx];
        if (b) b.click();   // grupo armado: o clique cai no onclick do botao, como hoje
    }
    function refresh() {
        vazio.style.display = idx === -1 ? '' : 'none';
        btns.forEach((b, i) => { b.style.display = i === idx ? '' : 'none'; });
        const m = typeof getMatriculaAtiva === 'function' ? getMatriculaAtiva() : null;
        dotVazio.classList.toggle('ativo', idx === -1);
        dots.forEach((d, i) => {
            d.classList.toggle('ativo', i === idx);
            const cod = btns[i].getAttribute('data-cod');
            d.classList.toggle('preenchido', !!(m && m.servicos.some(s => s.codigo === cod)));
        });
        limpar.hidden = idx === -1;
    }

    // ----- busca por codigo ou nome -----
    function abrirBusca(prefill) {
        outrosFora();
        aberto = true;
        grupoEl.classList.add('roleta-buscando');
        emErro = false;
        input.value = prefill || '';
        filtrar();
        input.focus();
        input.setSelectionRange(input.value.length, input.value.length);
    }
    function fecharBusca() {
        aberto = false;
        grupoEl.classList.remove('roleta-buscando');
    }
    function destacar(txt, q) {
        const i = q ? _rolNorm(txt).indexOf(q) : -1;
        if (i < 0) return _rolEsc(txt);
        return _rolEsc(txt.slice(0, i)) + '<mark>' + _rolEsc(txt.slice(i, i + q.length)) + '</mark>' + _rolEsc(txt.slice(i + q.length));
    }
    function filtrar() {
        const q = _rolNorm(input.value.trim());
        visiveis = itens.map((it, i) => ({ it: it, i: i }))
            .filter(x => !q || x.it.cod.indexOf(q) >= 0 || _rolNorm(x.it.nome).indexOf(q) >= 0);
        // codigo que comeca igual ao digitado vem primeiro
        visiveis.sort((a, b) => (b.it.cod.indexOf(q) === 0) - (a.it.cod.indexOf(q) === 0));
        selBusca = 0;
        let html = '';
        visiveis.forEach((x, n) => {
            html += '<li data-i="' + x.i + '"' + (n === 0 ? ' class="sel"' : '') + ' style="animation-delay:' + (n * 22) + 'ms">'
                  + '<b>' + destacar(x.it.cod, q) + '</b><span>' + destacar(x.it.nome, q) + '</span><span class="d">' + _rolEsc(x.it.desc) + '</span></li>';
        });
        let msg = '';
        let erro = false;
        if (q && !visiveis.length) {
            erro = true;
            const so = q.replace(/\D/g, '');
            const onde = so.length >= 3 ? _rolOnde(so) : [];
            if (onde.length) msg = 'O ' + so + ' existe, mas fica em: ' + onde.join(' / ') + '. Aqui nao cabe.';
            else if (so.length >= 4) msg = 'Codigo ' + so + ' nao existe.';
            else { msg = 'Nada encontrado.'; erro = false; }
        }
        if (erro && !emErro) { _rolReflow(input, 'rl-treme'); }
        emErro = erro;
        lista.innerHTML = html + (msg ? '<div class="msg">' + _rolEsc(msg) + '</div>' : '');
        // codigo completo e unico encaixa sozinho (so preenche a casa, nao registra nada)
        if (/^\d{4}$/.test(q) && visiveis.length === 1 && visiveis[0].it.cod === q) {
            const alvo = visiveis[0].i;
            setTimeout(() => { if (aberto && input.value.trim() === q) escolher(alvo); }, 140);
        }
    }
    function marcar(n) {
        const lis = lista.querySelectorAll('li');
        if (!lis.length) return;
        selBusca = (n + lis.length) % lis.length;
        lis.forEach((li, k) => li.classList.toggle('sel', k === selBusca));
    }
    function escolher(i) {
        fecharBusca();
        mostrar(i, 0, true);
        armar();
    }

    input.addEventListener('input', filtrar);
    input.addEventListener('keydown', e => {
        if (e.key === 'ArrowDown') { e.preventDefault(); marcar(selBusca + 1); }
        else if (e.key === 'ArrowUp') { e.preventDefault(); marcar(selBusca - 1); }
        else if (e.key === 'Enter') { e.preventDefault(); const x = visiveis[selBusca]; if (x) escolher(x.i); }
        else if (e.key === 'Escape') { e.preventDefault(); e.stopPropagation(); fecharBusca(); if (idx >= 0) armar(); lupa.focus(); }
    });
    lista.addEventListener('mousedown', e => {
        const li = e.target.closest('li');
        if (!li) return;
        e.preventDefault();
        escolher(parseInt(li.getAttribute('data-i'), 10));
    });
    lista.addEventListener('mouseover', e => {
        const li = e.target.closest('li');
        if (li) marcar(Array.prototype.indexOf.call(lista.querySelectorAll('li'), li));
    });
    vazio.addEventListener('click', e => { e.stopPropagation(); abrirBusca(''); });
    lupa.addEventListener('click', e => { e.stopPropagation(); abrirBusca(''); });
    limpar.addEventListener('click', e => {
        e.stopPropagation();
        if (aberto) fecharBusca();
        mostrar(-1, -1, false);
        armar();
    });

    nav.querySelector('.roleta-cima').addEventListener('click', e => { e.stopPropagation(); mover(-1); });
    nav.querySelector('.roleta-baixo').addEventListener('click', e => { e.stopPropagation(); mover(1); });
    grupoEl.addEventListener('wheel', e => {
        if (aberto) return;
        e.preventDefault();
        const agora = Date.now();
        if (agora - ultimoWheel < 110) return;   // um passo por vez, controlavel
        ultimoWheel = agora;
        mover(e.deltaY > 0 ? 1 : -1);
    }, { passive: false });
    grupoEl.addEventListener('click', function (e) {
        if (!e.target.closest('.servico-btn')) return;
        if (!grupoEl.classList.contains('roleta-armada')) {
            e.stopPropagation();
            armar();
        } else {
            desarmar();
        }
    }, true);
    document.addEventListener('click', e => { if (!grupoEl.contains(e.target)) { desarmar(); fecharBusca(); } });
    document.addEventListener('keydown', e => { if (e.key === 'Escape') desarmar(); });
    // Teclado com o grupo armado: digitar abre a busca, setas giram, Enter registra, Delete esvazia.
    document.addEventListener('keydown', e => {
        if (_roletaArmada !== inst || aberto) return;
        if (e.ctrlKey || e.metaKey || e.altKey) return;
        const t = e.target;
        if (t && (t.tagName === 'INPUT' || t.tagName === 'TEXTAREA' || t.tagName === 'SELECT' || t.isContentEditable)) return;
        const aba = document.getElementById('aba-fluxo');
        if (!aba || !aba.classList.contains('active')) return;
        const modal = document.getElementById('modalOverlay');
        if (modal && modal.classList.contains('ativo')) return;
        if (/^\d$/.test(e.key)) { e.preventDefault(); abrirBusca(e.key); }
        else if (e.key === 'ArrowDown') { e.preventDefault(); mover(1); }
        else if (e.key === 'ArrowUp') { e.preventDefault(); mover(-1); }
        else if (e.key === 'Enter' && idx >= 0) { e.preventDefault(); confirmar(); }
        else if (e.key === 'Backspace' || e.key === 'Delete') { e.preventDefault(); mostrar(-1, -1, false); }
    });

    const inst = { refresh: refresh, desarmar: desarmar, fecharBusca: fecharBusca };
    refresh();
    _roletaInstances.push(inst);
}

'''
s = s[:ini] + crlf(NOVA_FUNCAO) + s[fim:]

# ---------------------------------------------------------------- 4. plano B do export limpo
ANCORA_B = "    todos('.roleta-grupo').forEach(el => el.classList.remove('roleta-armada'));\n"
PLANO_B = ANCORA_B + r'''    //    A busca e o palco tambem sao gerados na tela: desembrulha os botoes reais
    //    e apaga o resto, senao initRoletas() embrulha de novo por cima.
    todos('.roleta-palco').forEach(p => {
        p.querySelectorAll('.servico-btn:not(.roleta-fantasma)').forEach(b => { b.removeAttribute('style'); p.parentNode.insertBefore(b, p); });
        p.remove();
    });
    todos('.roleta-busca').forEach(el => el.remove());
    todos('.roleta-grupo').forEach(el => el.classList.remove('roleta-buscando'));
'''
s = troca(s, ANCORA_B, PLANO_B, 'plano B roletas')

with open('index.html', 'w', encoding='utf-8', newline='') as f:
    f.write(s)
print('OK: patch aplicado.')
