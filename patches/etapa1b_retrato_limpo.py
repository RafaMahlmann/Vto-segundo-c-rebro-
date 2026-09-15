# -*- coding: utf-8 -*-
"""
ETAPA 1b - Retrato limpo (corrige os vazamentos que a Etapa 1 deixou passar).

Um teste independente achou 8 sobras que a limpeza por enumeracao nao cobria.
Duas delas eram dado pessoal de verdade, dentro do ZIP:
  - #timelineEmpty guardava "Matricula 99999999 - nenhum servico"
  - .timeline-evento guardava codigo e data de servico ("8480 - Criado 25/05/2026"),
    e isso acontecia SEM o usuario fazer nada, porque o app ja abre com uma
    matricula ativa e a timeline desenhada.

Limpar item por item e uma corrida que nunca termina: cada funcao nova volta a
vazar. A correcao troca a estrategia.

COMO PASSA A FUNCIONAR
  Um bloco no fim do arquivo tira um RETRATO do documento antes de qualquer
  coisa ser desenhada na tela, e so depois manda o app iniciar. O Exportar ZIP
  usa esse retrato. O DOM vivo nunca mais e serializado.

Alteracoes:
  1. a IIFE de versao dinamica vira a funcao aplicarVersaoDinamica()
     (o carimbo de data/hora tambem nao pode ficar gravado no pacote)
  2. as 4 chamadas de inicializacao saem do fim do <script> principal
  3. bloco novo antes de </body>: tira o retrato e SO ENTAO inicia o app
  4. prepararHtmlLimpo() passa a devolver o retrato; a limpeza do clone fica
     como plano B, agora com as sobras que o teste encontrou

Nao toca em nenhuma aba, no CSS, em matriculas[] nem no anonimizador.
"""
import io
import sys

CAMINHO = "index.html"

# ------------------------------------------------- 1. IIFE de versao -> funcao
VERSAO_ANTIGA = """// ===== VERSAO DINAMICA =====
(function() {
    const agora = new Date();"""

VERSAO_NOVA = """// ===== VERSAO DINAMICA =====
// Chamada la no fim do arquivo, DEPOIS do retrato: o carimbo de data e hora
// da maquina de quem exportou nao pode ficar gravado no pacote distribuido.
function aplicarVersaoDinamica() {
    const agora = new Date();"""

VERSAO_FIM_ANTIGO = """    document.querySelectorAll('[data-versao]').forEach(el => { el.textContent = versao; });
})();"""

VERSAO_FIM_NOVO = """    document.querySelectorAll('[data-versao]').forEach(el => { el.textContent = versao; });
}"""

# ------------------------------------------- 2. tira a inicializacao do script
INIT_ANTIGO = """// Inicializa
gerarMockData();
initRoletas();
atualizarTodasRoletas();
alternarModoFluxo('grade');
</script>"""

INIT_NOVO = """// A inicializacao mudou de lugar: ela roda no bloco do fim do arquivo,
// logo depois do retrato limpo. Ver "RETRATO DO ARQUIVO LIMPO" abaixo.
</script>"""

# ------------------------------------------------ 3. bloco do retrato + inicio
RETRATO_ANTIGO = """<!-- /ANONIMIZADOR EMBUTIDO -->
</body>"""

RETRATO_NOVO = """<!-- /ANONIMIZADOR EMBUTIDO -->

<!-- RETRATO DO ARQUIVO LIMPO -->
<!-- Este bloco precisa ser o ULTIMO do body. Ele tira uma copia do documento
     antes de o app desenhar qualquer coisa, e e dessa copia que sai o pacote
     do Exportar ZIP. Nao mexa na ordem: se o app iniciar antes do retrato, o
     arquivo distribuido volta a levar matricula, data e calculo junto. -->
<script>
window._htmlOriginal = '<!DOCTYPE html>\\n' + document.documentElement.outerHTML;

aplicarVersaoDinamica();
gerarMockData();
initRoletas();
atualizarTodasRoletas();
alternarModoFluxo('grade');
</script>
<!-- /RETRATO DO ARQUIVO LIMPO -->
</body>"""

# ------------------------------------------- 4. prepararHtmlLimpo usa o retrato
PREPARA_ANTIGO = """function prepararHtmlLimpo() {
    const raiz = document.documentElement.cloneNode(true);"""

