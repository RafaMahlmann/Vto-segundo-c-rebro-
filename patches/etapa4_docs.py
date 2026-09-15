# -*- coding: utf-8 -*-
"""
ETAPA 4 - Atualiza os documentos para o mapa novo.

Documento divergente e o que faz a proxima sessao de IA "corrigir" o codigo
certo. O AGENTS.md ainda falava em 5 abas, 2.430 linhas e v3.7.

Mexe em: AGENTS.md, TIMELINE.md, README.md.
Nao toca em index.html, anonimizador.html, sw.js nem version.json.
"""
import io
import os
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VERSAO = "4.4"


def aplica(nome, trocas, acrescimo=None):
    caminho = os.path.join(RAIZ, nome)
    with io.open(caminho, encoding="utf-8", newline="") as f:
        txt = f.read()
    antes = txt
    for rotulo, antigo, novo in trocas:
        if txt.count(antigo) != 1:
            print("  ABORTADO em %s: '%s' apareceu %d vez(es)."
                  % (nome, rotulo, txt.count(antigo)))
            return False
        txt = txt.replace(antigo, novo, 1)
    if acrescimo:
        txt = txt.rstrip("\n") + "\n" + acrescimo
    if txt == antes:
        print("  %s: nada a mudar" % nome)
        return True
    with io.open(caminho, "w", encoding="utf-8", newline="") as f:
        f.write(txt)
    print("  %s: %d troca(s) aplicada(s)" % (nome, len(trocas)))
    return True


AGENTS = [
    ("tamanho do arquivo",
     "- `index.html` **é o aplicativo inteiro**: ~2.430 linhas / ~147 KB, HTML + CSS + JS monobloco.",
     "- `index.html` **é o aplicativo inteiro**: ~3.110 linhas / ~263 KB, HTML + CSS + JS monobloco.\n"
     "- Desses 263 KB, ~96 KB são o **anonimizador embutido em Base64** (`<script id=\"anonimizadorFonte\">`)."),
    ("lista de abas",
     "- 5 abas: `prazo` (Calculadora de Sanção de Esgoto), `dilacao`, `fluxo`, `matriculas`, `estatisticas`.",
     "- 6 abas: `prazo` (Calculadora de Sanção de Esgoto), `dilacao`, `fluxo`, `matriculas`, `estatisticas`, `anonimizador`.\n"
     "- A aba 6 roda o **Anonimizador LGPD v19** dentro de um `iframe srcdoc`, alimentado pelo Base64 embutido.\n"
     "  **Não existe dependência de arquivo irmão.** O `anonimizador.html` da raiz é só a fonte de edição."),
    ("divergencias de versao",
     "  - README.md e TIMELINE.md dizem \"v3.2\"; o app está em **v3.7**.",
     "  - O app está em **v%s** (título, badge, 4 rodapés, `VERSAO_LOCAL`, `sw.js` e `version.json` sobem juntos)." % VERSAO),
    ("mapa: aba 5",
     "| `<!-- ABA 5 -->` | 623–708 | Estatísticas (Canvas) |",
     "| `<!-- ABA 5 -->` | ~690–745 | Estatísticas (Canvas) |\n"
     "| `<!-- ABA 6: ANONIMIZADOR -->` | ~747–757 | `iframe#anonimizadorFrame` (sem `src`) + aviso de falha |"),
    ("mapa: sistema de abas",
     "| `// ===== SISTEMA DE ABAS =====` | 813+ | `mostrarAba()` + auto-foco por aba |",
     "| `// ===== SISTEMA DE ABAS =====` | ~904+ | `mostrarAba()` + auto-foco + carrega a aba 6 sob demanda |\n"
     "| `// ===== ABA 6: ANONIMIZADOR EMBUTIDO =====` | ~922+ | `carregarAnonimizador()` — decodifica o Base64 para o `srcdoc` |"),
    ("mapa: exportar",
     "| `// ===== EXPORTAR/IMPORTAR =====` | 2146+ | CSV e JSON |",
     "| `// ===== EXPORTAR/IMPORTAR =====` | ~2420+ | CSV e JSON |\n"
     "| `// ===== GERAR ZIP PORTATIL =====` | ~2728+ | `prepararHtmlLimpo()` + `gerarZipCompleto()` + `criarZipMulti()` |"),
    ("mapa: verificador",
     "| `// ===== VERIFICADOR DE NOVA VERSAO =====` | 2398+ | Único `fetch()` autorizado (lê `version.json` do GitHub) |",
     "| `// ===== VERIFICADOR DE NOVA VERSAO =====` | ~2661+ | Único `fetch()` autorizado + `versaoEhMaior()` |"),
    ("rodape do documento",
     "*Criado em 2026-08-19 após análise dos incidentes das sessões anteriores. App em v3.7.*",
     "*Criado em 2026-08-19 após análise dos incidentes das sessões anteriores. Atualizado em 2026-09-14. App em v%s.*" % VERSAO),
]

