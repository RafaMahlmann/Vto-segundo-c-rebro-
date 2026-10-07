# Teste automatizado da apresentacao de propostas (uso temporario)
# Abre o arquivo, clica em tudo em rodadas, mede erros e tira prints.
import asyncio, pathlib, sys
from playwright.async_api import async_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
ALVO = (ROOT / "propostas" / "2026-10-07" / "apresentacao.html").as_uri()
PRINTS = ROOT / "propostas" / "2026-10-07" / "prints"
PRINTS.mkdir(parents=True, exist_ok=True)

LOOP_JS = """
window._errs = [];
addEventListener('error', e => _errs.push(e.message + ' @' + e.lineno));
addEventListener('unhandledrejection', e => _errs.push(String(e.reason)));
window._res = { fim: false, rodadas: [] };
(async () => {
  const vistos = new Set();
  for (let k = 0; k < 5; k++) {
    const bs = [...document.querySelectorAll('button,[role="button"],[tabindex="0"]')]
      .filter(b => b.isConnected && !b.disabled && b.offsetParent !== null);
    let novos = 0;
    for (const b of bs) {
      const ch = b.textContent.trim().slice(0, 30) + '|' + (b.closest('section')?.id || '');
      if (vistos.has(ch)) continue;
      vistos.add(ch); novos++;
      b.dispatchEvent(new PointerEvent('pointerdown', { bubbles: true, button: 0 }));
      if (/segure/i.test(b.textContent)) await new Promise(r => setTimeout(r, 1600));
      b.dispatchEvent(new PointerEvent('pointerup', { bubbles: true, button: 0 }));
      b.click();
      await new Promise(r => setTimeout(r, 200));
    }
    _res.rodadas.push(novos);
    await new Promise(r => setTimeout(r, 800));
  }
  _res.vistos = vistos.size;
  _res.fim = true;
})();
"""

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width": 1280, "height": 900})
        console_erros = []
        page.on("console", lambda m: console_erros.append(m.text) if m.type == "error" else None)
        page.on("pageerror", lambda e: console_erros.append(str(e)))

        await page.goto(ALVO)
        await page.wait_for_timeout(1200)

        # print da capa
        await page.screenshot(path=str(PRINTS / "01_capa.png"))

        # laço de cliques em rodadas
        await page.evaluate(LOOP_JS)
        await page.wait_for_function("window._res && window._res.fim === true", timeout=120000)
        res = await page.evaluate("({..._res, erros: _errs})")
        print("RODADAS:", res["rodadas"], "| elementos clicados:", res["vistos"])
        print("ERROS JS:", res["erros"] if res["erros"] else "nenhum")
        print("ERROS CONSOLE:", console_erros if console_erros else "nenhum")

        # prints de demos: rola ate a parte 1 e parte 2
        for nome, seletor in [("02_calculadora", "section#parte1"), ("03_seletor", "section#parte2")]:
            try:
                await page.locator(seletor).first.scroll_into_view_if_needed()
                await page.wait_for_timeout(900)
                await page.screenshot(path=str(PRINTS / f"{nome}.png"))
            except Exception as e:
                print(f"print {nome} falhou:", e)

        # celular 375px: nao pode rolar na horizontal
        await page.set_viewport_size({"width": 375, "height": 800})
        await page.reload()
        await page.wait_for_timeout(1000)
        medidas = await page.evaluate("({sw: document.documentElement.scrollWidth, iw: innerWidth})")
        print("CELULAR 375px: scrollWidth =", medidas["sw"], "| innerWidth =", medidas["iw"],
              "|", "OK" if medidas["sw"] <= medidas["iw"] + 1 else "ROLA NA HORIZONTAL (problema)")
        await page.screenshot(path=str(PRINTS / "04_celular.png"))

        await browser.close()

asyncio.run(main())
