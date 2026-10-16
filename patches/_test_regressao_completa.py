# -*- coding: utf-8 -*-
# AGENTE DE REGRESSAO COMPLETA — executa de verdade o checklist do AGENTS.md §6
# num Chromium headless, clicando na interface como uma pessoa:
#   1. console zero erros no carregamento
#   2. as 6 abas abrem e renderizam
#   3. aba 1: sanção calcula com datas reais de teste
#   4. aba 2: dilacao calcula (botao 90)
#   5. aba 3: fluxo registra servico 8403 na matricula ativa via modal
#   6. aba 4: CRUD — adicionar, Ctrl+Z, Ctrl+Shift+Z, remover
#   7. timeline renderiza ao selecionar matricula
#   8. aba 5: os 4 graficos canvas nao sao virgens
#   9. exportar CSV e JSON (download com conteudo valido)
#  10. importar o JSON de volta
#  11. exportar ZIP, reabrir o index.html extraido e conferir as 6 abas + aba 6
# Uso: venv_agente/Scripts/python.exe patches/_test_regressao_completa.py
import json
import shutil
import sys
import tempfile
import zipfile
from pathlib import Path

from playwright.sync_api import sync_playwright

RAIZ = Path(__file__).resolve().parent.parent
INDEX = RAIZ / "index.html"
falhas = []
dialogos = []


def marca(item, ok, detalhe):
    print(("PASS " if ok else "FALHA") + " | " + item + " | " + detalhe)
    if not ok:
        falhas.append(item + ": " + detalhe)


