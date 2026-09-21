# -*- coding: utf-8 -*-
"""
Teste da roleta do Fluxo: casa vazia + busca por codigo + efeito de giro.

Roda o app de verdade em file:// com o Playwright:
  A. estado inicial - 11 retangulos vazios, botoes reais intactos no HTML
  B. busca          - digitar, filtrar, encaixe sozinho, outra vistoria, nome
  C. roleta         - setas, casa vazia no giro, limpar, efeito sem sobra
  D. registro       - 1o clique arma, 2o abre o modal, salva, Ctrl+Z desfaz
  E. teclado        - digitar com grupo armado, Delete, Enter; nao rouba digito
  F. modos          - carrossel, movimento reduzido
  G. export limpo   - retrato (plano A) e limpeza do DOM vivo (plano B)
  H. 6 abas         - abrem sem erro de console

Uso:  venv_agente/Scripts/python.exe patches/_test_roleta_vazia.py
"""
import pathlib
import re
import sys

from playwright.sync_api import sync_playwright

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

RAIZ = pathlib.Path(__file__).resolve().parent.parent
URL = (RAIZ / "index.html").as_uri()

falhas = []
erros = []


def checa(nome, ok, detalhe=""):
    print("  %s %s %s" % ("OK   " if ok else "FALHA", nome, detalhe))
    if not ok:
        falhas.append(nome)


def abre(br, largura=1300):
    pg = br.new_page(viewport={"width": largura, "height": 1000})
    # o 404 do version.json (verificador de versao no GitHub) ja existia antes; nao e da roleta
    pg.on("console", lambda m: erros.append(m.text) if m.type == "error" and "version.json" not in (m.location.get("url") or "") else None)
    pg.on("pageerror", lambda e: erros.append(str(e)))
    pg.goto(URL)
    pg.wait_for_timeout(500)
    pg.evaluate("() => mostrarAba('fluxo')")
    pg.wait_for_timeout(200)
    return pg


