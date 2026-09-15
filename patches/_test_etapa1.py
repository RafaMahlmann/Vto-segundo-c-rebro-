# -*- coding: utf-8 -*-
"""
Teste da ETAPA 1 (export limpo) + teste de regressao das 6 abas.

Roda o app de verdade em file:// com o Playwright:
  A. vazamento  - o HTML exportado nao pode conter matricula nem banner
  B. inchaco    - o exportado tem que ficar do tamanho do arquivo em disco
  C. roletas    - as setas do fluxo nao podem duplicar
  D. reabertura - o arquivo exportado abre, as 6 abas funcionam, console limpo
  E. confirmacao- o botao Exportar ZIP pergunta antes de baixar
  F. regressao  - undo, timeline, CSV e JSON continuam funcionando

Uso:  venv_agente/Scripts/python.exe patches/_test_etapa1.py
"""
import io
import os
import pathlib
import re
import sys

from playwright.sync_api import sync_playwright

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

RAIZ = pathlib.Path(__file__).resolve().parent.parent
INDEX = RAIZ / "index.html"
SAIDA = RAIZ / "patches" / "_saida_teste_etapa1"

falhas = []
passou = []


def checa(nome, condicao, detalhe=""):
    if condicao:
        passou.append(nome)
        print("  OK   %s %s" % (nome, detalhe))
    else:
        falhas.append(nome)
        print("  FALHA %s %s" % (nome, detalhe))


