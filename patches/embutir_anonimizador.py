# -*- coding: utf-8 -*-
"""
Embute o conteudo de anonimizador.html dentro do index.html em Base64.

E desse bloco que saem AS DUAS coisas:
  - a aba 6 (carregarAnonimizador() le o Base64 e joga no iframe);
  - o botao Exportar ZIP (que escreve o anonimizador dentro do pacote).

REGRA: editou anonimizador.html? Rode este script antes de exportar
qualquer coisa. Senao a aba mostra a versao nova e o ZIP distribui a velha.

Este script SO mexe no bloco Base64. Ele nao toca em nenhuma funcao
JavaScript do index.html.
  (Versao anterior reescrevia gerarZipCompleto() junto e, depois da Etapa 1,
   isso desfazia a correcao de vazamento de dado pessoal no export.)

Uso:  python patches/embutir_anonimizador.py
"""
import base64
import io
import os
import re
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INDEX = os.path.join(RAIZ, "index.html")
ANON = os.path.join(RAIZ, "anonimizador.html")

MARCA_ABRE = "<!-- ANONIMIZADOR EMBUTIDO (Base64) -->"
MARCA_FECHA = "<!-- /ANONIMIZADOR EMBUTIDO -->"


def main():
    with io.open(ANON, encoding="utf-8", newline="") as f:
        anon_html = f.read()
    with io.open(INDEX, encoding="utf-8", newline="") as f:
        index_html = f.read()

    anon_b64 = base64.b64encode(anon_html.encode("utf-8")).decode("ascii")

    bloco = (
        "\n" + MARCA_ABRE + "\n"
        '<script id="anonimizadorFonte" type="application/octet-stream">'
        + anon_b64 +
        "</script>\n"
        + MARCA_FECHA + "\n"
    )

    antes = index_html

    if MARCA_ABRE in index_html:
        # troca o bloco existente, sem mexer em mais nada
        novo = re.sub(
            r"\n" + re.escape(MARCA_ABRE) + r".*?" + re.escape(MARCA_FECHA) + r"\n",
            lambda _m: bloco,
            index_html,
            count=1,
            flags=re.DOTALL,
        )
    else:
        if index_html.count("</body>") != 1:
            print("ABORTADO: nao achei um </body> unico no index.html.")
            return 1
        novo = index_html.replace("</body>", bloco + "</body>", 1)

    if novo == antes:
        print("Nada a fazer: o Base64 ja estava igual ao anonimizador.html.")
        return 0

    with io.open(INDEX, "w", encoding="utf-8", newline="") as f:
        f.write(novo)

    print("OK: anonimizador embutido (%d bytes de Base64)." % len(anon_b64))
    print("    index.html: %d -> %d caracteres." % (len(antes), len(novo)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
