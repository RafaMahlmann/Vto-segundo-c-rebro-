# -*- coding: utf-8 -*-
"""
ETAPA 2b - Fecha a <div class="header"> do anonimizador.

Causa do layout espremido: a div .header (display:flex) nunca era fechada.
O app inteiro virava filho do cabecalho flex, entao o titulo quebrava na
vertical e o conteudo se amontoava numa coluna estreita.
Sao 37 <div> abertos e 36 </div> no body.

Correcao: uma linha. Fecha .header logo depois de .header-actions.
Vale para o anonimizador avulso E para a copia embutida no VTO.

Depois deste script: rodar patches/embutir_anonimizador.py.
"""
import io
import re
import sys

CAMINHO = "anonimizador.html"

ANTIGO = """        <div class="header-actions">
            <a href="index.html" class="nav-vto-btn" title="Voltar ao VTO">&#8592; VTO</a>
            <div class="version-badge">v19.0.0 (Segurança Reconstruída)</div>
    </div>

    <div class="tabs">"""

NOVO = """        <div class="header-actions">
            <a href="index.html" class="nav-vto-btn" title="Voltar ao VTO">&#8592; VTO</a>
            <div class="version-badge">v19.0.0 (Segurança Reconstruída)</div>
        </div>
    </div>

    <div class="tabs">"""


def divs(texto):
    corpo = texto[texto.index("<body>"):texto.index("</body>")]
    return len(re.findall(r"<div\b", corpo)), len(re.findall(r"</div>", corpo))


def main():
    with io.open(CAMINHO, encoding="utf-8", newline="") as f:
        html = f.read()

    # o arquivo usa CRLF; alinha as ancoras com a quebra de linha real
    quebra = "\r\n" if "\r\n" in html else "\n"
    antigo = ANTIGO.replace("\n", quebra)
    novo_bloco = NOVO.replace("\n", quebra)

    abre, fecha = divs(html)
    print("antes : %d <div> / %d </div>" % (abre, fecha))

    if html.count(antigo) != 1:
        print("ABORTADO: ancora do header nao bateu (%d ocorrencias)." % html.count(antigo))
        return 1

    novo = html.replace(antigo, novo_bloco, 1)

    a2, f2 = divs(novo)
    print("depois: %d <div> / %d </div>" % (a2, f2))
    if a2 != f2:
        print("ABORTADO: as divs continuam desbalanceadas. Nada foi gravado.")
        return 1

    with io.open(CAMINHO, "w", encoding="utf-8", newline="") as f:
        f.write(novo)
    print("OK: header fechado. %d -> %d caracteres." % (len(html), len(novo)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