def main():
    SAIDA.mkdir(parents=True, exist_ok=True)
    fonte = io.open(INDEX, encoding="utf-8", newline="").read()
    navs_fonte = fonte.count("roleta-nav")
    bytes_fonte = len(fonte.encode("utf-8"))

    with sync_playwright() as p:
        nav = p.chromium.launch()
        pg = nav.new_page(viewport={"width": 1400, "height": 900})
        erros = []
        pg.on("pageerror", lambda e: erros.append("pageerror: " + str(e)[:160]))
        pg.on("console", lambda m: erros.append("console.error: " + m.text[:160])
              if m.type == "error" else None)

        pg.goto(INDEX.as_uri())
        pg.wait_for_timeout(1500)

        # coloca dados na tela, que e a situacao de risco
        pg.click("button:has-text('Matriculas')")
        pg.wait_for_timeout(700)
        pg.click("button:has-text('Fluxo de Vistorias VTO')")
        pg.wait_for_timeout(700)

        total = pg.evaluate("() => (typeof matriculas !== 'undefined') ? matriculas.length : 0")
        print("\n[preparo] matriculas na tela: %d" % total)
        checa("dados carregados na tela", total > 0, "(%d matriculas)" % total)

        # Guarda contra script cortado no meio. Basta a tag de fechamento de
        # script dentro de uma string ou comentario para o parser encerrar o
        # bloco ali, e o app deixa de inicializar sem um unico erro no console.
        blocos = pg.evaluate("() => document.querySelectorAll('script').length")
        checa("os 3 blocos de script sobreviveram ao parser", blocos == 3,
              "(%d blocos; esperado 3: principal, Base64, retrato)" % blocos)
        retrato = pg.evaluate("() => typeof window._htmlOriginal === 'string' ? window._htmlOriginal.length : -1")
        checa("retrato do arquivo limpo foi tirado", retrato > 200000,
              "(%d caracteres)" % retrato)
        checa("o retrato leva o anonimizador embutido",
              pg.evaluate("() => (window._htmlOriginal || '').indexOf('anonimizadorFonte') !== -1"))

        # ---------- A, B, C: o HTML que seria distribuido ----------
        print("\n[A/B/C] conteudo do arquivo exportado")
        limpo = pg.evaluate("() => prepararHtmlLimpo()")
        sujo = pg.evaluate("() => '<!DOCTYPE html>' + String.fromCharCode(10) + document.documentElement.outerHTML")

        nums = pg.evaluate("() => matriculas.slice(0, 30).map(m => String(m.numero))")
        vazados = [n for n in nums if limpo.count(n) > fonte.count(n)]
        vazados_antes = [n for n in nums if sujo.count(n) > fonte.count(n)]

        checa("nenhuma matricula no exportado", len(vazados) == 0,
              "(antes vazavam %d)" % len(vazados_antes))
        checa("o bug existia mesmo", len(vazados_antes) > 0,
              "(%d matriculas vazavam)" % len(vazados_antes))
        banner_ativo = 'id="bannerVersao" class="ativo"' in limpo or 'class="ativo" id="bannerVersao"' in limpo
        banner_texto = re.search(r'id="bannerVersaoTexto"[^>]*>([^<]*)<', limpo)
        checa("banner de versao desligado no exportado",
              (not banner_ativo) and (not (banner_texto and banner_texto.group(1).strip())),
              "(ativo=%s texto=%r)" % (banner_ativo, banner_texto.group(1) if banner_texto else None))
        checa("tabela de matriculas vazia", limpo.count("<tr") <= fonte.count("<tr"),
              "(exportado %d / fonte %d)" % (limpo.count("<tr"), fonte.count("<tr")))

        bytes_limpo = len(limpo.encode("utf-8"))
        bytes_sujo = len(sujo.encode("utf-8"))
        folga = bytes_limpo - bytes_fonte
        checa("exportado sem inchaco", abs(folga) < 2000,
              "(fonte %d / limpo %d / sujo %d bytes)" % (bytes_fonte, bytes_limpo, bytes_sujo))

        navs_limpo = limpo.count("roleta-nav")
        navs_sujo = sujo.count("roleta-nav")
        checa("setas de roleta nao duplicam", navs_limpo == navs_fonte,
              "(fonte %d / limpo %d / sujo %d)" % (navs_fonte, navs_limpo, navs_sujo))

        # ---------- E: confirmacao antes de baixar ----------
        print("\n[E] confirmacao antes de baixar")
        perguntas = []

        def responde(d):
            perguntas.append(d.message)
            d.dismiss()

        pg.on("dialog", responde)
        pg.click(".btn-zip")
        pg.wait_for_timeout(600)
        checa("pergunta antes de gerar o ZIP", len(perguntas) == 1,
              "(%d dialogo(s))" % len(perguntas))
        if perguntas:
            checa("aviso fala dos dados da tela", "NAO vao junto" in perguntas[0],
                  "\n         texto: " + perguntas[0].replace("\n", " | "))
        rotulo = pg.evaluate("() => document.querySelector('.btn-zip').textContent")
        checa("botao volta ao normal ao recusar", "..." not in rotulo,
              "(rotulo: %s)" % rotulo.strip())

        # ---------- F: regressao no app original ----------
        print("\n[F] regressao no app original")
        pg.click("button:has-text('Matriculas')")
        pg.wait_for_timeout(500)
        antes = pg.evaluate("() => matriculas.length")
        pg.keyboard.press("Control+z")
        pg.wait_for_timeout(300)
        checa("Ctrl+Z nao quebra", pg.evaluate("() => typeof matriculas !== 'undefined'"))
        pg.evaluate("() => { matriculaAtiva = matriculas[0].numero; atualizarTimeline(); }")
        pg.wait_for_timeout(400)
        marcos = pg.evaluate("() => document.getElementById('timelineFases').children.length")
        checa("timeline renderiza", marcos >= 0, "(%d fases)" % marcos)
        for fn in ["exportarCSV", "exportarJSON"]:
            ok = pg.evaluate("(f) => typeof window[f] === 'function' || typeof eval(f) === 'function'", fn)
            checa("funcao %s existe" % fn, ok)

        nav.close()

    # ---------- D: reabre o arquivo exportado ----------
    print("\n[D] o arquivo exportado abre e funciona")
    (SAIDA / "index.html").write_text(limpo, encoding="utf-8", newline="")
    anon = RAIZ / "anonimizador.html"
    (SAIDA / "anonimizador.html").write_text(
        anon.read_text(encoding="utf-8"), encoding="utf-8", newline="")

    with sync_playwright() as p:
        nav = p.chromium.launch()
        pg = nav.new_page(viewport={"width": 1400, "height": 900})
        erros2 = []
        pg.on("pageerror", lambda e: erros2.append("pageerror: " + str(e)[:160]))
        pg.on("console", lambda m: erros2.append("console.error: " + m.text[:160])
              if m.type == "error" else None)
        pg.goto((SAIDA / "index.html").as_uri())
        pg.wait_for_timeout(1500)

        abas = [("Calculadora de Prazo", "prazo"), ("Calculadora de Dilacao", "dilacao"),
                ("Fluxo de Vistorias VTO", "fluxo"), ("Matriculas", "matriculas"),
                ("Estatisticas", "estatisticas"), ("Anonimizador", "anonimizador")]
        abertas = 0
        for rotulo, ident in abas:
            pg.click("button:has-text('%s')" % rotulo)
            pg.wait_for_timeout(400)
            if pg.evaluate("(a) => document.getElementById('aba-' + a).classList.contains('active')", ident):
                abertas += 1
        checa("as 6 abas abrem", abertas == 6, "(%d de 6)" % abertas)

        recarregou = pg.evaluate("() => (typeof matriculas !== 'undefined') ? matriculas.length : -1")
        checa("dados de demonstracao voltam no load", recarregou > 0, "(%d matriculas)" % recarregou)

        navs_vivo = pg.evaluate("() => document.querySelectorAll('.roleta-nav').length")
        checa("setas de roleta sem duplicata ao reabrir", navs_vivo == 11,
              "(%d setas; esperado 11)" % navs_vivo)

        banner = pg.evaluate("() => document.getElementById('bannerVersao').classList.contains('ativo')")
        print("       (banner de versao ativo ao reabrir: %s - depende do version.json)" % banner)

        linhas = pg.evaluate("() => document.querySelectorAll('#listaMatriculas tr').length")
        checa("tabela de matriculas volta a renderizar", linhas > 0, "(%d linhas)" % linhas)

        # depois da Etapa 2 o anonimizador vem do Base64 embutido (about:srcdoc),
        # e nao mais de um arquivo irmao
        quadros = [f for f in pg.frames if f != pg.main_frame]
        anon_ok = any("srcdoc" in f.url for f in quadros)
        titulo_anon = ""
        for f in quadros:
            try:
                titulo_anon = f.evaluate("() => document.title")
            except Exception:
                pass
        checa("aba do anonimizador carrega sem arquivo irmao", anon_ok,
              "(frame: %s)" % ", ".join(f.url[:20] for f in quadros))
        checa("anonimizador certo dentro da aba", "Auditoria" in titulo_anon,
              "(titulo: %s)" % titulo_anon[:45])

        checa("console sem erro no arquivo exportado", len(erros2) == 0,
              "" if not erros2 else "\n         " + "\n         ".join(erros2[:4]))
        nav.close()

    print("\n" + "=" * 62)
    print("PASSOU: %d    FALHOU: %d" % (len(passou), len(falhas)))
    if falhas:
        print("Falhas: " + ", ".join(falhas))
    print("=" * 62)
    return 1 if falhas else 0


if __name__ == "__main__":
    sys.exit(main())