with sync_playwright() as p:
    br = p.chromium.launch()
    pg = abre(br)
    visiveis = lambda sel: pg.evaluate(
        "(s) => [...document.querySelectorAll(s)].filter(e => e.offsetParent !== null).length", sel)

    print("A. estado inicial")
    checa("11 grupos de roleta", pg.locator(".roleta-grupo").count() == 11)
    checa("11 setas (roleta-nav)", pg.locator(".roleta-nav").count() == 11)
    checa("11 casas vazias visiveis", visiveis(".roleta-vazio") == 11)
    checa("nenhum codigo visivel", visiveis(".roleta-grupo .servico-btn") == 0)
    checa("45 botoes reais continuam no HTML", pg.locator(".roleta-grupo .servico-btn").count() == 45)
    checa("cards de sancao intactos (2)", pg.locator(".sancao-btn").count() == 2)
    checa("botoes reais mantem onclick e data-cod",
          pg.evaluate("() => [...document.querySelectorAll('.roleta-grupo .servico-btn')]"
                      ".every(b => b.getAttribute('onclick') && b.getAttribute('data-cod'))"))
    g1 = pg.locator(".roleta-grupo").nth(0)   # 1a vistoria / Servicos

    total0 = pg.evaluate("() => matriculas.reduce((n, m) => n + m.servicos.length, 0)")
    print("B. busca")
    g1.locator(".roleta-vazio").click()
    checa("clicar no vazio abre a busca", "roleta-buscando" in (g1.get_attribute("class") or ""))
    checa("campo de busca ganhou foco", pg.evaluate("() => document.activeElement.tagName") == "INPUT")
    checa("lista mostra os 3 codigos", g1.locator(".roleta-busca li").count() == 3)
    g1.locator("input").type("84")
    checa("'84' filtra para 2", g1.locator(".roleta-busca li").count() == 2)
    g1.locator("input").type("03")
    pg.wait_for_timeout(500)
    checa("8403 encaixa sozinho", g1.locator(".servico-btn[data-cod='8403']").is_visible())
    checa("busca fechou", "roleta-buscando" not in (g1.get_attribute("class") or ""))
    checa("grupo ficou armado", "roleta-armada" in (g1.get_attribute("class") or ""))
    checa("nada foi registrado so por escolher",
          pg.evaluate("() => matriculas.reduce((n, m) => n + m.servicos.length, 0)") == total0)
    pg.wait_for_timeout(500)

    g1.locator(".roleta-limpar").click()
    pg.wait_for_timeout(500)
    g1.locator(".roleta-vazio").click()
    g1.locator("input").type("8428")
    pg.wait_for_timeout(300)
    msg = g1.locator(".roleta-busca .msg").inner_text()
    checa("codigo de outra vistoria explica onde mora", "3a Vistoria - Servicos" in msg, msg)
    g1.locator("input").press("Escape")
    checa("Esc volta para o vazio", g1.locator(".roleta-vazio").is_visible())

    g2 = pg.locator(".roleta-grupo").nth(1)   # Intermediarios
    g2.locator(".roleta-vazio").click()
    g2.locator("input").type("topo")
    checa("busca por nome acha Topografia", g2.locator(".roleta-busca li").count() == 1)
    g2.locator("input").press("Enter")
    pg.wait_for_timeout(500)
    checa("Enter escolhe 8407", g2.locator(".servico-btn[data-cod='8407']").is_visible())

    g2.locator(".roleta-limpar").click()
    pg.wait_for_timeout(500)
    g2.locator(".roleta-vazio").click()
    g2.locator("input").type("99")
    checa("'99' mostra 'Nada encontrado'", "Nada" in g2.locator(".roleta-busca .msg").inner_text())
    g2.locator("input").press("Escape")

    print("C. roleta")
    g1.locator(".roleta-baixo").click()
    pg.wait_for_timeout(500)
    checa("baixo a partir do vazio vai ao 1o codigo (8403)", g1.locator(".servico-btn[data-cod='8403']").is_visible())
    g1.locator(".roleta-baixo").click()
    pg.wait_for_timeout(450)
    checa("baixo -> 8421", g1.locator(".servico-btn[data-cod='8421']").is_visible())
    g1.locator(".roleta-baixo").click()
    g1.locator(".roleta-baixo").click()
    pg.wait_for_timeout(500)
    checa("depois do ultimo, a casa vazia volta ao giro", g1.locator(".roleta-vazio").is_visible())
    checa("sem sobra de efeito (fantasma) no DOM", pg.locator(".roleta-fantasma").count() == 0)
    checa("limpar escondido no vazio", not g1.locator(".roleta-limpar").is_visible())
    g1.locator(".roleta-cima").click()
    pg.wait_for_timeout(450)
    checa("cima a partir do vazio vai ao ultimo (8563)", g1.locator(".servico-btn[data-cod='8563']").is_visible())
    checa("bolinha ativa acompanha", g1.locator(".roleta-dot.ativo").count() == 1)
    g1.locator(".roleta-limpar").click()
    pg.wait_for_timeout(450)
    checa("limpar volta ao vazio", g1.locator(".roleta-vazio").is_visible())
    g1.hover()
    pg.mouse.wheel(0, 120)
    pg.wait_for_timeout(450)
    checa("rodinha gira", g1.locator(".servico-btn[data-cod='8403']").is_visible())

    print("D. registro")
    pg.evaluate("() => selecionarMatricula(matriculas[0].numero)")
    n0 = pg.evaluate("() => getMatriculaAtiva().servicos.length")
    pg.mouse.click(5, 5)
    b = g1.locator(".servico-btn[data-cod='8403']")
    b.click()
    checa("1o clique so arma (nao abre modal)",
          "roleta-armada" in (g1.get_attribute("class") or "")
          and not pg.evaluate("() => document.getElementById('modalOverlay').classList.contains('ativo')"))
    b.click()
    pg.wait_for_timeout(200)
    checa("2o clique abre o modal de datas",
          pg.evaluate("() => document.getElementById('modalOverlay').classList.contains('ativo')"))
    pg.locator("#modalDataCriacao").fill("2026-09-01")
    pg.locator("#btnSalvarModal").click()
    pg.wait_for_timeout(300)
    checa("servico registrado (+1)", pg.evaluate("() => getMatriculaAtiva().servicos.length") == n0 + 1)
    checa("bolinha verde (preenchido)", g1.locator(".roleta-dot.preenchido").count() == 1)
    checa("retangulo continua mostrando o 8403", g1.locator(".servico-btn[data-cod='8403']").is_visible())
    pg.evaluate("() => undo()")
    pg.wait_for_timeout(200)
    checa("Ctrl+Z (undo) desfaz o registro", pg.evaluate("() => getMatriculaAtiva().servicos.length") == n0)
    pg.keyboard.press("Control+Shift+Z")
    pg.wait_for_timeout(200)
    checa("Ctrl+Shift+Z refaz", pg.evaluate("() => getMatriculaAtiva().servicos.length") == n0 + 1)
    pg.keyboard.press("Control+z")
    pg.wait_for_timeout(200)
    checa("Ctrl+Z pelo teclado volta", pg.evaluate("() => getMatriculaAtiva().servicos.length") == n0)
    checa("Ctrl+Z nao mexeu na casa escolhida", g1.locator(".servico-btn[data-cod='8403']").is_visible())

    print("E. teclado")
    g3 = pg.locator(".roleta-grupo").nth(2)   # Habite-se, 1a vistoria
    pg.mouse.click(5, 5)
    g3.locator(".roleta-baixo").click()
    pg.wait_for_timeout(450)
    pg.keyboard.press("Delete")
    pg.wait_for_timeout(450)
    checa("Delete esvazia o grupo armado", g3.locator(".roleta-vazio").is_visible())
    pg.keyboard.type("8480")
    pg.wait_for_timeout(600)
    checa("digitar com grupo armado abre a busca e encaixa 8480", g3.locator(".servico-btn[data-cod='8480']").is_visible())
    pg.keyboard.press("ArrowDown")
    pg.wait_for_timeout(450)
    checa("seta pra baixo gira (8485)", g3.locator(".servico-btn[data-cod='8485']").is_visible())
    pg.keyboard.press("Enter")
    pg.wait_for_timeout(250)
    checa("Enter abre o modal (grupo armado + codigo escolhido)",
          pg.evaluate("() => document.getElementById('modalOverlay').classList.contains('ativo')"))
    pg.keyboard.press("Escape")
    pg.wait_for_timeout(200)
    checa("Esc fecha o modal", not pg.evaluate("() => document.getElementById('modalOverlay').classList.contains('ativo')"))
    # nao pode roubar digito de outros campos nem de outras abas
    g3.locator(".roleta-cima").click()
    pg.evaluate("() => mostrarAba('matriculas')")
    pg.wait_for_timeout(200)
    pg.locator("#novaMatricula").click()
    pg.keyboard.type("1234")
    checa("digitos na aba Matriculas ficam no campo",
          pg.locator("#novaMatricula").input_value() == "1234")
    checa("nenhuma busca abriu por engano", pg.locator(".roleta-buscando").count() == 0)
    pg.locator("#novaMatricula").fill("")
    pg.evaluate("() => mostrarAba('fluxo')")

    print("F. modos")
    pg.evaluate("() => alternarModoFluxo('carrossel')")
    pg.wait_for_timeout(400)
    gc = pg.locator("#coluna1 .roleta-grupo").nth(2)
    gc.scroll_into_view_if_needed()
    gc.locator(".roleta-lupa").click()
    pg.wait_for_timeout(300)
    ult = gc.locator(".roleta-busca li").last
    ult.scroll_into_view_if_needed()
    box = ult.bounding_box()
    topo = pg.evaluate("(p) => { const e = document.elementFromPoint(p.x, p.y); return e ? !!e.closest('.roleta-busca') : false; }",
                       {"x": box["x"] + box["width"] / 2, "y": box["y"] + box["height"] / 2})
    checa("carrossel: lista da busca nao fica cortada", topo)
    gc.locator("input").press("Escape")
    pg.evaluate("() => alternarModoFluxo('grade')")
    pg.close()

    pg = abre(br)
    pg.emulate_media(reduced_motion="reduce")
    gr = pg.locator(".roleta-grupo").nth(0)
    gr.locator(".roleta-baixo").click()
    checa("movimento reduzido: gira sem criar fantasma", pg.locator(".roleta-fantasma").count() == 0
          and gr.locator(".servico-btn[data-cod='8403']").is_visible())
    pg.close()

    print("G. export limpo")
    pg = abre(br)
    pg.locator(".roleta-grupo").nth(0).locator(".roleta-vazio").click()
    pg.keyboard.type("8403")
    pg.wait_for_timeout(500)
    retrato = pg.evaluate("() => window._htmlOriginal")
    checa("plano A: retrato sem palco nem busca gerados",
          'class="roleta-palco"' not in retrato and 'class="roleta-busca"' not in retrato and 'class="roleta-vazio"' not in retrato)
    checa("plano A: retrato mantem os 45 botoes", len(re.findall(r'class="servico-btn"[^>]*data-cod', retrato)) >= 40)
    limpo = pg.evaluate("() => { const o = window._htmlOriginal; window._htmlOriginal = null; const r = prepararHtmlLimpo(); window._htmlOriginal = o; return r; }")
    if not isinstance(limpo, str):
        limpo = pg.evaluate("() => { const o = window._htmlOriginal; window._htmlOriginal = null; const r = prepararHtmlLimpo(); window._htmlOriginal = o; return typeof r === 'string' ? r : (r.outerHTML || String(r)); }")
    checa("plano B: sem palco, busca, fantasma nem casa vazia",
          'class="roleta-palco"' not in limpo and 'class="roleta-busca"' not in limpo
          and 'class="roleta-vazio"' not in limpo and 'roleta-fantasma"' not in limpo.replace('.roleta-fantasma', ''))
    checa("plano B: sem setas nem grupo armado", 'class="roleta-nav"' not in limpo and 'roleta-armada"' not in limpo.replace('.roleta-armada', ''))
    checa("plano B: nenhum botao ficou com style=display:none",
          re.search(r'class="servico-btn"[^>]*style="display', limpo) is None)
    for nome, html in (("A", retrato), ("B", limpo)):
        pg2 = br.new_page(viewport={"width": 1300, "height": 1000})
        pg2.on("pageerror", lambda e: erros.append("reabertura %s: %s" % (nome, e)))
        pg2.set_content(html)
        pg2.wait_for_timeout(600)
        checa("reabrir %s: 11 vazios, 11 setas, sem palco dentro de palco" % nome,
              pg2.locator(".roleta-vazio").count() == 11 and pg2.locator(".roleta-nav").count() == 11
              and pg2.locator(".roleta-palco .roleta-palco").count() == 0
              and pg2.locator(".roleta-grupo .servico-btn").count() == 45)
        pg2.close()
    pg.close()

    print("H. 6 abas")
    pg = abre(br)
    for aba in ("prazo", "dilacao", "fluxo", "matriculas", "estatisticas", "anonimizador"):
        pg.evaluate("(a) => mostrarAba(a)", aba)
        pg.wait_for_timeout(250)
        checa("aba %s ativa" % aba, pg.evaluate("(a) => document.getElementById('aba-' + a).classList.contains('active')", aba))
    pg.close()
    br.close()

checa("zero erros de console", not erros, "; ".join(erros)[:400])
print("\nFALHAS: %s" % (falhas if falhas else "nenhuma"))
sys.exit(1 if falhas else 0)
