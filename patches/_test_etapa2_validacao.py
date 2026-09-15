# -*- coding: utf-8 -*-
# Validacao dos 3 itens manuais pendentes da Etapa 2 (checklist Fusao):
#   e2g - processar um arquivo na aba 6 e baixar o resultado (navegador real, headless Chromium)
#   e2h - index.html sozinho numa pasta vazia, sem o anonimizador.html do lado
#   e2i - simulacao do fluxo Google Docs -> Bloco de Notas -> renomear .html
# Uso: venv_agente/Scripts/python.exe patches/_test_etapa2_validacao.py
import shutil
import sys
import tempfile
from pathlib import Path

from playwright.sync_api import sync_playwright

RAIZ = Path(__file__).resolve().parent.parent
INDEX = RAIZ / "index.html"
ABAS = ["Calculadora de Prazo", "Calculadora de Dilacao", "Fluxo de Vistorias VTO",
        "Matriculas", "Estatisticas", "Anonimizador"]
falhas = []


def marca(item, ok, detalhe):
    print(("PASS " if ok else "FALHA") + " | " + item + " | " + detalhe)
    if not ok:
        falhas.append(item + ": " + detalhe)


def abre_navegador(p, tmp):
    browser = p.chromium.launch(args=["--allow-file-access-from-files"])
    ctx = browser.new_context(accept_downloads=True)
    pg = ctx.new_page()
    erros = []
    pg.on("pageerror", lambda e: erros.append("pageerror: " + str(e)))
    pg.on("console", lambda m: erros.append("console: " + m.text) if m.type == "error" else None)
    pg.on("dialog", lambda d: (erros.append("dialog: " + d.message), d.dismiss()))
    return browser, pg, erros


def abre_as_seis_abas(pg):
    for nome in ABAS:
        pg.locator("button.tab-btn", has_text=nome).first.click()
        pg.wait_for_timeout(250)


def aba6_ok(pg):
    quadro = pg.locator("#anonimizadorFrame")
    srcdoc = quadro.get_attribute("srcdoc")
    if not srcdoc:
        return False, "srcdoc vazio (Base64 nao decodificou?)"
    try:
        pg.frame_locator("#anonimizadorFrame").locator("#fileInput").wait_for(state="visible", timeout=8000)
    except Exception as e:
        return False, "fileInput nao apareceu dentro do iframe: " + str(e)[:120]
    return True, "iframe com srcdoc e painel de processamento visivel"


def teste_e2h(p, tmp):
    pasta_vazia = tmp / "e2h"
    pasta_vazia.mkdir()
    shutil.copy(INDEX, pasta_vazia / "index.html")
    browser, pg, erros = abre_navegador(p, tmp)
    try:
        pg.goto((pasta_vazia / "index.html").as_uri())
        pg.wait_for_timeout(600)
        abre_as_seis_abas(pg)
        ok_frame, det = aba6_ok(pg)
        crit = [e for e in erros if "favicon" not in e.lower()]
        marca("e2h", ok_frame and not crit,
              det + ("; erros: " + "; ".join(crit[:3]) if crit else ""))
    finally:
        browser.close()


