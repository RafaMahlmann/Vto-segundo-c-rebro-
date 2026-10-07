# Checklist da Fase 1 (Calculadora 180) - AGENTS.md secao 6
import asyncio, pathlib, subprocess, time, socket
from playwright.async_api import async_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
PRINTS = ROOT / "propostas" / "2026-10-07" / "prints"
PRINTS.mkdir(parents=True, exist_ok=True)
PORTA = 8645

async def main():
    # o app e feito para rodar de arquivo (duplo clique) - testamos assim mesmo
    srv = None
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch()
            page = await browser.new_page(viewport={"width": 1280, "height": 900})
            erros = []
            page.on("console", lambda m: erros.append(m.text) if m.type == "error" else None)
            page.on("pageerror", lambda e: erros.append(str(e)))

            await page.goto((ROOT / "index.html").as_uri())
            await page.wait_for_timeout(1500)

            # 1. console limpo no load
            print("1) erros no load:", erros if erros else "ZERO")

            # 2. as 6 abas abrem e renderizam
            abas = {"prazo": "#resultadoPrazoSancao, .calc-wrap", "dilacao": "#resultadoDilacao, .secao-dilacao",
                    "fluxo": "#fluxoContainer", "matriculas": "#listaMatriculas",
                    "estatisticas": ".estat-resumo-grid", "anonimizador": "#anonimizadorFrame, #aba-anonimizador"}
            for aba, sel in abas.items():
                await page.click(f".tab-btn[onclick*=\"mostrarAba('{aba}')\"]")
                await page.wait_for_timeout(400)
                visivel = await page.locator(f"#aba-{aba}").first.is_visible()
                tem = await page.locator(sel).first.count()
                print(f"2) aba {aba}: {'OK' if visivel and tem else 'PROBLEMA'}")

            # 3. FAB so aparece em fluxo/matriculas
            await page.click(".tab-btn[onclick*=\"mostrarAba('prazo')\"]"); await page.wait_for_timeout(300)
            fab_prazo = await page.locator("#calc180Fab").is_visible()
            await page.click(".tab-btn[onclick*=\"mostrarAba('fluxo')\"]"); await page.wait_for_timeout(300)
            fab_fluxo = await page.locator("#calc180Fab").is_visible()
            print(f"3) FAB escondido na aba Prazo: {'OK' if not fab_prazo else 'PROBLEMA'} | visivel no Fluxo: {'OK' if fab_fluxo else 'PROBLEMA'}")

            # 4. abre a folha e testa as 3 faixas + estouro
            await page.click("#calc180Fab"); await page.wait_for_timeout(700)
            folha_aberta = await page.locator("#calc180Folha.aberta").count()
            print("4) folha abre:", "OK" if folha_aberta else "PROBLEMA")

            casos = [("2026-09-07", "ok", "30", "150"), ("2026-05-30", "alerta", "130", "50"), ("2026-03-21", "estourado", "200", "0")]
            for data, faixa, corridos, restantes in casos:
                await page.fill("#calc180Data", data)
                await page.wait_for_timeout(800)
                cls = await page.locator("#calc180Painel").get_attribute("class")
                n_corr = await page.locator("#calc180Corridos").text_content()
                n_rest = await page.locator("#calc180Restantes").text_content()
                msg = await page.locator("#calc180Msg").text_content()
                ok = faixa in (cls or "") and n_corr == corridos and n_rest == restantes
                print(f"4) {data}: faixa={faixa} {'OK' if ok else 'PROBLEMA cls=' + str(cls) + ' ' + n_corr + '/' + n_rest} | msg: {msg}")
                if faixa == "estourado":
                    await page.screenshot(path=str(PRINTS / "05_app_calc180_estourado.png"))
                if faixa == "alerta":
                    await page.screenshot(path=str(PRINTS / "06_app_calc180_alerta.png"))

            # 4b. O BUG DO RAFA: edicao no meio da data (03/02/2026 -> 03/06/2026)
            await page.fill("#calc180Data", "2026-02-03")
            await page.wait_for_timeout(600)
            await page.click("#calc180Data")          # foca o segmento do dia
            await page.keyboard.press("ArrowRight")   # vai para o mes
            await page.keyboard.type("06", delay=60)  # troca 02 por 06
            await page.wait_for_timeout(800)
            n_meio = await page.locator("#calc180Corridos").text_content()
            cls_meio = await page.locator("#calc180Painel").get_attribute("class")
            print(f"4b) edicao no meio (02->06): corridos={n_meio} {'OK' if n_meio == '126' and 'alerta' in (cls_meio or '') else 'PROBLEMA'}")

            # 5. Esc fecha a folha
            await page.keyboard.press("Escape"); await page.wait_for_timeout(500)
            folha_fechou = await page.locator("#calc180Folha.aberta").count()
            print("5) Esc fecha a folha:", "OK" if not folha_fechou else "PROBLEMA")

            # 5b. nota some quando a data muda na mao
            await page.click("#calc180Fab"); await page.wait_for_timeout(700)
            await page.fill("#calc180Data", "2026-09-10")
            await page.wait_for_timeout(800)
            n_cal = await page.locator("#calc180Corridos").text_content()
            nota_vis = await page.locator("#calc180Nota").is_visible()
            print(f"5b) recalculo ao trocar data: {'OK' if n_cal == '27' else 'PROBLEMA (' + str(n_cal) + ')'} | nota some apos troca: {'OK' if not nota_vis else 'PROBLEMA'}")
            await page.keyboard.press("Escape"); await page.wait_for_timeout(500)
            overlay_aberto = await page.locator("#calc180Overlay.aberto").count()
            print("5c) folha+overlay fecham:", "OK" if not overlay_aberto else "PROBLEMA")

            # 6. mock + matricula ativa -> preenchimento automatico
            await page.evaluate("gerarMockData()")
            await page.wait_for_timeout(500)
            await page.click(".tab-btn[onclick*=\"mostrarAba('matriculas')\"]"); await page.wait_for_timeout(500)
            await page.locator("#listaMatriculas tr").nth(1).click(); await page.wait_for_timeout(600)
            # 7. timeline renderizou?
            eventos = await page.locator("#timelineTrack .timeline-evento").count()
            print("7) timeline renderiza ao clicar na matricula:", "OK" if eventos > 0 else "PROBLEMA")
            # FAB na aba matriculas + prefill
            await page.click("#calc180Fab"); await page.wait_for_timeout(800)
            nota = await page.locator("#calc180Nota").text_content()
            nota_visivel = await page.locator("#calc180Nota").is_visible()
            campo = await page.locator("#calc180Data").input_value()
            print(f"6) prefill da matricula ativa: {'OK' if nota_visivel and campo else 'PROBLEMA'} | data={campo} | nota={nota.strip()[:60]}")
            await page.screenshot(path=str(PRINTS / "07_app_calc180_prefill.png"))
            await page.keyboard.press("Escape"); await page.wait_for_timeout(400)

            # 8. undo/redo continuam funcionando
            await page.fill("#novaMatricula", "99999999")
            await page.click("button.btn-add:has-text('+ Adicionar')"); await page.wait_for_timeout(400)
            total_antes = await page.locator("#resTotal").text_content()
            await page.keyboard.press("Control+z"); await page.wait_for_timeout(400)
            total_depois = await page.locator("#resTotal").text_content()
            await page.keyboard.press("Control+Shift+z"); await page.wait_for_timeout(400)
            total_refeito = await page.locator("#resTotal").text_content()
            print(f"8) undo/redo: {total_antes} -> {total_depois} -> {total_refeito}", "OK" if total_depois != total_antes and total_refeito == total_antes else "PROBLEMA")

            # 9. export limpo (plano B do prepararHtmlLimpo, sem o retrato)
            sujo = await page.evaluate("""(() => {
                delete window._htmlOriginal;
                abrirCalc180();
                document.getElementById('calc180Data').value = '2026-05-30';
                calc180Atualizar();
                const notaTxt = document.getElementById('calc180Nota').textContent;
                const html = prepararHtmlLimpo();
                const temFolha = html.includes('calc180Folha');
                const aberta = html.includes('calc180-folha aberta');
                const valorVazado = html.includes('2026-05-30');
                // a nota RENDERIZADA (com o numero da matricula) nao pode vazar;
                // o texto-fonte do script tem so o trecho estatico, sem numero
                const notaVazada = notaTxt.length > 5 && html.includes(notaTxt);
                fecharCalc180();
                return { temFolha, aberta, valorVazado, notaVazada };
            })()""")
            limpo = sujo["temFolha"] and not sujo["aberta"] and not sujo["valorVazado"] and not sujo["notaVazada"]
            print(f"9) export limpo (plano B): {'OK' if limpo else 'PROBLEMA ' + str(sujo)}")

            # 10. celular 375px
            await page.set_viewport_size({"width": 375, "height": 800})
            await page.reload(); await page.wait_for_timeout(1200)
            medidas = await page.evaluate("({sw: document.documentElement.scrollWidth, iw: innerWidth})")
            print(f"10) celular 375px: scrollWidth={medidas['sw']} innerWidth={medidas['iw']}", "OK" if medidas["sw"] <= medidas["iw"] + 1 else "PROBLEMA")

            print("ERROS FINAIS:", erros if erros else "ZERO")
            await browser.close()
    finally:
        if srv: srv.terminate()

asyncio.run(main())