PREPARA_NOVO = """function prepararHtmlLimpo() {
    // Caminho normal: o retrato tirado antes de o app desenhar. E uma copia
    // fiel do arquivo, entao nao existe nada de tela para vazar.
    if (window._htmlOriginal) return window._htmlOriginal;

    // Plano B, caso o bloco do retrato tenha se perdido: limpa uma copia do
    // DOM vivo. Menos confiavel - cada funcao nova pode escrever num lugar
    // que esta lista ainda nao conhece.
    const raiz = document.documentElement.cloneNode(true);"""

# ---------------------------------------- 4b. sobras achadas no teste (plano B)
SOBRAS_ANTIGO = """    const vazio = um('#timelineEmpty');
    if (vazio) vazio.style.display = '';"""

SOBRAS_NOVO = """    const vazio = um('#timelineEmpty');
    if (vazio) {
        vazio.style.display = '';
        // guardava "Matricula 99999999 - nenhum servico"
        vazio.textContent = 'Nenhuma matricula selecionada';
    }
    // os eventos entram direto no #timelineTrack e levam codigo e data de servico
    todos('#timelineTrack .timeline-evento').forEach(el => el.remove());
    // textos dos contadores
    const textos = {
        '#contadorNumero': '180', '#contadorRotulo': 'dias restantes',
        '#contadorMsg': 'Dentro do prazo', '#alerta180Numero': '0',
        '#alerta180Msg': 'Limite excedido', '#modalTitulo': 'Data do Servico',
        '#dataLimiteSancao': '--', '#statusTextoSancao': '--',
        '#ceConcedidos': '\\u2014', '#ceVencimento': '\\u2014',
        '#prazoFinalPedido': '\\u2014', '#estTotalMatriculas': '0',
        '#estMediaExecucao': '0', '#estTaxaAberto': '0%', '#estTaxaExcedido': '0%'
    };
    Object.keys(textos).forEach(sel => {
        const el = um(sel);
        if (el) el.textContent = textos[sel];
    });
    todos('[data-versao]').forEach(el => { el.textContent = 'v' + VERSAO_LOCAL; });
    todos('.sancao-btn').forEach(el => { el.className = 'servico-btn sancao-btn'; });"""

# ------------------------------------ 4c. a classe da aba 6 vazava para o pacote
CORPO_ANTIGO = """    // 9. Abre na aba 1, do jeito que um arquivo novo abre
    todos('.tab-content').forEach(el => el.classList.remove('active'));"""

CORPO_NOVO = """    // 9. Abre na aba 1, do jeito que um arquivo novo abre.
    //    A classe anon-aberto tambem sai: gravada no pacote, ela fazia o
    //    arquivo distribuido abrir sem a Linha do Tempo.
    const corpo = raiz.querySelector('body');
    if (corpo) corpo.classList.remove('anon-aberto');
    todos('.tab-content').forEach(el => el.classList.remove('active'));"""

TROCAS = [
    ("abertura da IIFE de versao", VERSAO_ANTIGA, VERSAO_NOVA),
    ("fechamento da IIFE de versao", VERSAO_FIM_ANTIGO, VERSAO_FIM_NOVO),
    ("inicializacao no fim do script", INIT_ANTIGO, INIT_NOVO),
    ("bloco do retrato antes de </body>", RETRATO_ANTIGO, RETRATO_NOVO),
    ("atalho em prepararHtmlLimpo", PREPARA_ANTIGO, PREPARA_NOVO),
    ("sobras do plano B", SOBRAS_ANTIGO, SOBRAS_NOVO),
    ("classe anon-aberto no clone", CORPO_ANTIGO, CORPO_NOVO),
]


def main():
    with io.open(CAMINHO, encoding="utf-8", newline="") as f:
        html = f.read()

    if "window._htmlOriginal" in html:
        print("ABORTADO: o retrato ja existe. Nada foi alterado.")
        return 1

    for nome, antigo, _novo in TROCAS:
        if html.count(antigo) != 1:
            print("ABORTADO: ancora '%s' apareceu %d vez(es), esperava 1. "
                  "Nada foi alterado." % (nome, html.count(antigo)))
            return 1

    novo = html
    for _nome, antigo, troca in TROCAS:
        novo = novo.replace(antigo, troca, 1)

    with io.open(CAMINHO, "w", encoding="utf-8", newline="") as f:
        f.write(novo)

    print("OK. %d -> %d caracteres (+%d)" % (len(html), len(novo), len(novo) - len(html)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