AGENTS_EXTRA = """
---

## 9. Duas regras que nasceram da Etapa 1–4 (2026-09-14)

**O export NÃO pode serializar o DOM vivo.**
`gerarZipCompleto()` usa `prepararHtmlLimpo()`, que clona o documento e apaga
tudo que foi gerado na tela antes de empacotar. Sem isso o arquivo distribuído
levava as matrículas em texto claro — incidente de LGPD — e duplicava as setas
das roletas a cada ciclo exportar/reabrir.
Mexeu em algo que é renderizado em tempo de execução? Acrescente a limpeza
correspondente em `prepararHtmlLimpo()`.

**Editou o `anonimizador.html`? Rode `patches/embutir_anonimizador.py`.**
A aba 6 e o ZIP leem os dois do mesmo bloco Base64. Sem regerar, a aba mostra a
versão nova e o pacote distribui a velha — e a v18.2.2 do anonimizador foi
reprovada em pentest. O script deixa o Base64 byte a byte igual ao arquivo em
disco, então dá para conferir a qualquer momento.
"""

TIMELINE_EXTRA = """
---

## PARTE 9 — Fusão VTO + Anonimizador (2026-09-14, v%s)

Quatro etapas para transformar os dois monoblocos num arquivo só.

**Etapa 1 — Export limpo (LGPD).**
`gerarZipCompleto()` serializava o DOM vivo: o `index.html` distribuído saía com
as 30 matrículas gravadas em texto claro e 43 KB de HTML gerado em tela.
Nasceu `prepararHtmlLimpo()`, que clona o documento e limpa antes de empacotar.
O botão agora também confirma antes de baixar.
Medido: 0 matrículas no pacote, exportado voltou ao tamanho do arquivo em disco.

**Etapa 2 — Arquivo único.**
A aba 6 era `<iframe src="anonimizador.html">`: sem o arquivo irmão do lado,
abria em branco e calada. Passou a ser `iframe srcdoc` alimentado pelo Base64 já
embutido, carregado sob demanda, com aviso visível se o bloco falhar.
De quebra: o `.header` do anonimizador nunca era fechado (37 `<div>` para 36
`</div>`), e o app inteiro renderizava dentro de um cabeçalho `display:flex` —
era essa a causa do layout espremido, e não o iframe.
O `patches/embutir_anonimizador.py` foi desarmado: ele reescrevia o
`gerarZipCompleto()` com a versão antiga e teria desfeito a Etapa 1.

**Etapa 3 — Versão e banner.**
Tudo subiu junto para v%s. E a checagem do banner virou `versaoEhMaior()`:
antes era "diferente de", então qualquer descompasso ligava o aviso de nova
versão — inclusive para quem tinha acabado de baixar a versão nova.

**Etapa 4 — Higiene.**
Scripts de teste soltos na raiz foram para `patches/testes_antigos/`.
Documentos atualizados para o mapa de 6 abas.

Teste automatizado da entrega: `patches/_test_etapa1.py` (21 verificações).
""" % (VERSAO, VERSAO)

README = [
    ("versao atual",
     "- **Versao Atual:** 3.9 (Sancao de Esgoto + Dilacao parcial + Banner de versao)",
     "- **Versao Atual:** %s (6 abas; Anonimizador LGPD embutido; export sem dado pessoal)" % VERSAO),
]


def main():
    print("Atualizando documentos para v%s" % VERSAO)
    ok = True
    ok &= aplica("AGENTS.md", AGENTS, AGENTS_EXTRA)
    ok &= aplica("TIMELINE.md", [], TIMELINE_EXTRA)
    ok &= aplica("README.md", README)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
