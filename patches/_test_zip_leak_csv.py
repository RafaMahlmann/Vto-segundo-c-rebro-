# -*- coding: utf-8 -*-
# Responde: dados de CSV carregados no app (biblioteca de matriculas) vao junto no ZIP?
# Cenario: importa CSV com matricula-armadilha 99900011, exporta o ZIP e procura
# a armadilha dentro do index.html exportado. Esperado: ZERO ocorrencias.
# Uso: venv_agente/Scripts/python.exe patches/_test_zip_leak_csv.py
import shutil
import sys
import tempfile
import zipfile
from pathlib import Path

from playwright.sync_api import sync_playwright

RAIZ = Path(__file__).resolve().parent.parent
INDEX = RAIZ / "index.html"
ARMADILHA = "99900011"


def main():
    with tempfile.TemporaryDirectory(prefix="vto_leak_") as t:
        tmp = Path(t)
        shutil.copy(INDEX, tmp / "index.html")
        csv_teste = tmp / "biblioteca.csv"
        csv_teste.write_text(
            "Matricula;Servico;Data_Criacao;Data_Baixa\n"
            f"{ARMADILHA};8403;2026-01-10;\n"
            f"{ARMADILHA};8405;2026-03-05;2026-04-01\n",
            encoding="utf-8")

        with sync_playwright() as p:
            browser = p.chromium.launch(args=["--allow-file-access-from-files"])
            ctx = browser.new_context(accept_downloads=True)
            pg = ctx.new_page()
            erros = []
            pg.on("pageerror", lambda e: erros.append(str(e)))
            pg.on("console", lambda m: erros.append(m.text) if m.type == "error" else None)
            pg.on("dialog", lambda d: d.accept() if d.type == "confirm" else d.dismiss())
            pg.goto((tmp / "index.html").as_uri())
            pg.wait_for_timeout(600)

            # 1. vai ate a aba Matriculas (botao de importar fica escondido fora dela)
            pg.locator("button.tab-btn", has_text="Matriculas").first.click()
            pg.wait_for_timeout(400)

            # 2. importa a "biblioteca" CSV
            with pg.expect_file_chooser() as fc:
                pg.locator("button", has_text="Importar CSV").first.click()
            fc.value.set_files(str(csv_teste))
            pg.wait_for_timeout(800)
            na_tela = pg.evaluate("() => matriculas.some(m => m.numero === '" + ARMADILHA + "')")
            print("PASS | dado-carregado | armadilha na tela do app:", na_tela)
            if not na_tela:
                print("FALHA | nao conseguiu importar o CSV de teste")
                sys.exit(1)

            # 3. Copiar o VTO em ZIP (sem o "Salvar como", que no navegador de
            #    teste fica esperando uma janela que nunca aparece)
            downloads = []
            pg.on("download", lambda d: downloads.append(d))
            pg.evaluate("() => { window.showSaveFilePicker = undefined; }")
            pg.locator("button.btn-zip").first.click()
            pg.wait_for_timeout(300)
            pg.locator("#copiaOpZip").click()
            pg.wait_for_timeout(2500)
            if not downloads:
                print("FALHA | nenhum ZIP baixou")
                sys.exit(1)
            zip_path = tmp / downloads[0].suggested_filename
            downloads[0].save_as(str(zip_path))

            # 3. procura a armadilha dentro do pacote exportado
            extraido = tmp / "extraido"
            with zipfile.ZipFile(zip_path) as z:
                nomes = z.namelist()
                z.extractall(extraido)
            contagem = 0
            for nome in nomes:
                conteudo = (extraido / nome).read_text(encoding="utf-8", errors="replace")
                contagem += conteudo.count(ARMADILHA)
            print(("PASS" if contagem == 0 else "FALHA") +
                  f" | vazamento | {ARMADILHA} aparece {contagem}x no ZIP exportado")
            print("INFO | pacote contem:", ", ".join(nomes))

            # 4. abre o exportado e ve se nasce limpo (so mock)
            pg2 = ctx.new_page()
            pg2.on("dialog", lambda d: d.dismiss())
            pg2.goto((extraido / nomes[0]).as_uri())
            pg.wait_for_timeout(600)
            tem_armadilha = pg2.evaluate("() => matriculas.some(m => m.numero === '" + ARMADILHA + "')")
            n_mock = pg2.evaluate("() => matriculas.length")
            print(("PASS" if not tem_armadilha else "FALHA") +
                  f" | exportado-limpo | ao reabrir: {n_mock} matriculas (mock), armadilha ausente: {not tem_armadilha}")
            crit = [e for e in erros if "favicon" not in e.lower()]
            print(("PASS" if not crit else "FALHA") + " | console | zero erros" if not crit else " | console | " + "; ".join(crit[:3]))
            browser.close()

            if contagem == 0 and not tem_armadilha and not crit:
                print("-" * 60)
                print("RESPOSTA: NAO vai junto. O ZIP sai sem os dados da tela.")
                sys.exit(0)
            sys.exit(1)


if __name__ == "__main__":
    main()
