# -*- coding: utf-8 -*-
"""
ETAPA 5 - Conserta o Refazer (Ctrl+Shift+Z), que nunca funcionou.

DIAGNOSTICO
O historico era UMA pilha so, com um indice apontando para o "estado atual".
Mas o protocolo da casa manda chamar salvarHistorico() ANTES de alterar
matriculas[] - e 9 dos 10 pontos fazem exatamente isso, corretamente.

O resultado e que a pilha so guarda estados ANTERIORES. O estado de agora
nunca entra nela. Entao:

  carregou o mock      -> historico [30], indice 0
  adicionou 99999999   -> salvarHistorico() grava 30 de novo, depois o push
                          historico [30, 30], indice 1, e na tela 31
  Ctrl+Z               -> indice 0, restaura 30       (parece funcionar)
  Ctrl+Shift+Z         -> indice 1, restaura 30 OUTRA VEZ

O 31 nunca foi guardado em lugar nenhum, entao refazer e impossivel por
construcao. E o Ctrl+Z so acerta por coincidencia: os dois estados sao iguais.

CORRECAO
Duas pilhas em vez de uma - o modelo classico de desfazer/refazer:

  historico       = estados anteriores (empilha em salvarHistorico)
  historicoFuturo = estados desfeitos  (empilha em undo, desempilha em redo)

undo() empurra o estado DE AGORA para o futuro antes de voltar. E esse estado
de agora que estava faltando. Refazer passa a ter para onde voltar.

A vantagem: isso mantem o protocolo do AGENTS.md intacto. salvarHistorico()
continua sendo chamado ANTES da alteracao, e os 9 pontos nao mudam.

Alteracoes:
  1. a secao // ===== UNDO / REDO ===== inteira
  2. UMA linha em gerarMockData(): salvarHistorico() -> limparHistorico()
     (ela roda DEPOIS do mock, gravando um estado que nao da para desfazer;
      no modelo novo isso deixaria o botao Desfazer aceso sem ter o que fazer)

Nao toca em mais nada.
"""
import io
import sys

CAMINHO = "index.html"

BLOCO_ANTIGO = """// ===== UNDO / REDO =====
let historico = [];
let historicoIndex = -1;
const HISTORICO_MAX = 50;

function salvarHistorico() {
    // Remove estados futuros se estiver no meio do historico
    if (historicoIndex < historico.length - 1) {
        historico = historico.slice(0, historicoIndex + 1);
    }
    // Salva estado atual (deep copy)
    historico.push(JSON.stringify({ matriculas: matriculas, matriculaAtiva: matriculaAtiva }));
    if (historico.length > HISTORICO_MAX) historico.shift();
    else historicoIndex++;
    atualizarBotoesUndoRedo();
}

function undo() {
    if (historicoIndex <= 0) return;
    historicoIndex--;
    const estado = JSON.parse(historico[historicoIndex]);
    matriculas = estado.matriculas;
    matriculaAtiva = estado.matriculaAtiva;
    atualizarMatriculaAtivaNosCards();
    renderMatriculas();
    atualizarTimeline();
    atualizarBotoesUndoRedo();
}

function redo() {
    if (historicoIndex >= historico.length - 1) return;
    historicoIndex++;
    const estado = JSON.parse(historico[historicoIndex]);
    matriculas = estado.matriculas;
    matriculaAtiva = estado.matriculaAtiva;
    atualizarMatriculaAtivaNosCards();
    renderMatriculas();
    atualizarTimeline();
    atualizarBotoesUndoRedo();
}

function atualizarBotoesUndoRedo() {
    const btnUndo = document.getElementById('btnUndo');
    const btnRedo = document.getElementById('btnRedo');
    if (btnUndo) { btnUndo.disabled = historicoIndex <= 0; btnUndo.style.opacity = historicoIndex <= 0 ? '.4' : '1'; }
    if (btnRedo) { btnRedo.disabled = historicoIndex >= historico.length - 1; btnRedo.style.opacity = historicoIndex >= historico.length - 1 ? '.4' : '1'; }
}

// Ctrl+Z / Ctrl+Shift+Z
document.addEventListener('keydown', function(e) {
    if (e.ctrlKey && e.key === 'z') { e.preventDefault(); e.shiftKey ? redo() : undo(); }
});
"""

