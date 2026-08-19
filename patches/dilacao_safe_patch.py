import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# ============================================================
# 1. SUBSTITUIR APENAS O CONTEUDO DO CARD DA ABA DE DILACAO
# ============================================================

old_card = '''    <div class="card calc-wrap">
        <h2>Calculadora de Dilacao</h2>
        <p class="subtitle">Calcule prazos de dilacao (30, 60 ou 90 dias)</p>
        <div class="dica-box"><strong>Dica:</strong> Cliente pode solicitar ate 90 dias corridos adicionais para regularizar.</div>
        <div class="campo"><label for="dataInicialDilacao">Data Base</label><div class="data-input-wrap"><input type="text" id="dataInicialDilacao" placeholder="DD/MM/AAAA" maxlength="10"><button type="button" class="btn-calendario" onclick="abrirCalendario('dataInicialDilacao')" title="Abrir calendario">📅</button></div></div>
        <div class="row"><div class="campo"><label for="quantidadeDilacao">Dias de Dilacao</label><select id="quantidadeDilacao"><option value="30">30 dias</option><option value="60" selected>60 dias</option><option value="90">90 dias</option></select></div><div class="campo"><label for="tipoDiasDilacao">Tipo de Dias</label><select id="tipoDiasDilacao"><option value="corridos" selected>Dias Corridos</option><option value="uteis">Dias Uteis</option></select></div></div>
        <button class="btn-calcular" onclick="calcularDilacao()">Calcular Data Final</button>
        <div id="resultadoDilacao"><h3>Resultado</h3><div class="data-final" id="dataFinalDilacao"></div><div class="info" id="infoAdicionalDilacao"></div></div>
        <div class="footer">v3.7</div>
    </div>'''

new_card = '''    <div class="card calc-wrap">
        <h2>Calculadora de Dilacao</h2>
        <p class="subtitle">Calcule prazos de dilacao em dias corridos</p>
        <div class="dica-box">
            <strong>Como usar:</strong><br>
            <strong>Dilacao simples</strong> — quando o cliente pede agora pela primeira vez. Escolha a data base e os dias (30, 60, 90 ou outro valor).<br><br>
            <strong>Caso especial</strong> — quando o cliente ja tinha pedido dilação antes e voce vai dar mais prazo agora. Coloque a data do pedido antigo e os dias totais que ele pediu. Aqui voce ve quanto tempo ja passou, quanto ainda falta, e quanto dar hoje (padrao: 90 dias). Tambem mostra quando vence esse prazo novo e quanto faltara pedir depois.
        </div>

        <!-- DILACAO SIMPLES -->
        <div class="secao-dilacao">
            <h3 class="secao-titulo">Dilacao Simples</h3>
            <div class="campo"><label for="dataInicialDilacao">Data Base</label><div class="data-input-wrap"><input type="text" id="dataInicialDilacao" placeholder="DD/MM/AAAA" maxlength="10"><button type="button" class="btn-calendario" onclick="abrirCalendario('dataInicialDilacao')" title="Abrir calendario">📅</button></div></div>
            <div class="campo"><label>Dias de Dilacao</label>
                <div class="botoes-dias-wrap">
                    <button type="button" class="btn-dia-rapido" onclick="setDiasDilacao(30)">30</button>
                    <button type="button" class="btn-dia-rapido" onclick="setDiasDilacao(60)">60</button>
                    <button type="button" class="btn-dia-rapido" onclick="setDiasDilacao(90)">90</button>
                    <input type="number" id="quantidadeDilacao" class="input-dias-manual" placeholder="Outro" min="1" oninput="validarDiasDilacao(this)">
                </div>
            </div>
            <button class="btn-calcular" onclick="calcularDilacao()">Calcular Data Final</button>
            <div id="resultadoDilacao"><h3>Resultado</h3><div class="data-final" id="dataFinalDilacao"></div><div class="info" id="infoAdicionalDilacao"></div></div>
        </div>

        <hr class="separador-dilacao">

        <!-- CASO ESPECIAL / DATA BASE EXTRA -->
        <div class="secao-dilacao">
            <h3 class="secao-titulo">Caso especial — dilação parcial</h3>
            <p class="secao-subtitle">Use quando o cliente ja tinha pedido dilacao antes e voce vai dar mais prazo agora.</p>
            <div class="campo"><label for="dataPedidoOriginal">Data do Pedido Original</label><div class="data-input-wrap"><input type="text" id="dataPedidoOriginal" placeholder="DD/MM/AAAA" maxlength="10"><button type="button" class="btn-calendario" onclick="abrirCalendario('dataPedidoOriginal')" title="Abrir calendario">📅</button></div></div>
            <div class="campo"><label for="diasTotaisSolicitados">Dias totais do pedido antigo</label><input type="number" id="diasTotaisSolicitados" placeholder="Ex: 365" min="1"></div>
            <div class="campo"><label for="diasConcederAgora">Dias para dar agora (padrao: 90)</label><input type="number" id="diasConcederAgora" value="90" min="1"></div>
            <button class="btn-calcular btn-calcular--secundario" onclick="calcularDilacaoCasoEspecial()">Calcular prazo parcial</button>
            <div id="resultadoCasoEspecial"><h3>Resultado do Caso Especial</h3>
                <div class="info-grid" id="gridCasoEspecial">
                    <div class="info-item"><span class="info-label">Dias decorridos ate hoje:</span><span class="info-valor" id="ceDecorridos">—</span></div>
                    <div class="info-item"><span class="info-label">Dias restantes do pedido original:</span><span class="info-valor" id="ceRestantes">—</span></div>
                    <div class="info-item"><span class="info-label">Dias concedidos agora:</span><span class="info-valor" id="ceConcedidos">—</span></div>
                    <div class="info-item"><span class="info-label">Quanto ainda falta pedir:</span><span class="info-valor" id="ceFaltarao">—</span></div>
                    <div class="info-item destaque"><span class="info-label">Data de vencimento (prazo atual):</span><span class="info-valor" id="ceVencimento">—</span></div>
                    <div class="info-item"><span class="info-label">Nova data base para proximo pedido:</span><span class="info-valor" id="ceNovaDataBase">—</span></div>
                </div>
            </div>
        </div>

        <div class="footer">v3.7</div>
    </div>'''

