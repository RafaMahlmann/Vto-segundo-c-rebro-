# Checklist da Fase 2 (Seletor de colunas no Anonimizador) - AGENTS.md secao 6
import asyncio, pathlib
from playwright.async_api import async_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
PATCHES = ROOT / "patches"
PRINTS = ROOT / "propostas" / "2026-10-07" / "prints"
PRINTS.mkdir(parents=True, exist_ok=True)

CORTES = [0, 3, 6, 36, 44, 49, 79, 84, 93, 98, 103, 133, 163, 193, 196, 203, 206, 210, 216,
          229, 232, 235, 238, 241, 244, 247, 250, 253, 256, 259, 262, 263, 264, 265, 266,
          274, 282, 290, 298, 306, 307, 315, 316, 317, 319, 320, 321, 322, 323, 325, 326,
          339, 347, 353, 354, 368, 376, 382, 383, 384, 388, 392, 396, 400, 404, 408, 412,
          416, 420, 424, 428, 435, 442, 449, 456, 463, 470, 477, 484, 491, 498, 505, 512,
          519, 526, 533, 540, 547, 554, 561, 568, 575, 582, 589, 596, 600, 601, 603, 606,
          608, 610, 611, 612, 621, 623, 625, 630, 638, 652, 666, 680, 694, 709, 721, 734,
          748, 757, 759, 761, 763, 765, 767, 769, 771, 773, 775, 777, 779, 799, 810, 817,
          821, 829, 832, 840, 848, 856, 864, 872, 880, 888, 896, 904, 912, 920, 945, 961,
          968, 975, 978, 981, 1011, 1016, 1025, 1026, 1038, 1043, 1093, 1100, 1105]

def gerar_txt():
    linhas = []
    for li in range(3):
        buf = []
        for k in range(len(CORTES) - 1):
            larg = CORTES[k + 1] - CORTES[k]
            val = (f"L{li}C{k}")[:larg].ljust(larg)
            buf.append(val)
        linhas.append("".join(buf))
    p = PATCHES / "_fixture_seletor.txt"
    p.write_text("\n".join(linhas) + "\n", encoding="ascii")
    return p

