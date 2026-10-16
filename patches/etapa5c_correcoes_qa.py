# -*- coding: utf-8 -*-
"""
ETAPA 5c - Corrige o que o teste independente achou na Etapa 5.

1. Ctrl+Z SEQUESTRAVA O TECLADO DENTRO DOS CAMPOS (o mais serio)
   O handler nao olhava onde estava o foco e ainda dava preventDefault.
   Medido: digitar uma data em #dataSancao e apertar Ctrl+Z nao desfazia o
   texto - desfazia uma MATRICULA, em silencio, numa aba que a pessoa nem
   estava vendo. Perda de trabalho sem aviso.
   E parte disso foi piora da Etapa 5: o toLowerCase() passou a capturar
   tambem o Ctrl+Shift+Z, que antes escapava com 'Z' maiusculo.
   Correcao: dentro de input, textarea ou campo editavel, o atalho e do
   texto. O VTO nao se mete.

2. AS BOLINHAS DA ROLETA FICAVAM DEFASADAS DEPOIS DE DESFAZER
   aplicarEstado() redesenha tabela e timeline, mas nao as roletas do Fluxo.
   Medido: registrar 8421, Ctrl+Z, e a bolinha continuava preenchida.
   Correcao: uma chamada a atualizarTodasRoletas().

3. O AVISO DO RESET MENTIA
   O confirm dizia "Isso nao pode ser desfeito", mas resetarFluxo() chama
   salvarHistorico() - e o teste provou: Ctrl+Z devolve os 56 servicos.
   E o reset NAO apaga "todos os dados": as 30 matriculas continuam na lista,
   sai so o que foi registrado nelas. O rotulo do botao dizia a mesma
   inverdade.
   Correcao: o botao e o aviso passam a contar a mesma historia, e a historia
   verdadeira (voz-do-vto, regras 1, 6 e 9).

Nao toca nos 9 pontos que chamam salvarHistorico().
"""
import io
import sys

CAMINHO = "index.html"

# ----------------------------------------------- 1. teclado dentro dos campos
TECLADO_ANTIGO = """// Ctrl+Z / Ctrl+Shift+Z
// e.key vem maiusculo em alguns navegadores quando o Shift esta pressionado.
document.addEventListener('keydown', function(e) {
    if (e.ctrlKey && String(e.key).toLowerCase() === 'z') {
        e.preventDefault();
        e.shiftKey ? redo() : undo();
    }
});"""

TECLADO_NOVO = """// Ctrl+Z / Ctrl+Shift+Z
// e.key vem maiusculo em alguns navegadores quando o Shift esta pressionado.
document.addEventListener('keydown', function(e) {
    if (!e.ctrlKey || String(e.key).toLowerCase() !== 'z') return;
    // Dentro de um campo, o Ctrl+Z e do texto que a pessoa esta digitando.
    // Sem esta linha ele desfazia uma MATRICULA, calado, numa aba que ela
    // nem estava vendo - e o campo nao mudava, entao nada denunciava.
    const alvo = e.target;
    if (alvo && (alvo.tagName === 'INPUT' || alvo.tagName === 'TEXTAREA' || alvo.isContentEditable)) return;
    e.preventDefault();
    e.shiftKey ? redo() : undo();
});"""

# ------------------------------------------------- 2. roletas ao desfazer
ESTADO_ANTIGO = """    atualizarMatriculaAtivaNosCards();
    renderMatriculas();
    atualizarTimeline();
    atualizarBotoesUndoRedo();
}

// Chamar SEMPRE antes de alterar matriculas[]."""

ESTADO_NOVO = """    atualizarMatriculaAtivaNosCards();
    renderMatriculas();
    atualizarTimeline();
    // sem isto as bolinhas do Fluxo ficam marcando servico que ja foi desfeito
    atualizarTodasRoletas();
    atualizarBotoesUndoRedo();
}

// Chamar SEMPRE antes de alterar matriculas[]."""

# ------------------------------------------------------ 3. aviso do reset
AVISO_ANTIGO = """    if (!confirm('Limpar TODOS os dados? Isso nao pode ser desfeito.')) return;"""

AVISO_NOVO = """    if (!confirm('Apagar os servicos de todas as matriculas?\\n\\n'
        + 'As matriculas continuam na lista. Sai so o que foi registrado nelas.\\n\\n'
        + 'Da para voltar atras com Ctrl+Z.')) return;"""

BOTAO_ANTIGO = """&#128465; Limpar Todos os Dados</button>"""

BOTAO_NOVO = """&#128465; Apagar servicos</button>"""

TROCAS = [
    ("handler de teclado", TECLADO_ANTIGO, TECLADO_NOVO),
    ("aplicarEstado", ESTADO_ANTIGO, ESTADO_NOVO),
    ("aviso do reset", AVISO_ANTIGO, AVISO_NOVO),
    ("rotulo do botao de reset", BOTAO_ANTIGO, BOTAO_NOVO),
]


def main():
    with io.open(CAMINHO, encoding="utf-8", newline="") as f:
        html = f.read()

    if "alvo.isContentEditable" in html:
        print("ABORTADO: a correcao ja foi aplicada. Nada foi alterado.")
        return 1

    for nome, antigo, _novo in TROCAS:
        if html.count(antigo) != 1:
            print("ABORTADO: ancora '%s' apareceu %d vez(es), esperava 1. "
                  "Nada foi alterado." % (nome, html.count(antigo)))
            return 1

    novo = html
    for _nome, antigo, troca in TROCAS:
        novo = novo.replace(antigo, troca, 1)

    antes = html.count("    salvarHistorico();")
    depois = novo.count("    salvarHistorico();")
    if antes != depois:
        print("ABORTADO: chamadas a salvarHistorico() mudaram de %d para %d. "
              "Nada foi gravado." % (antes, depois))
        return 1

    with io.open(CAMINHO, "w", encoding="utf-8", newline="") as f:
        f.write(novo)

    print("OK. %d -> %d caracteres (+%d)" % (len(html), len(novo), len(novo) - len(html)))
    print("    chamadas a salvarHistorico() intactas: %d" % depois)
    return 0


if __name__ == "__main__":
    sys.exit(main())
