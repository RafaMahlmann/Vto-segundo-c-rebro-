# -*- coding: utf-8 -*-
"""
Teste da ETAPA 5c - as tres correcoes vindas do teste independente.

Reproduz os passos exatos que o testador usou:
  1. digitar numa data e apertar Ctrl+Z nao pode mexer nas matriculas
  2. a bolinha da roleta tem que apagar quando o servico e desfeito
  3. o aviso do reset tem que dizer a verdade, e o Ctrl+Z tem que cumprir

Uso:  venv_agente/Scripts/python.exe patches/_test_etapa5c.py
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


def main():
    with sync_playwright() as p:
        nav = p.chromium.launch()
        pg = nav.new_page(viewport={"width": 1400, "height": 900})
        erros = []
        pg.on("pageerror", lambda e: erros.append("pageerror: " + str(e)[:150]))
        pg.on("console", lambda m: erros.append("console.error: " + m.text[:150])
              if m.type == "error" else None)
        avisos = []
        pg.on("dialog", lambda d: (avisos.append(d.message), d.accept()))
        pg.goto(INDEX.as_uri())
        pg.wait_for_timeout(1500)

        # ---------- 1. o atalho nao pode roubar o teclado do campo ----------
        print("\n[1] Ctrl+Z dentro de um campo de texto")
        pg.click("button:has-text('Matriculas')")
        pg.wait_for_timeout(400)
        pg.evaluate("""() => {
            const i = document.getElementById('novaMatricula')
                  || document.querySelector('#aba-matriculas input[type=text]');
            i.value = '99999999';
            adicionarMatricula();
        }""")
        pg.wait_for_timeout(300)
        checa("preparo: 31 matriculas", pg.evaluate("() => matriculas.length") == 31)

        pg.click("button:has-text('Calculadora de Prazo')")
        pg.wait_for_timeout(400)
        pg.click("#dataSancao")
        pg.type("#dataSancao", "15032026", delay=15)
        pg.wait_for_timeout(200)
        antes = pg.evaluate("() => matriculas.length")
        pg.keyboard.press("Control+z")
        pg.wait_for_timeout(300)
        depois = pg.evaluate("() => matriculas.length")
        checa("Ctrl+Z no campo NAO desfaz matricula", antes == depois,
              "(%d -> %d)" % (antes, depois))
        checa("o campo continua sendo da pessoa",
              pg.evaluate("() => document.activeElement.id") == "dataSancao")

        pg.keyboard.press("Control+Shift+z")
        pg.wait_for_timeout(300)
        checa("Ctrl+Shift+Z no campo NAO refaz matricula",
              pg.evaluate("() => matriculas.length") == antes,
              "(%d)" % pg.evaluate("() => matriculas.length"))

        # fora do campo o atalho tem que continuar funcionando
        print("\n[2] fora do campo o atalho continua valendo")
        pg.click("button:has-text('Matriculas')")
        pg.wait_for_timeout(400)
        pg.evaluate("() => document.activeElement.blur()")
        pg.keyboard.press("Control+z")
        pg.wait_for_timeout(300)
        checa("Ctrl+Z fora de campo desfaz", pg.evaluate("() => matriculas.length") == 30,
              "(%d)" % pg.evaluate("() => matriculas.length"))
        pg.keyboard.press("Control+Shift+z")
        pg.wait_for_timeout(300)
        checa("Ctrl+Shift+Z fora de campo refaz", pg.evaluate("() => matriculas.length") == 31,
              "(%d)" % pg.evaluate("() => matriculas.length"))

        # ---------- 3. bolinhas da roleta ----------
        print("\n[3] bolinha da roleta depois de desfazer")
        pg.evaluate("""() => {
            matriculaAtiva = '10045206';
            atualizarMatriculaAtivaNosCards();
            salvarHistorico();
            const m = matriculas.find(x => x.numero === '10045206');
            m.servicos.push({ codigo: '8421', dataCriacao: '2026-03-10', dataBaixa: null, fase: 1 });
            renderMatriculas();
            atualizarTimeline();
            atualizarTodasRoletas();
        }""")
        pg.wait_for_timeout(400)
        cheias_antes = pg.evaluate("() => document.querySelectorAll('.roleta-dot.preenchido').length")
        pg.keyboard.press("Control+z")
        pg.wait_for_timeout(400)
        cheias_depois = pg.evaluate("() => document.querySelectorAll('.roleta-dot.preenchido').length")
        checa("a bolinha apaga ao desfazer", cheias_depois < cheias_antes,
              "(%d -> %d bolinhas preenchidas)" % (cheias_antes, cheias_depois))
        pg.keyboard.press("Control+Shift+z")
        pg.wait_for_timeout(400)
        checa("a bolinha volta ao refazer",
              pg.evaluate("() => document.querySelectorAll('.roleta-dot.preenchido').length") == cheias_antes,
              "(%d)" % pg.evaluate("() => document.querySelectorAll('.roleta-dot.preenchido').length"))

        # ---------- 4. o aviso do reset ----------
        print("\n[4] o aviso do reset diz a verdade")
        servicos_antes = pg.evaluate("() => matriculas.reduce((n,m) => n + m.servicos.length, 0)")
        pg.evaluate("() => resetarFluxo()")
        pg.wait_for_timeout(500)
        texto = avisos[-1] if avisos else ""
        checa("o aviso nao diz mais que e irreversivel",
              "nao pode ser desfeito" not in texto, "\n         texto: " + texto.replace("\n", " | "))
        checa("o aviso explica que as matriculas ficam",
              "continuam na lista" in texto)
        checa("o aviso oferece o caminho de volta", "Ctrl+Z" in texto)
        servicos_depois = pg.evaluate("() => matriculas.reduce((n,m) => n + m.servicos.length, 0)")
        checa("o reset realmente apagou os servicos", servicos_depois == 0,
              "(%d -> %d)" % (servicos_antes, servicos_depois))
        checa("as matriculas continuaram na lista",
              pg.evaluate("() => matriculas.length") == 31,
              "(%d)" % pg.evaluate("() => matriculas.length"))
        pg.evaluate("() => document.activeElement.blur()")
        pg.keyboard.press("Control+z")
        pg.wait_for_timeout(500)
        checa("Ctrl+Z cumpre o que o aviso promete",
              pg.evaluate("() => matriculas.reduce((n,m) => n + m.servicos.length, 0)") == servicos_antes,
              "(%d servicos de volta)" % pg.evaluate("() => matriculas.reduce((n,m) => n + m.servicos.length, 0)"))

        # ---------- 5. rotulo do botao ----------
        print("\n[5] o botao conta a mesma historia")
        pg.evaluate("() => toggleConfig()")
        pg.wait_for_timeout(400)
        rotulo = pg.evaluate("""() => {
            const b = Array.from(document.querySelectorAll('button'))
                .find(x => x.getAttribute('onclick') === 'resetarFluxo()');
            return b ? b.textContent.trim() : '';
        }""")
        checa("o botao nao promete apagar tudo", "Todos os Dados" not in rotulo,
              "(rotulo: %s)" % rotulo)
        checa("o botao diz o que faz", "servicos" in rotulo.lower(), "(rotulo: %s)" % rotulo)
        pg.keyboard.press("Escape")
        pg.wait_for_timeout(300)

        # ---------- 6. nada vazou ----------
        print("\n[6] o pacote continua limpo")
        limpo = pg.evaluate("() => prepararHtmlLimpo()")
        fonte = INDEX.read_text(encoding="utf-8")
        checa("99999999 nao vazou", limpo.count("99999999") <= fonte.count("99999999"),
              "(fonte %d / pacote %d)" % (fonte.count("99999999"), limpo.count("99999999")))
        checa("console sem erro no percurso", len(erros) == 0,
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
