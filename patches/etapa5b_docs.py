# -*- coding: utf-8 -*-
"""
ETAPA 5b - Documenta o modelo novo de desfazer/refazer.

O AGENTS.md dizia so "chamar salvarHistorico() antes de alterar matriculas[]".
Essa regra continua valendo - e justamente por isso o Refazer quebrava: o
estado de agora nunca entrava no historico. Agora sao duas pilhas, e a linha
do mapa precisa dizer isso.

Mexe em: AGENTS.md e TIMELINE.md. Nao toca em codigo.
"""
import io
import os
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

AGENTS_ANTIGO = "| `// ===== UNDO / REDO =====` | 716+ | Snapshots; chamar `salvarHistorico()` **antes** de alterar `matriculas[]` |"

AGENTS_NOVO = ("| `// ===== UNDO / REDO =====` | ~809+ | **Duas pilhas**: `historico` (antes) e `historicoFuturo` (desfeito). "
               "Chamar `salvarHistorico()` **antes** de alterar `matriculas[]` — quem guarda o estado de agora é o `undo()` |")

AGENTS_EXTRA = """
**Desfazer e refazer são duas pilhas, não um índice.**
`salvarHistorico()` é chamado **antes** de alterar `matriculas[]` — os 9 pontos
que fazem isso estão certos e não devem mudar. A consequência é que o estado
*atual* nunca está em `historico`: quem o empilha é o `undo()`, em
`historicoFuturo`, no instante em que desfaz.
Foi a falta disso que deixou o Refazer quebrado desde sempre — com uma pilha só
e um índice, o estado pós-alteração não existia em lugar nenhum.
Ao criar uma função que altera `matriculas[]`: chame `salvarHistorico()` antes,
e só isso. Não empilhe nada depois, não mexa em `historicoFuturo`.
Para definir um novo ponto de partida (carga de dados, não alteração do
usuário), use `limparHistorico()` — é o que o `gerarMockData()` faz.
"""

TIMELINE_EXTRA = """
---

## PARTE 10 — Refazer (2026-09-14, v4.4)

O `Ctrl+Shift+Z` e o botão Refazer nunca funcionaram. Não era o atalho.

O histórico era uma pilha só com um índice. Como o protocolo manda chamar
`salvarHistorico()` **antes** de alterar `matriculas[]`, a pilha só guardava
estados anteriores — o estado pós-alteração não era gravado em lugar nenhum.
Refazer era impossível por construção, e o `Ctrl+Z` só acertava por
coincidência, porque os dois últimos estados eram iguais.

Passou a ter duas pilhas: `historico` e `historicoFuturo`. O `undo()` empilha o
estado de agora antes de voltar — era esse o estado que faltava. Os 9 pontos que
chamam `salvarHistorico()` não mudaram: o protocolo do `AGENTS.md` continua
valendo palavra por palavra.

De quebra, o `gerarMockData()` passou a chamar `limparHistorico()`: os dados de
demonstração são ponto de partida, não alteração do usuário.

Teste: `patches/_test_etapa5.py` (31 verificações).
"""


def aplica(nome, trocas, acrescimo=None):
    caminho = os.path.join(RAIZ, nome)
    with io.open(caminho, encoding="utf-8", newline="") as f:
        txt = f.read()
    for rotulo, antigo, novo in trocas:
        if txt.count(antigo) != 1:
            print("  ABORTADO em %s: '%s' apareceu %d vez(es)." % (nome, rotulo, txt.count(antigo)))
            return False
        txt = txt.replace(antigo, novo, 1)
    if acrescimo:
        txt = txt.rstrip("\n") + "\n" + acrescimo
    with io.open(caminho, "w", encoding="utf-8", newline="") as f:
        f.write(txt)
    print("  %s: atualizado" % nome)
    return True


def main():
    ok = aplica("AGENTS.md", [("linha do mapa", AGENTS_ANTIGO, AGENTS_NOVO)], AGENTS_EXTRA)
    ok = aplica("TIMELINE.md", [], TIMELINE_EXTRA) and ok
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
