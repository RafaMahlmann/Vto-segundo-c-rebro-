# script temporario de validacao visual do checklist reconstruido
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

alvo = Path(sys.argv[1]).resolve()
saida = Path(sys.argv[2]).resolve()

with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": 1280, "height": 1600})
    erros = []
    pg.on("pageerror", lambda e: erros.append(str(e)))
    pg.on("console", lambda m: erros.append(m.text) if m.type == "error" else None)
    pg.goto(alvo.as_uri())
    pg.wait_for_timeout(400)
    pct = pg.locator("#pct").inner_text()
    cont = pg.locator("#cont").inner_text()
    print("PLACAR:", pct, cont)
    for et in ["e0", "e1", "e2", "e3", "e4", "er"]:
        print(et, pg.locator(f'[data-c="{et}"]').inner_text(),
              "feito" if (pg.locator(f'[data-rail="{et}"]').get_attribute("class") or "").find("feito") >= 0 else "-")
    pg.screenshot(path=str(saida), full_page=True)
    print("ERROS CONSOLE:", erros if erros else "zero")
    b.close()