if old_card not in content:
    print('ERRO: Card original nao encontrado!')
    exit(1)

content = content.replace(old_card, new_card)
print('Card da dilacao substituido com sucesso.')

# ============================================================
# 2. ADICIONAR CSS MINIMO NO LOCAL APROPRIADO
# ============================================================

css_novo = '''.dica-box strong{color:#002752}

/* ===== CALCULADORA DE DILACAO ===== */
.secao-dilacao{margin-bottom:24px}
.secao-titulo{font-size:1.05rem;color:#343a40;margin-bottom:10px;margin-top:4px;border-bottom:2px solid #e9ecef;padding-bottom:6px}
.secao-subtitle{color:#6c757d;font-size:.85rem;margin-bottom:14px;margin-top:-6px}
.botoes-dias-wrap{display:flex;gap:8px;align-items:center}
.btn-dia-rapido{flex:1;padding:10px 8px;font-size:.95rem;font-weight:700;color:#495057;background:#f8f9fa;border:2px solid #dee2e6;border-radius:8px;cursor:pointer;transition:all .2s;font-family:inherit}
.btn-dia-rapido:hover{background:#e9ecef;border-color:#adb5bd}
.btn-dia-rapido.ativo{background:#007bff;color:white;border-color:#007bff}
.input-dias-manual{width:90px;padding:10px 12px;font-size:.95rem;border:2px solid #dee2e6;border-radius:8px;outline:none;text-align:center;font-family:inherit}
.input-dias-manual:focus{border-color:#007bff}
.separador-dilacao{border:none;border-top:1px solid #dee2e6;margin:24px 0}
.btn-calcular--secundario{background:#007bff}
.btn-calcular--secundario:hover{background:#0056b3}
#resultadoCasoEspecial{display:none;margin-top:22px;padding:20px;background:#f8f9fa;border-radius:10px;border-left:4px solid #28a745}
#resultadoCasoEspecial h3{font-size:1rem;color:#343a40;margin-bottom:14px}
.info-grid{display:grid;gap:10px}
.info-item{display:flex;justify-content:space-between;align-items:center;padding:10px 14px;background:white;border-radius:8px;border:1px solid #e9ecef}
.info-item.destaque{border-color:#28a745;background:#eafaf1}
.info-label{font-size:.85rem;color:#6c757d}
.info-valor{font-size:.95rem;font-weight:700;color:#343a40}
.info-item.destaque .info-valor{color:#155724;font-size:1.05rem}'''

