# -*- coding: utf-8 -*-
"""
ETAPA 2 - Arquivo unico.

Problema: a aba 6 era um <iframe src="anonimizador.html">, caminho relativo.
Sem o arquivo irmao do lado, a aba abria em branco e calada. E o irmao nao
viaja no fluxo Google Docs, nem no botao Baixar do banner, nem no cache do
service worker.

Correcao: o iframe passa a ser alimentado pelo Base64 que JA esta embutido no
proprio index.html. O VTO volta a ser um arquivo so.

Alteracoes (todas localizadas):
  1. <!-- ABA 6 --> : iframe sem src + aviso visivel de falha
  2. CSS novo, escopado a aba 6 (altura util e Linha do Tempo fora do caminho)
  3. mostrarAba() : carrega sob demanda e marca o body
  4. nova funcao carregarAnonimizador()
  5. prepararHtmlLimpo() : limpa o srcdoc, senao o export leva o
     anonimizador DUAS vezes dentro do arquivo

Nao toca em anonimizador.html nem nas abas 1 a 5.
"""
import io
import sys

CAMINHO = "index.html"

# ---------------------------------------------------------------- 1. ABA 6
ABA6_ANTIGA = """<!-- ABA 6: ANONIMIZADOR -->
<div id="aba-anonimizador" class="tab-content">
    <div class="card" style="padding:0;overflow:hidden">
        <iframe src="anonimizador.html" style="width:100%;height:85vh;border:none;border-radius:12px" title="Anonimizador Sanepar"></iframe>
    </div>
</div>
"""

ABA6_NOVA = """<!-- ABA 6: ANONIMIZADOR -->
<div id="aba-anonimizador" class="tab-content">
    <div class="anon-caixa">
        <iframe id="anonimizadorFrame" title="Anonimizador Sanepar"></iframe>
        <div class="anon-aviso" id="anonimizadorAviso">
            <strong>O anonimizador nao abriu.</strong>
            <span>O bloco embutido neste arquivo pode estar corrompido. Baixe o VTO de novo e abra outra vez.</span>
        </div>
    </div>
</div>
"""

# ------------------------------------------------------------------- 2. CSS
CSS_ANTIGO = """.matricula-header .campo{min-width:100%}
}
</style>"""

CSS_NOVO = """.matricula-header .campo{min-width:100%}
}
/* ===== ABA 6: ANONIMIZADOR ===== */
.anon-caixa{background:white;border-radius:16px;box-shadow:0 4px 20px rgba(0,0,0,.08);overflow:hidden;margin-bottom:20px}
#anonimizadorFrame{display:block;width:100%;height:calc(100vh - 140px);min-height:540px;border:none}
.anon-aviso{display:none;padding:48px 30px;text-align:center;color:#c62828;line-height:1.6}
.anon-aviso.ativo{display:block}
.anon-aviso strong{display:block;margin-bottom:8px;font-size:1.05rem}
body.anon-aberto .timeline-panel{display:none}
</style>"""

# ------------------------------------------------------------ 3. mostrarAba
ABAS_ANTIGO = """    if (aba === 'fluxo') { setTimeout(() => { const el = document.getElementById('matriculaInputCard1'); if (el) el.focus(); }, 100); }
}
"""

ABAS_NOVO = """    if (aba === 'fluxo') { setTimeout(() => { const el = document.getElementById('matriculaInputCard1'); if (el) el.focus(); }, 100); }
    // A aba do anonimizador precisa da tela inteira: recolhe a Linha do Tempo
    document.body.classList.toggle('anon-aberto', aba === 'anonimizador');
    if (aba === 'anonimizador') { carregarAnonimizador(); }
}

// ===== ABA 6: ANONIMIZADOR EMBUTIDO =====
// O anonimizador mora dentro deste arquivo, em Base64. Nao existe arquivo
// irmao: o VTO continua sendo um arquivo so, que e do que o app depende
// para sobreviver ao fluxo Google Docs -> Bloco de Notas.
let _anonimizadorCarregado = false;
function carregarAnonimizador() {
    if (_anonimizadorCarregado) return;
    const quadro = document.getElementById('anonimizadorFrame');
    const aviso = document.getElementById('anonimizadorAviso');
    if (!quadro) return;

    let html = '';
    try {
        const fonte = document.getElementById('anonimizadorFonte');
        if (fonte && fonte.textContent) {
            const bin = atob(fonte.textContent.trim());
            const bytes = new Uint8Array(bin.length);
            for (let i = 0; i < bin.length; i++) bytes[i] = bin.charCodeAt(i);
            html = new TextDecoder('utf-8').decode(bytes);
        }
    } catch (e) {
        html = '';
    }

    if (!html) {
        quadro.style.display = 'none';
        if (aviso) aviso.classList.add('ativo');
        return;
    }

    // Aqui dentro o botao "voltar ao VTO" do anonimizador nao faz sentido:
    // o VTO esta na aba do lado. Sem tirar, ele abre o VTO dentro do VTO.
    html = html.replace(/<a[^>]*class="nav-vto-btn"[^>]*>[\\s\\S]*?<\\/a>/, '');

    quadro.srcdoc = html;
    _anonimizadorCarregado = true;
}
"""

# ----------------------------------------------- 5. limpeza do srcdoc no export
LIMPEZA_ANTIGA = """    // 8. Abre na aba 1, do jeito que um arquivo novo abre
"""

LIMPEZA_NOVA = """    // 8. Anonimizador embutido - o iframe recebe o HTML inteiro no srcdoc.
    //    Sem limpar, o arquivo exportado levaria o anonimizador duas vezes.
    const quadroAnon = um('#anonimizadorFrame');
    if (quadroAnon) {
        quadroAnon.removeAttribute('srcdoc');
        quadroAnon.style.display = '';
    }
    const avisoAnon = um('#anonimizadorAviso');
    if (avisoAnon) avisoAnon.classList.remove('ativo');

    // 9. Abre na aba 1, do jeito que um arquivo novo abre
"""

TROCAS = [
    ("bloco da ABA 6", ABA6_ANTIGA, ABA6_NOVA),
    ("CSS da aba 6", CSS_ANTIGO, CSS_NOVO),
    ("fim de mostrarAba()", ABAS_ANTIGO, ABAS_NOVO),
    ("limpeza do srcdoc no export", LIMPEZA_ANTIGA, LIMPEZA_NOVA),
]


def main():
    with io.open(CAMINHO, encoding="utf-8", newline="") as f:
        html = f.read()

    if "function carregarAnonimizador()" in html:
        print("ABORTADO: carregarAnonimizador() ja existe. Nada foi alterado.")
        return 1
    if "function prepararHtmlLimpo()" not in html:
        print("ABORTADO: a Etapa 1 precisa estar aplicada antes. Nada foi alterado.")
        return 1

    for nome, antigo, _novo in TROCAS:
        if html.count(antigo) != 1:
            print("ABORTADO: ancora '%s' apareceu %d vez(es), esperava 1. "
                  "Nada foi alterado." % (nome, html.count(antigo)))
            return 1

    novo = html
    for _nome, antigo, troca in TROCAS:
        novo = novo.replace(antigo, troca, 1)

    with io.open(CAMINHO, "w", encoding="utf-8", newline="") as f:
        f.write(novo)

    print("OK. %d -> %d caracteres (+%d)" % (len(html), len(novo), len(novo) - len(html)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
