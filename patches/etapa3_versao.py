# -*- coding: utf-8 -*-
"""
ETAPA 3 - Versao, banner falso e nome do ZIP.

Problemas:
  F4  version.json dizia 4.3 e o index inteiro dizia v4.2. Resultado: o banner
      "Nova versao disponivel" aparecia para sempre, inclusive para quem tinha
      acabado de baixar a versao nova.
  F6  o commit 5a09c31 (fix do CRC32) desfez sem querer o nome versionado do
      ZIP, que o commit anterior tinha acabado de criar.

Correcoes:
  1. sobe TODOS os pontos de versao de uma vez (protocolo do AGENTS.md secao 8)
  2. o banner so aparece quando a versao remota e MAIOR que a local.
     Antes era "diferente de", entao qualquer descompasso ligava o banner -
     ate um numero mais antigo no GitHub.
  3. devolve a versao ao nome do arquivo ZIP

Uso:  python patches/etapa3_versao.py [versao]     (padrao: 4.4)
"""
import io
import json
import os
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VELHA = "4.2"


def troca_index(nova):
    caminho = os.path.join(RAIZ, "index.html")
    with io.open(caminho, encoding="utf-8", newline="") as f:
        html = f.read()

    trocas = [
        ("titulo",
         "<title>VTO v%s — Prazos e Vistorias</title>" % VELHA,
         "<title>VTO v%s — Prazos e Vistorias</title>" % nova),
        ("badge do header",
         '<span class="versao-badge" id="versaoBadge" data-versao>v%s</span>' % VELHA,
         '<span class="versao-badge" id="versaoBadge" data-versao>v%s</span>' % nova),
        ("rodape da aba 1",
         'color:#adb5bd" data-versao>v%s</div>' % VELHA,
         'color:#adb5bd" data-versao>v%s</div>' % nova),
        ("rodape da aba 2",
         '<div class="footer" data-versao>v%s</div>' % VELHA,
         '<div class="footer" data-versao>v%s</div>' % nova),
        ("rodape da aba 4",
         '<div class="footer">v%s - IT OPE 1580</div>' % VELHA,
         '<div class="footer">v%s - IT OPE 1580</div>' % nova),
        ("rodape da aba 5",
         '<div class="footer">v%s - Timeline Proporcional</div>' % VELHA,
         '<div class="footer">v%s - Timeline Proporcional</div>' % nova),
        ("versao dinamica",
         "const versao = 'v%s.' + dataHora;" % VELHA,
         "const versao = 'v%s.' + dataHora;" % nova),
        ("VERSAO_LOCAL",
         "const VERSAO_LOCAL = '%s';" % VELHA,
         "const VERSAO_LOCAL = '%s';" % nova),
        ("nome do ZIP",
         "    a.download = 'vto-completo.zip';",
         "    a.download = 'vto-completo-v' + VERSAO_LOCAL + '.zip';"),
        ("comparacao do banner",
         "            if (d.versao && d.versao !== VERSAO_LOCAL) {",
         "            if (d.versao && versaoEhMaior(d.versao, VERSAO_LOCAL)) {"),
        ("funcao de comparacao",
         "(function verificarNovaVersao() {",
         "// Compara 4.10 com 4.9 do jeito certo: numero por numero, nao como texto.\n"
         "// Antes a checagem era 'diferente de', entao qualquer descompasso entre o\n"
         "// arquivo e o version.json ligava o banner - ate um numero mais ANTIGO.\n"
         "function versaoEhMaior(remota, local) {\n"
         "    const a = String(remota).split('.').map(n => parseInt(n, 10) || 0);\n"
         "    const b = String(local).split('.').map(n => parseInt(n, 10) || 0);\n"
         "    for (let i = 0; i < Math.max(a.length, b.length); i++) {\n"
         "        const x = a[i] || 0, y = b[i] || 0;\n"
         "        if (x !== y) return x > y;\n"
         "    }\n"
         "    return false;\n"
         "}\n"
         "\n"
         "(function verificarNovaVersao() {"),
    ]

    for nome, antigo, _novo in trocas:
        if html.count(antigo) != 1:
            print("ABORTADO: '%s' apareceu %d vez(es), esperava 1." % (nome, html.count(antigo)))
            return None

    for _nome, antigo, novo_txt in trocas:
        html = html.replace(antigo, novo_txt, 1)

    with io.open(caminho, "w", encoding="utf-8", newline="") as f:
        f.write(html)
    print("  index.html      : %d pontos de versao trocados" % len(trocas))
    return True


def troca_sw(nova):
    caminho = os.path.join(RAIZ, "sw.js")
    with io.open(caminho, encoding="utf-8", newline="") as f:
        js = f.read()
    antigo = "const CACHE_NAME = 'vto-cache-v%s';" % VELHA
    if js.count(antigo) != 1:
        print("ABORTADO: CACHE_NAME nao bateu no sw.js.")
        return None
    js = js.replace(antigo, "const CACHE_NAME = 'vto-cache-v%s';" % nova, 1)
    with io.open(caminho, "w", encoding="utf-8", newline="") as f:
        f.write(js)
    print("  sw.js           : CACHE_NAME -> vto-cache-v%s" % nova)
    return True


def troca_version_json(nova):
    caminho = os.path.join(RAIZ, "version.json")
    with io.open(caminho, encoding="utf-8", newline="") as f:
        antes = json.load(f).get("versao")
    with io.open(caminho, "w", encoding="utf-8", newline="") as f:
        f.write('{\n"versao": "%s"\n}\n' % nova)
    print("  version.json    : %s -> %s" % (antes, nova))
    return True


def main():
    nova = sys.argv[1] if len(sys.argv) > 1 else "4.4"
    print("Subindo a versao para v%s" % nova)
    if troca_index(nova) is None:
        return 1
    if troca_sw(nova) is None:
        return 1
    troca_version_json(nova)
    print("\nATENCAO: o banner so fica correto para os outros depois que o")
    print("version.json for enviado para o GitHub. Ate la, quem abrir o app")
    print("nao ve banner nenhum (o remoto 4.3 agora e MENOR que o local).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