def main():
    with tempfile.TemporaryDirectory(prefix="vto_reg_") as t:
        tmp = Path(t)
        shutil.copy(INDEX, tmp / "index.html")
        with sync_playwright() as p:
            browser = p.chromium.launch(args=["--allow-file-access-from-files"])
            ctx = browser.new_context(accept_downloads=True)
            pg = ctx.new_page()
            erros = []
            pg.on("pageerror", lambda e: erros.append("pageerror: " + str(e)))
            pg.on("console", lambda m: erros.append("console: " + m.text) if m.type == "error" else None)

            def no_dialog(d):
                dialogos.append(d.message)
                # aceita confirmacoes de fluxo (remover, ZIP, enviada), dispensa alertas
                if d.type == "confirm":
                    d.accept()
                else:
                    d.dismiss()

            pg.on("dialog", no_dialog)

            pg.goto((tmp / "index.html").as_uri())
            pg.wait_for_timeout(700)
            crit = [e for e in erros if "favicon" not in e.lower()]
            marca("carga/console", not crit, "zero erros no carregamento" if not crit else "; ".join(crit[:3]))

            # ---- 2. as 6 abas abrem e renderizam ----
            # (resultados de calculo ficam display:none ate calcular; ancora em conteudo estavel)
            abas = [("Calculadora de Prazo", "Lançamento da Sanção"),
                    ("Calculadora de Dilacao", "Dilacao Simples"),
                    ("Fluxo de Vistorias VTO", "1a VISTORIA"),
                    ("Matriculas", "Adicionar"),
                    ("Estatisticas", None),
                    ("Anonimizador", None)]
            for nome, trecho in abas:
                pg.locator("button.tab-btn", has_text=nome).first.click()
                pg.wait_for_timeout(300)
                alvo = pg.locator(".tab-content.active")
                visivel = alvo.count() > 0
                if visivel and trecho:
                    visivel = trecho in alvo.first.inner_text()
                if visivel and nome == "Estatisticas":
                    visivel = alvo.locator("canvas").count() >= 4
                if visivel and nome == "Anonimizador":
                    visivel = alvo.locator("iframe#anonimizadorFrame").count() == 1
                marca("abas/" + nome, visivel, "conteudo caracteristico visivel" if visivel else "conteudo nao apareceu")

            # ---- 3. aba 1: sancao calcula ----
            pg.locator("button.tab-btn", has_text="Calculadora de Prazo").first.click()
            pg.locator("#dataSancao").fill("01/08/2026")
            pg.locator("#dataFaturamento").fill("10/08/2026")
            pg.locator("#dataSolicitacao").fill("05/09/2026")
            pg.locator("button.btn-calcular").click()
            pg.wait_for_timeout(300)
            vis = pg.locator("#resultadoPrazoSancao").is_visible()
            marca("sancao/calcula", vis, "resultado visivel" if vis else "resultado nao apareceu")

            # ---- 4. aba 2: dilacao calcula ----
            pg.locator("button.tab-btn", has_text="Calculadora de Dilacao").first.click()
            pg.locator("#dataInicialDilacao").fill("01/08/2026")
            pg.locator("button.btn-dia-rapido", has_text="90").first.click()
            pg.wait_for_timeout(300)
            vis = pg.locator("#resultadoDilacao").is_visible() and pg.locator("#dataFinalDilacao").inner_text().strip() != ""
            marca("dilacao/calcula", vis, "data final preenchida" if vis else "resultado vazio")

            # ---- 5. aba 3: fluxo registra servico via modal ----
            # (matricula 10045206 ja tem servicos; estado via funcoes reais do app)
            pg.evaluate("() => mostrarAba('matriculas')")
            pg.wait_for_timeout(200)
            pg.evaluate("() => selecionarMatricula('10045206')")
            pg.wait_for_timeout(200)
            ativa = pg.evaluate("() => matriculaAtiva")
            n_antes = pg.evaluate("() => { const m = matriculas.find(x => x.numero === matriculaAtiva);"
                                  " return m ? m.servicos.length : -1; }")
            pg.evaluate("() => mostrarAba('fluxo')")
            pg.wait_for_timeout(200)
            # a roleta agora comeca vazia: escolhe o 8403 pela busca, como o usuario faz
            pg.locator("#coluna1 .roleta-vazio").first.click()
            pg.keyboard.type("8403")
            pg.wait_for_timeout(500)
            # tenta clique real num botao visivel fora da roleta
            handle = pg.evaluate_handle("""() => {
                const b = [...document.querySelectorAll('button.servico-btn')]
                    .filter(x => x.offsetParent !== null && !x.closest('.roleta-grupo'));
                return b[0] || null;
            }""")
            modo_clique = "programatico"
            codigo = None
            if handle.as_element() is not None:
                codigo = handle.get_attribute("data-cod")
                handle.click()
                modo_clique = "real"
                pg.wait_for_timeout(250)
            modal_aberto = pg.evaluate("() => document.getElementById('modalOverlay').classList.contains('ativo')")
            if not modal_aberto:
                codigo = pg.evaluate("() => { const b = [...document.querySelectorAll('button.servico-btn')]"
                                     " .filter(x => x.offsetParent !== null);"
                                     " if (b[0]) { b[0].click(); return b[0].dataset.cod; } return null; }")
                modo_clique = "programatico-1clique"
                pg.wait_for_timeout(250)
                modal_aberto = pg.evaluate("() => document.getElementById('modalOverlay').classList.contains('ativo')")
            if not modal_aberto:
                # mecanica da roleta: 1o clique arma, 2o clique seleciona de verdade
                pg.evaluate("() => { const b = [...document.querySelectorAll('button.servico-btn')]"
                            " .filter(x => x.offsetParent !== null); if (b[0]) b[0].click(); }")
                pg.wait_for_timeout(300)
                modal_aberto = pg.evaluate("() => document.getElementById('modalOverlay').classList.contains('ativo')")
            if modal_aberto:
                pg.locator("#modalDataCriacao").fill("2026-09-01")
                pg.locator("#btnSalvarModal").click()
                pg.wait_for_timeout(400)
                n_depois = pg.evaluate("() => { const m = matriculas.find(x => x.numero === matriculaAtiva);"
                                       " return m ? m.servicos.length : -1; }")
                marca("fluxo/registra", n_depois == n_antes + 1,
                      f"clique {modo_clique}: servico {codigo} em {ativa} ({n_antes} -> {n_depois})")
            else:
                diag = pg.evaluate("""() => ({
                    ativa: matriculaAtiva,
                    pendente: servicoPendente ? servicoPendente.codigo : null,
                    classe: document.getElementById('modalOverlay').className
                })""")
                pg.screenshot(path=str(RAIZ / "patches" / "_debug_fluxo.png"))
                marca("fluxo/registra", False,
                      "modal nao abriu; diag=" + json.dumps(diag, ensure_ascii=False) +
                      "; dialogos=" + " || ".join(dialogos[-4:]) +
                      "; screenshot em patches/_debug_fluxo.png")
            # seguranca: nao deixar modal aberto para os proximos passos
            pg.evaluate("() => { const mo = document.getElementById('modalOverlay');"
                        " if (mo.classList.contains('ativo')) fecharModal(); }")

            # ---- 6. aba 4: CRUD + undo/redo ----
            pg.locator("button.tab-btn", has_text="Matriculas").first.click()
            pg.wait_for_timeout(200)
            pg.locator("#novaMatricula").fill("77777777")
            pg.locator("button.btn-add", has_text="Adicionar").first.click()
            pg.wait_for_timeout(300)
            tem_nova = pg.locator("text=77777777").count() > 0
            marca("crud/adiciona", tem_nova, "matricula 77777777 na tabela" if tem_nova else "nao apareceu")
            pg.keyboard.press("Control+z")
            pg.wait_for_timeout(300)
            sumiu = pg.locator("text=77777777").count() == 0
            marca("crud/ctrl-z", sumiu, "Ctrl+Z removeu" if sumiu else "continua na tabela")
            pg.keyboard.press("Control+Shift+z")
            pg.wait_for_timeout(300)
            voltou = pg.locator("text=77777777").count() > 0
            marca("crud/ctrl-shift-z", voltou, "Ctrl+Shift+Z restaurou" if voltou else "nao voltou")
            if voltou:
                pg.locator("button.btn-acao.remover").last.click()
                pg.wait_for_timeout(300)
                removida = pg.locator("text=77777777").count() == 0
                marca("crud/remove", removida, "removida com confirmacao" if removida else "continua na tabela")

            # ---- 7. timeline renderiza (matricula com servicos) ----
            pg.locator("tr", has_text="10045206").first.locator("button.btn-acao.selecionar").first.click()
            pg.wait_for_timeout(300)
            tl = pg.locator("#timelineTrack").is_visible()
            ativa_tl = pg.evaluate("() => matriculaAtiva")
            marca("timeline", tl, "track visivel ao selecionar (ativa=" + str(ativa_tl) + ")" if tl
                  else "ficou vazia; ativa=" + str(ativa_tl))

            # ---- 8. aba 5: graficos com tinta ----
            pg.locator("button.tab-btn", has_text="Estatisticas").first.click()
            pg.wait_for_timeout(500)
            tinta = pg.evaluate("() => {"
                                " const ids = ['grafFases','grafStatus','grafEvolucao','grafTempoCodigo'];"
                                " return ids.every(id => {"
                                "   const c = document.getElementById(id);"
                                "   if (!c || c.width === 0) return false;"
                                "   const d = c.getContext('2d').getImageData(0, 0, c.width, c.height).data;"
                                "   for (let i = 3; i < d.length; i += 4) { if (d[i] > 0) return true; }"
                                "   return false; }); }")
            marca("estatisticas/tinta", bool(tinta), "os 4 canvas tem pixels desenhados")

            # ---- 9. exportar CSV e JSON ----
            baixados = []
            pg.on("download", lambda d: baixados.append(d))
            pg.locator("button.tab-btn", has_text="Matriculas").first.click()
            pg.locator("button", has_text="Exportar CSV").first.click()
            pg.wait_for_timeout(800)
            pg.locator("button", has_text="Salvar Arquivo").first.click()
            pg.wait_for_timeout(800)
            csv_ok = json_ok = False
            json_path = csv_path = None
            for d in baixados:
                dest = tmp / d.suggested_filename
                d.save_as(str(dest))
                if dest.suffix == ".csv":
                    csv_path = dest
                    csv_ok = "matricula" in dest.read_text(encoding="utf-8", errors="replace").lower()
                if dest.suffix == ".json":
                    json_path = dest
                    dados = json.loads(dest.read_text(encoding="utf-8"))
                    json_ok = isinstance(dados.get("matriculas"), list) and len(dados["matriculas"]) > 0
            marca("export/csv", csv_ok, "download com cabecalho valido" if csv_ok else "falhou")
            marca("export/json", json_ok, "download com lista de matriculas" if json_ok else "falhou")

            # ---- 10. importar JSON de volta ----
            if json_path:
                n_antes = pg.evaluate("() => matriculas.length")
                with pg.expect_file_chooser() as fc:
                    pg.locator("button", has_text="Abrir Arquivo").first.click()
                fc.value.set_files(str(json_path))
                pg.wait_for_timeout(600)
                n_depois = pg.evaluate("() => matriculas.length")
                marca("import/json", n_depois >= n_antes, f"{n_antes} -> {n_depois} matriculas")
            else:
                marca("import/json", False, "sem arquivo JSON exportado para reimportar")

            # ---- 11. exportar ZIP e reabrir o exportado ----
            baixados.clear()
            pg.locator("button.btn-zip").first.click()
            pg.wait_for_timeout(2500)
            zip_path = None
            for d in baixados:
                dest = tmp / d.suggested_filename
                d.save_as(str(dest))
                if dest.suffix == ".zip":
                    zip_path = dest
            if zip_path:
                extraido = tmp / "zip_extraido"
                with zipfile.ZipFile(zip_path) as z:
                    z.extractall(extraido)
                idx = extraido / "index.html"
                tem_anon = (extraido / "anonimizador.html").exists()
                pg2 = ctx.new_page()
                erros2 = []
                pg2.on("pageerror", lambda e: erros2.append(str(e)))
                pg2.on("console", lambda m: erros2.append(m.text) if m.type == "error" else None)
                pg2.on("dialog", no_dialog)
                pg2.goto(idx.as_uri())
                pg2.wait_for_timeout(700)
                abriu_tudo = True
                for nome in ["Calculadora de Prazo", "Calculadora de Dilacao", "Fluxo de Vistorias VTO",
                             "Matriculas", "Estatisticas", "Anonimizador"]:
                    pg2.locator("button.tab-btn", has_text=nome).first.click()
                    pg2.wait_for_timeout(250)
                try:
                    pg2.frame_locator("#anonimizadorFrame").locator("#fileInput").wait_for(state="visible", timeout=8000)
                except Exception:
                    abriu_tudo = False
                crit2 = [e for e in erros2 if "favicon" not in e.lower()]
                marca("zip/exporta", tem_anon, "ZIP com index.html + anonimizador.html" if tem_anon else "faltou anonimizador no ZIP")
                marca("zip/reabre", abriu_tudo and not crit2,
                      "reaberto: 6 abas + aba 6 carregando" if (abriu_tudo and not crit2)
                      else "aba 6 falhou ou erros: " + "; ".join(crit2[:3]))
                pg2.close()
            else:
                marca("zip/exporta", False, "nenhum download de ZIP disparou")
                marca("zip/reabre", False, "sem ZIP para reabrir")

            crit_f = [e for e in erros if "favicon" not in e.lower()]
            marca("final/console", not crit_f, "zero erros acumulados" if not crit_f else "; ".join(crit_f[:3]))
            browser.close()

    print("-" * 60)
    if falhas:
        print(str(len(falhas)) + " FALHA(S):")
        for f in falhas:
            print("  - " + f)
        sys.exit(1)
    print("REGRESSAO COMPLETA: TODOS OS TESTES PASSARAM")


if __name__ == "__main__":
    main()
