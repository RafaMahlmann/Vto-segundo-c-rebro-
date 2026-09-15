# -*- coding: utf-8 -*-
"""
Teste da ETAPA 5 - Desfazer e Refazer.

Roda o app de verdade em file:// com o Playwright.
O teste que importa e o 4: antes da correcao, o Refazer devolvia o estado
ERRADO (o mesmo que o Desfazer), porque o estado de agora nunca entrava
no historico.

Uso:  venv_agente/Scripts/python.exe patches/_test_etapa5.py
"""
import pathlib
import sys

from playwright.sync_api import sync_playwright

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

RAIZ = pathlib.Path(__file__).resolve().parent.parent
INDEX = RAIZ / "index.html"

falhas = []
passou = []


def checa(nome, condicao, detalhe=""):
    if condicao:
        passou.append(nome)
        print("  OK   %s %s" % (nome, detalhe))
    else:
        falhas.append(nome)
        print("  FALHA %s %s" % (nome, detalhe))


def estado(pg):
    return pg.evaluate("""() => ({
        total: matriculas.length,
        ativa: matriculaAtiva,
        desfazer: historico.length,
        refazer: historicoFuturo.length,
        btnUndo: document.getElementById('btnUndo').disabled,
        btnRedo: document.getElementById('btnRedo').disabled
    })""")


def adiciona(pg, numero):
    pg.evaluate("""(n) => {
        const i = document.getElementById('novaMatricula')
              || document.querySelector('#aba-matriculas input[type=text]');
        i.value = n;
        adicionarMatricula();
    }""", numero)
    pg.wait_for_timeout(200)


