with open('index.html', 'r', encoding='utf-8') as f:
    s = f.read()

old_resposta = '''                <div class="resposta-gerada-wrap" id="respostaGeradaWrap">
                    <div class="resposta-gerada-header">
                        <span>Resposta para o cliente</span>
                        <button type="button" class="btn-copiar" onclick="copiarRespostaCasoEspecial()">Copiar texto</button>
                    </div>
                    <textarea id="respostaCasoEspecial" class="resposta-gerada-texto" readonly></textarea>
                </div>'''

new_resposta = '''                <div class="card-resposta" id="cardResposta">
                    <div class="card-resposta-header">
                        <span class="card-resposta-titulo">Resposta para o cliente</span>
                        <div class="mini-tabs">
                            <button type="button" class="mini-tab" id="tabM1" onclick="mostrarModeloResposta(1)">Modelo 1</button>
                            <button type="button" class="mini-tab" id="tabM2" onclick="mostrarModeloResposta(2)">Modelo 2</button>
                        </div>
                    </div>
                    <div class="card-resposta-body">
                        <div class="modelo-resposta" id="modelo1">
                            <textarea id="respostaModelo1" readonly></textarea>
                            <div style="text-align:right;margin-top:8px">
                                <button type="button" class="btn-copiar" onclick="copiarTexto('respostaModelo1')">Copiar Modelo 1</button>
                            </div>
                        </div>
                        <div class="modelo-resposta" id="modelo2">
                            <textarea id="respostaModelo2" readonly></textarea>
                            <div style="text-align:right;margin-top:8px">
                                <button type="button" class="btn-copiar" onclick="copiarTexto('respostaModelo2')">Copiar Modelo 2</button>
                            </div>
                        </div>
                    </div>
                </div>'''

s = s.replace(old_resposta, new_resposta)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(s)

print('Etapa 3 (HTML com card laranja e abinhas M1/M2) concluida.')
