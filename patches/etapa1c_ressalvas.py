# -*- coding: utf-8 -*-
"""
ETAPA 1c - Fecha as duas ressalvas do teste independente.

1. O comentario <!-- /RETRATO DO ARQUIVO LIMPO --> nao chega no arquivo
   exportado: ele e parseado DEPOIS do outerHTML. Quem abrisse o arquivo
   distribuido veria o comentario de abertura sem o de fechamento.
   Correcao: o fechamento vira comentario de JavaScript, dentro do <script>.

2. A corretude depende de nada executar entre o fim do <script> principal e o
   bloco do retrato (uma fresta medida em 0,1 ms). Hoje nada executa, mas e uma
   premissa implicita que a proxima sessao pode quebrar sem perceber.
   Correcao: a premissa vira regra escrita, no codigo e no AGENTS.md.

Mexe em: index.html (so o bloco do retrato) e AGENTS.md (secao 9).
"""
import io
import os
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

INDEX_ANTIGO = """<script>
window._htmlOriginal = '<!DOCTYPE html>\\n' + document.documentElement.outerHTML;

aplicarVersaoDinamica();
gerarMockData();
initRoletas();
atualizarTodasRoletas();
alternarModoFluxo('grade');
</script>
<!-- /RETRATO DO ARQUIVO LIMPO -->
</body>"""

INDEX_NOVO = """<script>
// NAO INSIRA NADA entre o fim do script principal e este bloco. Tudo que
// rodar nessa fresta entra no retrato - e o retrato e tirado uma vez so, entao o
// arquivo sairia sujo em TODO export daquela sessao.
window._htmlOriginal = '<!DOCTYPE html>\\n' + document.documentElement.outerHTML;

// Agora sim o app pode desenhar.
aplicarVersaoDinamica();
gerarMockData();
initRoletas();
atualizarTodasRoletas();
alternarModoFluxo('grade');
// fim do RETRATO DO ARQUIVO LIMPO
</script>
</body>"""

AGENTS_ANTIGO = """Mexeu em algo que é renderizado em tempo de execução? Acrescente a limpeza
correspondente em `prepararHtmlLimpo()`."""

AGENTS_NOVO = """Mexeu em algo que é renderizado em tempo de execução? Acrescente a limpeza
correspondente em `prepararHtmlLimpo()` — ela é o plano B.

**Não insira nada entre o `</script>` principal e o bloco `RETRATO DO ARQUIVO LIMPO`.**
Esse bloco precisa ser o último do `<body>`. Ele tira a cópia do documento antes
de o app desenhar a primeira coisa, e só então chama `aplicarVersaoDinamica()`,
`gerarMockData()`, `initRoletas()`, `atualizarTodasRoletas()` e
`alternarModoFluxo('grade')`.
Qualquer `<script>`, `defer` ou imagem grande colocado nessa fresta passa a rodar
antes do retrato. O retrato é tirado uma única vez, então o arquivo sairia sujo
em **todo** export daquela sessão — e ninguém perceberia."""


def aplica(caminho, antigo, novo, rotulo):
    with io.open(caminho, encoding="utf-8", newline="") as f:
        txt = f.read()
    if txt.count(antigo) != 1:
        print("ABORTADO em %s: '%s' apareceu %d vez(es)." % (caminho, rotulo, txt.count(antigo)))
        return False
    with io.open(caminho, "w", encoding="utf-8", newline="") as f:
        f.write(txt.replace(antigo, novo, 1))
    print("  %s: %s OK" % (os.path.basename(caminho), rotulo))
    return True


def main():
    ok = aplica(os.path.join(RAIZ, "index.html"), INDEX_ANTIGO, INDEX_NOVO,
                "bloco do retrato")
    ok = aplica(os.path.join(RAIZ, "AGENTS.md"), AGENTS_ANTIGO, AGENTS_NOVO,
                "regra da fresta") and ok
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