def teste_e2g(p, tmp):
    pasta = tmp / "e2g"
    pasta.mkdir()
    shutil.copy(INDEX, pasta / "index.html")
    csv_teste = pasta / "dados_ficticios.csv"
    csv_teste.write_text(
        "NOME;CPF;ENDERECO;CONSUMO\n"
        "MARIA TESTE SILVA;111.444.777-35;RUA FICTICIA 123;150\n"
        "JOSE TESTE SOUZA;222.555.888-49;AV FICTICIA 456;90\n",
        encoding="utf-8")
    browser, pg, erros = abre_navegador(p, tmp)
    downloads = []
    pg.on("download", lambda d: downloads.append(d))
    try:
        pg.goto((pasta / "index.html").as_uri())
        pg.wait_for_timeout(600)
        pg.locator("button.tab-btn", has_text="Anonimizador").first.click()
        fr = pg.frame_locator("#anonimizadorFrame")
        try:
            fr.locator("#fileInput").set_input_files(str(csv_teste))
        except Exception as e:
            marca("e2g", False, "nao consegui anexar o arquivo: " + str(e)[:150])
            return
        try:
            pg.wait_for_function(
                """() => {
                    const f = document.getElementById('anonimizadorFrame');
                    const d = f && f.contentDocument;
                    const b = d && d.getElementById('btnProcess');
                    return b && !b.disabled;
                }""", timeout=15000)
        except Exception:
            marca("e2g", False, "botao Processar nao habilitou apos anexar o arquivo")
            return
        # destino "Downloads (Padrao)": o modo "picker" abre seletor de pasta,
        # que em headless reprova como AbortError e encerra o lote sem baixar nada
        try:
            fr.locator('input[name="saveMode"][value="auto"]').check()
        except Exception as e:
            marca("e2g", False, "radio saveMode=auto nao encontrado: " + str(e)[:120])
            return
        fr.locator("#btnProcess").click()
        pg.wait_for_timeout(4000)
        if not downloads:
            try:
                logtxt = fr.locator("#logConsole").inner_text()
            except Exception:
                logtxt = "(log inacessivel)"
            marca("e2g", False, "nenhum download disparou apos Processar | log: " + logtxt[-300:].replace(chr(10), " / "))
            return
        baixados = []
        vazou = False
        for d in downloads:
            destino = pasta / d.suggested_filename
            d.save_as(str(destino))
            conteudo = destino.read_text(encoding="utf-8", errors="replace")
            baixados.append(d.suggested_filename + " (" + str(len(conteudo)) + " chars)")
            if "MARIA TESTE SILVA" in conteudo or "111.444.777-35" in conteudo:
                vazou = True
        marca("e2g", not vazou,
              "baixados: " + ", ".join(baixados) + ("; DADO ORIGINAL VAZOU no resultado" if vazou else "; originais ausentes no resultado"))
    finally:
        browser.close()


def teste_e2i(p, tmp):
    fonte = INDEX.read_text(encoding="utf-8")
    # Cenario A: Bloco de Notas salvando em UTF-8 (padrao do Win10+), CRLF
    utf8_crlf = "\r\n".join(fonte.splitlines())
    # Cenario B: Bloco de Notas em ANSI (Windows-1252) — pior caso de encoding
    ansi = utf8_crlf.encode("cp1252", errors="replace")
    variantes = [("utf8-crlf", utf8_crlf.encode("utf-8")),
                 ("ansi-cp1252", ansi)]
    for nome, dados in variantes:
        pasta = tmp / ("e2i-" + nome)
        pasta.mkdir()
        (pasta / "index.html").write_bytes(dados)
        browser, pg, erros = abre_navegador(p, tmp)
        try:
            pg.goto((pasta / "index.html").as_uri())
            pg.wait_for_timeout(600)
            abre_as_seis_abas(pg)
            ok_frame, det = aba6_ok(pg)
            crit = [e for e in erros if "favicon" not in e.lower()]
            marca("e2i/" + nome, ok_frame and not crit,
                  det + ("; erros: " + "; ".join(crit[:3]) if crit else ""))
        finally:
            browser.close()


def main():
    with tempfile.TemporaryDirectory(prefix="vto_e2_") as t:
        tmp = Path(t)
        with sync_playwright() as p:
            teste_e2h(p, tmp)
            teste_e2g(p, tmp)
            teste_e2i(p, tmp)
    print("-" * 60)
    if falhas:
        print(str(len(falhas)) + " FALHA(S): " + "; ".join(falhas))
        sys.exit(1)
    print("TODOS OS TESTES PASSARAM (e2g, e2h, e2i)")


if __name__ == "__main__":
    main()
