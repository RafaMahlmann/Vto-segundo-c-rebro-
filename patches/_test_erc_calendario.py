# -*- coding: utf-8 -*-
# Validacao do item erc (Etapa R): botao de calendario abre e grava data.
# Fluxo real: clicar no botao 📅 -> cria input[type=date] oculto com showPicker()
# -> ao escolher a data, o campo de texto recebe DD/MM/AAAA.
# Uso: venv_agente/Scripts/python.exe patches/_test_erc_calendario.py
import shutil
import sys
import tempfile
from pathlib import Path

from playwright.sync_api import sync_playwright

RAIZ = Path(__file__).resolve().parent.parent
INDEX = RAIZ / "index.html"
falhas = []


def marca(item, ok, detalhe):
    print(("PASS " if ok else "FALHA") + " | " + item + " | " + detalhe)
    if not ok:
        falhas.append(item + ": " + detalhe)


def main():
    with tempfile.TemporaryDirectory(prefix="vto_erc_") as t:
        tmp = Path(t)
        shutil.copy(INDEX, tmp / "index.html")
        with sync_playwright() as p:
            browser = p.chromium.launch(args=["--allow-file-access-from-files"])
            pg = browser.new_context().new_page()
            erros = []
            pg.on("pageerror", lambda e: erros.append("pageerror: " + str(e)))
            pg.on("console", lambda m: erros.append("console: " + m.text) if m.type == "error" else None)
            pg.on("dialog", lambda d: (erros.append("dialog: " + d.message), d.dismiss()))
            pg.goto((tmp / "index.html").as_uri())
            pg.wait_for_timeout(500)
            # aba 1 (Calculadora de Prazo) ja e a ativa; o primeiro 📅 e o de dataSancao
            pg.locator("button.btn-calendario").first.click()
            pg.wait_for_timeout(300)

            # 1) o calendario abriu: um input[type=date] foi criado fora da tela
            fake = pg.locator("input[type='date']:not(#modalDataCriacao):not(#modalDataBaixa)")
            marca("erc/abre", fake.count() >= 1,
                  "input[type=date] criado ao clicar no botao" if fake.count() >= 1
                  else "nenhum input[type=date] apareceu apos o clique")

            # 2) escolher data grava no campo de texto em DD/MM/AAAA
            if fake.count() >= 1:
                fake.first.fill("2026-09-15")
                pg.evaluate("() => { const f = document.querySelector(\"body > input[type='date']\");"
                            " if (f) f.dispatchEvent(new Event('change', { bubbles: true })); }")
                pg.wait_for_timeout(300)
                valor = pg.locator("#dataSancao").input_value()
                marca("erc/grava", valor == "15/09/2026",
                      "dataSancao = " + repr(valor) + " (esperado '15/09/2026')")
                # o fake some depois do change
                sobra = pg.locator("body > input[type='date']").count()
                marca("erc/limpa", sobra == 0, "input oculto removido apos escolher" if sobra == 0
                      else str(sobra) + " input(s) oculto(s) sobrando")

            # 3) ida e volta: data ja digitada no texto preenche o calendario
            pg.locator("#dataFaturamento").fill("10/08/2026")
            botoes = pg.locator("button.btn-calendario")
            botoes.nth(1).click()
            pg.wait_for_timeout(300)
            fake2 = pg.locator("body > input[type='date']")
            if fake2.count() >= 1:
                preenchido = fake2.first.input_value()
                marca("erc/prefill", preenchido == "2026-08-10",
                      "calendario abriu preenchido com " + repr(preenchido) + " (esperado '2026-08-10')")
                fake2.first.dispatch_event("change")
            else:
                marca("erc/prefill", False, "input[type=date] nao apareceu para dataFaturamento")

            crit = [e for e in erros if "favicon" not in e.lower()]
            marca("erc/console", not crit, "zero erros de console" if not crit else "; ".join(crit[:3]))
            browser.close()
    print("-" * 60)
    if falhas:
        print(str(len(falhas)) + " FALHA(S): " + "; ".join(falhas))
        sys.exit(1)
    print("TESTE DO CALENDARIO PASSOU (erc)")


if __name__ == "__main__":
    main()