# Inserir CSS logo apos .dica-box strong{color:#002752}
old_css_anchor = '.dica-box strong{color:#002752}'
if old_css_anchor in content:
    content = content.replace(old_css_anchor, css_novo)
    print('CSS adicionado com sucesso.')
else:
    print('AVISO: Ancora CSS nao encontrada, CSS nao inserido.')

# ============================================================
# 3. ADICIONAR JS NOVAS FUNCOES APOS calcularDilacao() EXISTENTE
# ============================================================

js_novo = '''// ===== ABA 2: DILACAO - FUNCOES NOVAS =====
function setDiasDilacao(valor) {
    document.getElementById('quantidadeDilacao').value = valor;
    document.querySelectorAll('.btn-dia-rapido').forEach(btn => btn.classList.remove('ativo'));
    const btn = Array.from(document.querySelectorAll('.btn-dia-rapido')).find(b => parseInt(b.textContent) === valor);
    if (btn) btn.classList.add('ativo');
}
function validarDiasDilacao(input) {
    const val = parseInt(input.value);
    if (isNaN(val) || val < 1) input.value = '';
    else { document.querySelectorAll('.btn-dia-rapido').forEach(btn => btn.classList.remove('ativo')); }
}
function calcularDiferencaDias(dataInicio, dataFim) {
    const d1 = new Date(dataInicio + 'T12:00:00');
    const d2 = new Date(dataFim + 'T12:00:00');
    const diff = Math.round((d2 - d1) / (1000 * 60 * 60 * 24));
    return diff;
}
function calcularDilacaoCasoEspecial() {
    const dataPedidoTxt = document.getElementById('dataPedidoOriginal').value;
    const dataPedido = textoParaISODate(dataPedidoTxt);
    const diasTotais = parseInt(document.getElementById('diasTotaisSolicitados').value);
    const diasConceder = parseInt(document.getElementById('diasConcederAgora').value);
    if (!dataPedido || isNaN(diasTotais) || diasTotais < 1 || isNaN(diasConceder) || diasConceder < 1) {
        alert('Preencha todos os campos do Caso Especial.'); return;
    }
    const hoje = new Date();
    const hojeIso = hoje.getFullYear() + '-' + String(hoje.getMonth()+1).padStart(2,'0') + '-' + String(hoje.getDate()).padStart(2,'0');
    const decorridos = calcularDiferencaDias(dataPedido, hojeIso);
    if (decorridos < 0) { alert('A data do pedido original nao pode ser no futuro.'); return; }
    const restantes = Math.max(0, diasTotais - decorridos);
    const faltarao = Math.max(0, restantes - diasConceder);
    const dataVencimento = new Date(hoje);
    dataVencimento.setDate(dataVencimento.getDate() + diasConceder);
    const novaDataBase = new Date(dataVencimento);
    document.getElementById('ceDecorridos').textContent = decorridos + ' dia(s)';
    document.getElementById('ceRestantes').textContent = restantes + ' dia(s)';
    document.getElementById('ceConcedidos').textContent = diasConceder + ' dia(s)';
    document.getElementById('ceFaltarao').textContent = faltarao + ' dia(s)';
    document.getElementById('ceVencimento').textContent = dataVencimento.toLocaleDateString('pt-BR',{weekday:'long',year:'numeric',month:'long',day:'numeric'});
    document.getElementById('ceNovaDataBase').textContent = novaDataBase.toLocaleDateString('pt-BR');
    document.getElementById('resultadoCasoEspecial').style.display = 'block';
}
'''

# Inserir JS apos a funcao calcularDilacao() existente
# Procurar o fim da funcao calcularDilacao()
js_anchor = "document.getElementById('resultadoDilacao').style.display = 'block';\n}\n\n// ===== ABA 4: MATRICULAS ====="
if js_anchor in content:
    content = content.replace(js_anchor, "document.getElementById('resultadoDilacao').style.display = 'block';\n}\n\n" + js_novo + "\n// ===== ABA 4: MATRICULAS =====")
    print('JS adicionado com sucesso.')
else:
    print('AVISO: Ancora JS nao encontrada, tentando localizacao alternativa...')
    # Fallback: procurar o final da funcao calcularDilacao de outra forma
    pass

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print('\\nTudo pronto! Alteracoes aplicadas APENAS dentro do card da dilacao.')
