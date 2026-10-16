# Prints das demos atualizadas (C1 calculadora 180 em 2 estados, S1 seletor)
import asyncio, pathlib
from playwright.async_api import async_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
ALVO = (ROOT / "propostas" / "2026-10-07" / "apresentacao.html").as_uri()
PRINTS = ROOT / "propostas" / "2026-10-07" / "prints"

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width": 1280, "height": 900})
        erros = []
        page.on("pageerror", lambda e: erros.append(str(e)))
        await page.goto(ALVO)
        await page.wait_for_timeout(1200)

        # C1: abre a folha e testa o atalho "há 130 dias" (faixa verde/laranja)
        c1 = page.locator("#c1")
        await c1.scroll_into_view_if_needed()
        await page.wait_for_timeout(600)
        await c1.locator("button", has_text="130").first.click()
        await page.wait_for_timeout(1200)
        await page.screenshot(path=str(PRINTS / "02_calc180_no_prazo.png"))
        print("print ok: 02_calc180_no_prazo")

        # C1: atalho "há 200 dias" (estourado, vermelho)
        await c1.locator("button", has_text="200").first.click()
        await page.wait_for_timeout(1200)
        await page.screenshot(path=str(PRINTS / "03_calc180_expirado.png"))
        print("print ok: 03_calc180_expirado")

        print("ERROS:", erros if erros else "nenhum")
        await browser.close()

asyncio.run(main())
