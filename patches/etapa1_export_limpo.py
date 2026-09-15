# -*- coding: utf-8 -*-
"""
ETAPA 1 - Export limpo.

Problema: gerarZipCompleto() serializava o DOM VIVO. Tudo que estava na tela
(matriculas, timeline, setas de roleta, banner de versao) era gravado dentro
do index.html distribuido. Com dados reais isso vira vazamento de dado pessoal.

Correcao cirurgica, so na secao // ===== GERAR ZIP PORTATIL =====:
  1. nova funcao prepararHtmlLimpo() - clona o documento e apaga o que foi
     gerado em tempo de execucao (tudo isso e refeito no load do arquivo novo);
  2. gerarZipCompleto() passa a usar essa copia limpa e a confirmar com o
     usuario antes de baixar.

Nao toca em mais nada do arquivo.
"""
import io
import sys

CAMINHO = "index.html"

ANCORA_FUNCAO = "function gerarZipCompleto() {"

CABECA_ANTIGA = r"""function gerarZipCompleto() {
    const btn = document.querySelector('.btn-zip');
    const original = btn ? btn.textContent : 'Exportar ZIP';
    if (btn) btn.textContent = '...';

    // Coleta HTML do VTO (DOM atual)
    let htmlVto = '<!DOCTYPE html>\n' + document.documentElement.outerHTML;
"""

CABECA_NOVA = r"""function gerarZipCompleto() {
    const seguir = confirm('O pacote vai levar o aplicativo vazio.\n\n'
        + 'As matriculas que estao na tela agora NAO vao junto no arquivo.\n\n'
        + 'Gerar o ZIP?');
    if (!seguir) return;

    const btn = document.querySelector('.btn-zip');
    const original = btn ? btn.textContent : 'Exportar ZIP';
    if (btn) btn.textContent = '...';

    // Coleta HTML do VTO a partir de uma copia LIMPA do documento
    let htmlVto = prepararHtmlLimpo();
"""

FUNCAO_NOVA = r"""// Monta o HTML de distribuicao a partir de uma copia limpa do documento.
// O arquivo exportado nao pode levar o que foi gerado na tela: matricula e
// dado pessoal, e as setas de roleta duplicam a cada exportar/reabrir.
// Tudo que e apagado aqui volta sozinho quando o arquivo novo abre.
function prepararHtmlLimpo() {
    const raiz = document.documentElement.cloneNode(true);
    const um = sel => raiz.querySelector(sel);
    const todos = sel => raiz.querySelectorAll(sel);

    // 1. Tabela de matriculas - renderMatriculas() refaz no load
    const lista = um('#listaMatriculas');
    if (lista) lista.innerHTML = '';
    ['resTotal', 'resOk', 'resAlerta', 'resCritico'].forEach(id => {
        const el = um('#' + id);
        if (el) el.textContent = '0';
    });

    // 2. Matricula ativa gravada nos cards do fluxo
    todos('.matriculaAtivaCard').forEach(el => { el.textContent = 'Nenhuma'; });
    const inputCard = um('#matriculaInputCard1');
    if (inputCard) inputCard.removeAttribute('value');

    // 3. Timeline inferior - atualizarTimeline() refaz no load
    ['#timelineFases', '#timelineBarras', '#timelineMarcos'].forEach(sel => {
        const el = um(sel);
        if (el) el.innerHTML = '';
    });
    const trilho = um('#timelineTrack');
    if (trilho) trilho.style.display = 'none';
    const vazio = um('#timelineEmpty');
    if (vazio) vazio.style.display = '';
    ['#contador180', '#alerta180'].forEach(sel => {
        const el = um(sel);
        if (el) el.style.display = 'none';
    });

    // 4. Roletas do fluxo - initRoletas() refaz no load.
    //    Sem apagar, as setas aparecem em dobro a cada exportar/reabrir.
    todos('.roleta-nav').forEach(el => el.remove());
    todos('.roleta-grupo').forEach(el => el.classList.remove('roleta-armada'));

    // 5. Banner de nova versao
    const banner = um('#bannerVersao');
    if (banner) banner.classList.remove('ativo');
    const bannerTexto = um('#bannerVersaoTexto');
    if (bannerTexto) bannerTexto.textContent = '';
    const bannerBtn = um('#bannerBtnBaixar');
    if (bannerBtn) {
        bannerBtn.style.display = 'none';
        bannerBtn.textContent = 'Baixar vNova';
    }

    // 6. Modal (config e ajuda trocam o conteudo da caixa)
    const overlay = um('#modalOverlay');
    if (overlay) overlay.classList.remove('ativo');
    if (window._modalOriginal && overlay) {
        const caixa = overlay.querySelector('.modal-box');
        if (caixa) caixa.innerHTML = window._modalOriginal;
    }

    // 7. Resultados das calculadoras
    ['#resultadoPrazoSancao', '#resultadoDilacao'].forEach(sel => {
        const el = um(sel);
        if (el) el.style.display = 'none';
    });
    ['#dataFinalDilacao', '#infoAdicionalDilacao'].forEach(sel => {
        const el = um(sel);
        if (el) el.innerHTML = '';
    });
    todos('textarea').forEach(el => { el.textContent = ''; });

    // 8. Abre na aba 1, do jeito que um arquivo novo abre
    todos('.tab-content').forEach(el => el.classList.remove('active'));
    todos('.tab-btn').forEach(el => el.classList.remove('active'));
    const aba1 = um('#aba-prazo');
    if (aba1) aba1.classList.add('active');
    const btnAba1 = um('.tab-btn');
    if (btnAba1) btnAba1.classList.add('active');

    return '<!DOCTYPE html>\n' + raiz.outerHTML;
}

"""


def main():
    with io.open(CAMINHO, encoding="utf-8", newline="") as f:
        html = f.read()

    if "function prepararHtmlLimpo()" in html:
        print("ABORTADO: prepararHtmlLimpo() ja existe. Nada foi alterado.")
        return 1

    if html.count(CABECA_ANTIGA) != 1:
        print("ABORTADO: a cabeca de gerarZipCompleto() nao bateu exatamente "
              "(%d ocorrencias). Nada foi alterado." % html.count(CABECA_ANTIGA))
        return 1

    if html.count(ANCORA_FUNCAO) != 1:
        print("ABORTADO: ancora gerarZipCompleto nao e unica. Nada foi alterado.")
        return 1

    novo = html.replace(CABECA_ANTIGA, CABECA_NOVA, 1)
    novo = novo.replace(ANCORA_FUNCAO, FUNCAO_NOVA + ANCORA_FUNCAO, 1)

    with io.open(CAMINHO, "w", encoding="utf-8", newline="") as f:
        f.write(novo)

    print("OK. %d -> %d bytes (+%d)" % (len(html), len(novo), len(novo) - len(html)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