BLOCO_NOVO = """// ===== UNDO / REDO =====
// Duas pilhas, nao um indice.
//   historico       = como as coisas estavam ANTES de cada alteracao
//   historicoFuturo = o que foi desfeito e pode voltar
// O protocolo continua o mesmo: salvarHistorico() e chamado ANTES de alterar
// matriculas[]. Por isso o estado de AGORA nunca esta na pilha - quem guarda
// ele e o undo(), no momento em que desfaz. Era exatamente esse estado que
// faltava, e por isso o Refazer nunca funcionou.
let historico = [];
let historicoFuturo = [];
const HISTORICO_MAX = 50;

function estadoAtual() {
    return JSON.stringify({ matriculas: matriculas, matriculaAtiva: matriculaAtiva });
}

function aplicarEstado(texto) {
    const estado = JSON.parse(texto);
    matriculas = estado.matriculas;
    matriculaAtiva = estado.matriculaAtiva;
    atualizarMatriculaAtivaNosCards();
    renderMatriculas();
    atualizarTimeline();
    atualizarBotoesUndoRedo();
}

// Chamar SEMPRE antes de alterar matriculas[].
function salvarHistorico() {
    historico.push(estadoAtual());
    if (historico.length > HISTORICO_MAX) historico.shift();
    // Alteracao nova apaga o caminho de volta, como em qualquer editor.
    historicoFuturo = [];
    atualizarBotoesUndoRedo();
}

// Marca o estado de agora como ponto de partida: nao ha o que desfazer antes.
function limparHistorico() {
    historico = [];
    historicoFuturo = [];
    atualizarBotoesUndoRedo();
}

function undo() {
    if (!historico.length) return;
    historicoFuturo.push(estadoAtual());
    aplicarEstado(historico.pop());
}

function redo() {
    if (!historicoFuturo.length) return;
    historico.push(estadoAtual());
    aplicarEstado(historicoFuturo.pop());
}

function atualizarBotoesUndoRedo() {
    const btnUndo = document.getElementById('btnUndo');
    const btnRedo = document.getElementById('btnRedo');
    const semDesfazer = historico.length === 0;
    const semRefazer = historicoFuturo.length === 0;
    if (btnUndo) { btnUndo.disabled = semDesfazer; btnUndo.style.opacity = semDesfazer ? '.4' : '1'; }
    if (btnRedo) { btnRedo.disabled = semRefazer; btnRedo.style.opacity = semRefazer ? '.4' : '1'; }
}

// Ctrl+Z / Ctrl+Shift+Z
// e.key vem maiusculo em alguns navegadores quando o Shift esta pressionado.
document.addEventListener('keydown', function(e) {
    if (e.ctrlKey && String(e.key).toLowerCase() === 'z') {
        e.preventDefault();
        e.shiftKey ? redo() : undo();
    }
});
"""

MOCK_ANTIGO = """    renderMatriculas();
    atualizarTimeline();
    salvarHistorico();
}
"""

MOCK_NOVO = """    renderMatriculas();
    atualizarTimeline();
    // Ponto de partida: os dados de demonstracao nao sao uma alteracao do
    // usuario, entao nao ha o que desfazer antes deles.
    limparHistorico();
}
"""

TROCAS = [
    ("secao UNDO / REDO", BLOCO_ANTIGO, BLOCO_NOVO),
    ("fim de gerarMockData", MOCK_ANTIGO, MOCK_NOVO),
]


def main():
    with io.open(CAMINHO, encoding="utf-8", newline="") as f:
        html = f.read()

    if "historicoFuturo" in html:
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

    # os 9 pontos que chamam salvarHistorico() antes da alteracao nao podem mudar
    antes = html.count("    salvarHistorico();")
    depois = novo.count("    salvarHistorico();")
    esperado = antes - 1  # o de gerarMockData virou limparHistorico
    if depois != esperado:
        print("ABORTADO: chamadas a salvarHistorico() mudaram de %d para %d, "
              "esperava %d. Nada foi gravado." % (antes, depois, esperado))
        return 1

    with io.open(CAMINHO, "w", encoding="utf-8", newline="") as f:
        f.write(novo)

    print("OK. %d -> %d caracteres (+%d)" % (len(html), len(novo), len(novo) - len(html)))
    print("    chamadas a salvarHistorico() preservadas: %d" % depois)
    return 0


if __name__ == "__main__":
    sys.exit(main())
