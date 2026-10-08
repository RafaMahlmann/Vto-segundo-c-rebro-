# Checklist do pontinho de ajuda do Exportar ZIP - AGENTS.md secao 6
import asyncio, pathlib
from playwright.async_api import async_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
PRINTS = ROOT / "propostas" / "2026-10-07" / "prints"
PRINTS.mkdir(parents=True, exist_ok=True)

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width": 1280, "height": 900})
        erros = []
        page.on("console", lambda m: erros.append(m.text) if m.type == "error" else None)
        page.on("pageerror", lambda e: erros.append(str(e)))

        await page.goto((ROOT / "index.html").as_uri())
        await page.wait_for_timeout(1500)

        # 1. console limpo
        print("1) erros no load:", erros if erros else "ZERO")

        # 2. pontinho visivel ao lado do Exportar ZIP
        vis = await page.locator(".btn-zip-info").is_visible()
        print("2) pontinho ? visivel no header:", "OK" if vis else "PROBLEMA")

        # 3. clique abre o modal com a explicacao
        await page.click(".btn-zip-info")
        await page.wait_for_timeout(500)
        aberto = await page.locator("#modalOverlay.ativo").count()
        texto = await page.locator("#modalOverlay .modal-box").text_content()
        tem_titulo = "Para que serve o Exportar ZIP?" in texto
        tem_compartilhar = "compartilhar com um colega" in texto
        tem_limpo = "sai limpo" in texto
        print("3) modal abre:", "OK" if aberto else "PROBLEMA")
        print("3b) texto completo:", "OK" if tem_titulo and tem_compartilhar and tem_limpo else "PROBLEMA")
        await page.screenshot(path=str(PRINTS / "11_ajuda_zip.png"))

        # 4. Esc fecha e restaura o modal original
        await page.keyboard.press("Escape")
        await page.wait_for_timeout(400)
        fechou = await page.locator("#modalOverlay.ativo").count()
        print("4) Esc fecha:", "OK" if not fechou else "PROBLEMA")

        # 5. ajuda antiga continua funcionando
        await page.click("#btnAjuda")
        await page.wait_for_timeout(400)
        txt_ajuda = await page.locator("#modalOverlay .modal-box").text_content()
        print("5) ajuda antiga intacta:", "OK" if "Ajuda Rápida" in txt_ajuda else "PROBLEMA")
        await page.keyboard.press("Escape")
        await page.wait_for_timeout(300)

        # 6. export limpo mesmo com o modal de ajuda zip aberto
        sujo = await page.evaluate("""(() => {
            abrirAjudaZip();
            const html = prepararHtmlLimpo();
            const m = html.match(/<div[^>]*id="modalOverlay"[^>]*>/);
            const tag = m ? m[0] : 'NAO ACHOU';
            fecharModalAjuda();
            return tag;
        })()""")
        print(f"6) export: tag do overlay = {sujo}", "OK" if "ativo" not in sujo else "PROBLEMA")

        # 7. celular 375px sem quebrar
        await page.set_viewport_size({"width": 375, "height": 800})
        await page.reload(); await page.wait_for_timeout(1200)
        medidas = await page.evaluate("({sw: document.documentElement.scrollWidth, iw: innerWidth})")
        vis_m = await page.locator(".btn-zip-info").is_visible()
        print(f"7) celular 375px: {'OK' if medidas['sw'] <= medidas['iw'] + 1 and vis_m else 'PROBLEMA'} (scrollWidth={medidas['sw']})")

        print("ERROS FINAIS:", erros if erros else "ZERO")
        await browser.close()

asyncio.run(main())