def main():
    with sync_playwright() as p:
        nav = p.chromium.launch()
        pg = nav.new_page(viewport={"width": 1400, "height": 900})
        erros = []
        pg.on("pageerror", lambda e: erros.append("pageerror: " + str(e)[:150]))
        pg.on("console", lambda m: erros.append("console.error: " + m.text[:150])
              if m.type == "error" else None)
        pg.goto(INDEX.as_uri())
        pg.wait_for_timeout(1500)
        pg.click("button:has-text('Matriculas')")
        pg.wait_for_timeout(500)

        # ---------- 1. estado inicial ----------
        print("\n[1] estado ao abrir o app")
        e = estado(pg)
        checa("comeca com 30 matriculas", e["total"] == 30, "(%d)" % e["total"])
        checa("nada para desfazer", e["desfazer"] == 0, "(pilha %d)" % e["desfazer"])
        checa("nada para refazer", e["refazer"] == 0, "(pilha %d)" % e["refazer"])
        checa("botao Desfazer apagado", e["btnUndo"] is True)
        checa("botao Refazer apagado", e["btnRedo"] is True)

        # ---------- 2. uma alteracao ----------
        print("\n[2] adiciona a matricula 99999999")
        adiciona(pg, "99999999")
        e = estado(pg)
        checa("virou 31 matriculas", e["total"] == 31, "(%d)" % e["total"])
        checa("Desfazer acendeu", e["btnUndo"] is False)
        checa("Refazer continua apagado", e["btnRedo"] is True)

        # ---------- 3. desfazer ----------
        print("\n[3] Ctrl+Z")
        pg.keyboard.press("Control+z")
        pg.wait_for_timeout(300)
        e = estado(pg)
        checa("voltou para 30", e["total"] == 30, "(%d)" % e["total"])
        checa("99999999 sumiu da lista",
              pg.evaluate("() => !matriculas.find(m => m.numero === '99999999')"))
        checa("Refazer acendeu", e["btnRedo"] is False)
        checa("Desfazer apagou de novo", e["btnUndo"] is True)

        # ---------- 4. refazer: O TESTE QUE IMPORTA ----------
        print("\n[4] Ctrl+Shift+Z  <-- e aqui que estava quebrado")
        pg.keyboard.press("Control+Shift+z")
        pg.wait_for_timeout(300)
        e = estado(pg)
        checa("REFAZER devolveu as 31", e["total"] == 31, "(%d)" % e["total"])
        checa("99999999 voltou para a lista",
              pg.evaluate("() => !!matriculas.find(m => m.numero === '99999999')"))
        checa("Desfazer acendeu de novo", e["btnUndo"] is False)
        checa("Refazer apagou", e["btnRedo"] is True)

        # ---------- 5. varios passos ----------
        print("\n[5] tres alteracoes seguidas, desfaz tudo, refaz tudo")
        for n in ["11111111", "22222222", "33333333"]:
            adiciona(pg, n)
        checa("chegou a 34", estado(pg)["total"] == 34, "(%d)" % estado(pg)["total"])
        caminho = []
        for _ in range(4):
            pg.keyboard.press("Control+z")
            pg.wait_for_timeout(180)
            caminho.append(estado(pg)["total"])
        checa("desfaz um passo por vez", caminho == [33, 32, 31, 30], "(%s)" % caminho)
        volta = []
        for _ in range(4):
            pg.keyboard.press("Control+Shift+z")
            pg.wait_for_timeout(180)
            volta.append(estado(pg)["total"])
        checa("refaz um passo por vez", volta == [31, 32, 33, 34], "(%s)" % volta)

        # ---------- 6. alteracao nova apaga o refazer ----------
        print("\n[6] alteracao nova depois de desfazer")
        pg.keyboard.press("Control+z")
        pg.wait_for_timeout(200)
        checa("tem o que refazer antes", estado(pg)["refazer"] > 0,
              "(pilha %d)" % estado(pg)["refazer"])
        adiciona(pg, "44444444")
        e = estado(pg)
        checa("o caminho de volta foi apagado", e["refazer"] == 0, "(pilha %d)" % e["refazer"])
        checa("botao Refazer apagou", e["btnRedo"] is True)

        # ---------- 7. botoes da tela ----------
        print("\n[7] botoes Desfazer e Refazer da tela")
        antes = estado(pg)["total"]
        pg.click("#btnUndo")
        pg.wait_for_timeout(250)
        depois = estado(pg)["total"]
        checa("botao Desfazer funciona", depois == antes - 1, "(%d -> %d)" % (antes, depois))
        pg.click("#btnRedo")
        pg.wait_for_timeout(250)
        checa("botao Refazer funciona", estado(pg)["total"] == antes,
              "(%d -> %d)" % (depois, estado(pg)["total"]))

        # ---------- 8. remover tambem desfaz ----------
        print("\n[8] remover matricula e desfazer")
        pg.on("dialog", lambda d: d.accept())
        alvo = pg.evaluate("() => matriculas[0].numero")
        pg.evaluate("(n) => removerMatricula(n)", alvo)
        pg.wait_for_timeout(300)
        sumiu = pg.evaluate("(n) => !matriculas.find(m => m.numero === n)", alvo)
        checa("matricula removida", sumiu, "(%s)" % alvo)
        pg.keyboard.press("Control+z")
        pg.wait_for_timeout(300)
        checa("Ctrl+Z traz a matricula de volta",
              pg.evaluate("(n) => !!matriculas.find(m => m.numero === n)", alvo))

        # ---------- 9. matricula ativa acompanha ----------
        print("\n[9] a matricula ativa volta junto")
        pg.evaluate("() => { salvarHistorico(); matriculaAtiva = '11111111'; atualizarMatriculaAtivaNosCards(); }")
        pg.wait_for_timeout(200)
        antes_ativa = estado(pg)["ativa"]
        pg.keyboard.press("Control+z")
        pg.wait_for_timeout(250)
        depois_ativa = estado(pg)["ativa"]
        checa("a ativa muda ao desfazer", depois_ativa != antes_ativa,
              "(%s -> %s)" % (antes_ativa, depois_ativa))
        pg.keyboard.press("Control+Shift+z")
        pg.wait_for_timeout(250)
        checa("a ativa volta ao refazer", estado(pg)["ativa"] == antes_ativa,
              "(%s)" % estado(pg)["ativa"])

        # ---------- 10. teto de 50 ----------
        print("\n[10] teto do historico")
        pg.evaluate("""() => {
            for (let i = 0; i < 70; i++) {
                salvarHistorico();
                matriculas.push({ numero: String(50000000 + i), servicos: [], ativa: false });
            }
        }""")
        pg.wait_for_timeout(300)
        e = estado(pg)
        checa("historico nao passa de 50", e["desfazer"] <= 50, "(pilha %d)" % e["desfazer"])

        # ---------- 11. o retrato do export nao foi afetado ----------
        print("\n[11] o pacote continua limpo depois de tudo isso")
        limpo = pg.evaluate("() => prepararHtmlLimpo()")
        fonte = INDEX.read_text(encoding="utf-8")
        vazou = [n for n in ["99999999", "44444444", "50000000"]
                 if limpo.count(n) > fonte.count(n)]
        checa("nenhuma matricula de teste no pacote", not vazou, "(%s)" % (vazou or "nenhuma"))

        checa("console sem erro no percurso inteiro", len(erros) == 0,
              "" if not erros else "\n         " + "\n         ".join(erros[:5]))
        nav.close()

    print("\n" + "=" * 62)
    print("PASSOU: %d    FALHOU: %d" % (len(passou), len(falhas)))
    if falhas:
        print("Falhas: " + ", ".join(falhas))
    print("=" * 62)
    return 1 if falhas else 0


if __name__ == "__main__":
    sys.exit(main())