async def main():
    txt_path = gerar_txt()
    csv_path = PATCHES / "_fixture_seletor.csv"
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width": 1280, "height": 900})
        erros = []
        page.on("console", lambda m: erros.append(m.text) if m.type == "error" else None)
        page.on("pageerror", lambda e: erros.append(str(e)))

        await page.goto((ROOT / "index.html").as_uri())
        await page.wait_for_timeout(1500)

        # 1. console limpo + as 6 abas abrem
        print("1) erros no load:", erros if erros else "ZERO")
        for aba in ["prazo", "dilacao", "fluxo", "matriculas", "estatisticas"]:
            await page.click(f".tab-btn[onclick*=\"mostrarAba('{aba}')\"]")
            await page.wait_for_timeout(300)
            vis = await page.locator(f"#aba-{aba}").first.is_visible()
            print(f"1b) aba {aba}:", "OK" if vis else "PROBLEMA")

        # 2. abre o anonimizador (iframe srcdoc)
        await page.click(".tab-btn[onclick*=\"mostrarAba('anonimizador')\"]")
        await page.wait_for_timeout(1500)
        frame = page.frame_locator("#anonimizadorFrame")

        # 3. carrega CSV -> 6 cartoes com amostras
        await frame.locator("#fileInput").set_input_files(str(csv_path))
        await frame.locator(".selc-card").first.wait_for(timeout=8000)
        await page.wait_for_timeout(1000)
        n = await frame.locator(".selc-card").count()
        print("3) cartoes CSV:", n, "OK" if n == 6 else "PROBLEMA")
        vals = await frame.locator("#amostra-0 .selc-val").all_text_contents()
        print("3b) amostras col 0:", vals[:3], "OK" if "12345678" in vals else "PROBLEMA")
        await page.screenshot(path=str(PRINTS / "08_seletor_csv.png"))

        # 4. bolinha: 1 clique muda o estado (e nao seleciona o cartao)
        await frame.locator("#chip-0 .selc-bol[data-estado='2']").click()
        await page.wait_for_timeout(200)
        cls = await frame.locator("#chip-0").get_attribute("class") or ""
        rot = await frame.locator("#chip-0 .selc-estado-rotulo").text_content()
        ativa = await frame.locator("#chip-0 .selc-bol[data-estado='2'].ativa").count()
        on = await frame.locator("#chip-0.selc-on").count()
        ok = "chip-anon" in cls and rot == "Anonimizar" and ativa == 1
        print("4) bolinha 1 clique:", "OK" if ok else f"PROBLEMA {cls} {rot}")
        print("4b) bolinha nao seleciona cartao:", "OK" if not on else "PROBLEMA")

        # 5. busca instantanea
        await frame.locator("#selcBusca").fill("cpf")
        await page.wait_for_timeout(300)
        vis = await frame.locator(".selc-card:not(.oculto)").count()
        print("5) busca 'cpf' mostra 1:", "OK" if vis == 1 else f"PROBLEMA {vis}")
        await frame.locator("#selcBusca").fill("zzzzz")
        await page.wait_for_timeout(300)
        vazio = await frame.locator("#selcVazio.visivel").count()
        print("5b) busca sem resultado mostra aviso:", "OK" if vazio else "PROBLEMA")
        await frame.locator("#selcBusca").fill("")
        await page.wait_for_timeout(300)

        # 6. modo CSV esconde a bolinha Simular
        disp = await frame.locator("#chip-1 .selc-bol[data-estado='4']").evaluate("el => getComputedStyle(el).display")
        print("6) CSV esconde Simular:", "OK" if disp == "none" else f"PROBLEMA {disp}")

        # 7. selecionar visiveis + acao em massa
        await frame.locator("button.selc-btn-mini:has-text('Selecionar visíveis')").click()
        await page.wait_for_timeout(400)
        barra = await frame.locator("#selcBarra.aberta").count()
        n_txt = await frame.locator("#selcBarraN").text_content()
        print("7) barra de massa abre:", "OK" if barra and "6 colunas" in n_txt else f"PROBLEMA {n_txt}")
        await frame.locator("#selcBarra .selc-bol-grande[data-estado='0']").click()
        await page.wait_for_timeout(6 * 12 + 500)
        excl = await frame.locator(".selc-card.chip-exclude").count()
        cont = await frame.locator("#selcContador").text_content()
        print("7b) massa excluir tudo:", "OK" if excl == 6 and "6 Excluir" in cont else f"PROBLEMA {excl} {cont}")
        await page.screenshot(path=str(PRINTS / "09_seletor_csv_massa.png"))

        # 8. TXT: 159 cartoes, preset Power Query, Simular visivel
        await frame.locator("#fileInput").set_input_files(str(txt_path))
        await frame.locator("#chip-158").wait_for(timeout=8000)
        await page.wait_for_timeout(1000)
        n2 = await frame.locator(".selc-card").count()
        print("8) cartoes TXT:", n2, "OK" if n2 == 159 else "PROBLEMA")
        vals2 = await frame.locator("#amostra-3 .selc-val").all_text_contents()
        print("8b) amostra TXT col 3:", vals2[:2], "OK" if any("L0C3" in v for v in vals2) else "PROBLEMA")
        disp2 = await frame.locator("#chip-3 .selc-bol[data-estado='4']").evaluate("el => getComputedStyle(el).display")
        print("8c) TXT mostra Simular:", "OK" if disp2 != "none" else "PROBLEMA")
        # 8f. falsos positivos (ANTES do preset): NOME-BAIRRO/FONTE/RESERVA/ENDER-ALT nascem "Manter"
        ids_fp = {127: "NOME-BAIRRO", 131: "NOME-FONTE", 132: "NOME-RESERVA", 150: "NOME-ENDER-ALT"}
        for cid, cnome in ids_fp.items():
            cls_fp = await frame.locator(f"#chip-{cid}").get_attribute("class") or ""
            ok_fp = "chip-normal" in cls_fp and "chip-anon" not in cls_fp
            print(f"8f) {cnome} ({cid}) nasce Manter:", "OK" if ok_fp else f"PROBLEMA {cls_fp}")
        # e o NOME-CLIENTE (id 2) continua protegido (simular)
        cls_nc = await frame.locator("#chip-2").get_attribute("class") or ""
        print("8g) NOME-CLIENTE continua Simular:", "OK" if "chip-simular" in cls_nc else f"PROBLEMA {cls_nc}")
        await frame.locator("#btnPowerQuery").click()
        await page.wait_for_timeout(800)
        cont2 = await frame.locator("#selcContador").text_content()
        sim = await frame.locator(".selc-card.chip-simular").count()
        dub = await frame.locator(".selc-card.chip-duble").count()
        print("8d) preset SGCG:", "OK" if sim >= 10 and dub >= 1 else f"PROBLEMA {cont2}")
        print("    contador:", cont2)
        # amostras sobrevivem ao preset (regressao do innerHTML antigo)
        vals3 = await frame.locator("#amostra-3 .selc-val").all_text_contents()
        print("8e) amostras sobrevivem ao preset:", "OK" if any("L0C3" in v for v in vals3) else f"PROBLEMA {vals3[:2]}")
        await page.screenshot(path=str(PRINTS / "10_seletor_txt_preset.png"), full_page=False)

        print("ERROS FINAIS:", erros if erros else "ZERO")
        await browser.close()

asyncio.run(main())
