# Pesquisa: seletor de colunas com miniaturas — Anonimizador LGPD v19

Data: 2026-10-07 · Escopo: `anonimizador.html` (fonte da aba 6 do VTO)

---

## 1. Panorama externo — como os consagrados resolvem

**Power Query ("Escolher Colunas")** — abre uma caixa de diálogo com lista de caixas de seleção, "selecionar tudo" implícito e, no caminho "Ir para Coluna", busca direta pelo nome. Lição: lista com checkbox + busca vence qualquer grade quando são 100+ itens.
Fonte: iterationinsights.com / learn.microsoft.com/power-query/best-practices.

**Power Query (modo "Remover Outras Colunas")** — a Microsoft recomenda pensar "estas são as colunas que quero manter" em vez de "remover as que não quero": seleção positiva é mais segura quando entra coluna nova.
Fonte: iterationinsights.com/article/removing-columns-in-power-query-editor.

**ARX Data Anonymization Tool** — cada coluna recebe um "tipo" (identificante, quasi-identificante, sensível, insensível) marcado por uma bolinha colorida ao lado do nome; desde a v3.7.0 há botões para aplicar um tipo a TODAS as colunas de uma vez. Lição: papel por coluna + cor + ação global é exatamente o modelo mental do nosso chip — o ARX só adiciona a ação em massa.
Fonte: arx.deidentifier.org/anonymization-tool/configuration.

**Amnesia (OpenAIRE)** — wizard em 5 passos; no passo 2 a pessoa escolhe os campos vendo uma prévia da tabela original. Lição: "selecionar e pré-visualizar" no mesmo lugar; não se decide coluna às cegas.
Fonte: openaire.eu/discover-amnesia-anonymity-for-your-data; amnesia.openaire.eu.

**Google Photos / Lightroom / Explorador de Arquivos** — grade de miniaturas com seleção múltipla: clique marca, Shift marca intervalo, Ctrl marca avulso, e uma barra de ações em massa aparece só quando há seleção. Lightroom ainda mostra metadado (nome, data) em cada cartão. Lição: a miniatura carrega contexto (amostra do dado), e a ação em massa fica contextual.

**Frappe (diálogo "Select Table Columns")** — issue real pedindo "Select All / Unselect All" porque marcar coluna por coluna é "time-consuming and inefficient". Lição: até framework maduro sofre sem seleção em massa; é a dor nº 1 documentada.
Fonte: github.com/frappe/frappe/issues/36066.

## 2. Padrões de informação que importam aqui

1. **Revelação progressiva**: 159 colunas de uma vez assusta. Agrupar (Identidade / Endereço / Hidrômetro / Consumo / Faturamento) e mostrar grupos fechados, com contador ("12 de 159 visíveis").
2. **Ações em massa sempre visíveis**: "Manter todas", "Excluir todas", "Excluir não selecionadas". O preset Power Query já prova o valor: um clique economiza ~600 cliques.
3. **Decidir vendo amostra**: 2–3 valores reais da coluna (mascarados na tela se sensível) valem mais que o nome técnico ("CONSMED 7" não diz nada; "38, 41, 39" diz).
4. **Busca antes de rolagem**: com 159 itens, rolar é falha de design; filtrar por texto é uma linha de `includes()`.
5. **Seleção positiva**: pensar "quais eu quero" (e excluir o resto) é mais seguro para LGPD que "quais eu tiro" — coluna nova entra excluída por padrão.

## 3. Estado atual do app (lido no código)

Correção ao briefing: não são 156, são **159 colunas** no modo TXT — `PONTOS_CORTE_TXT` (linha 620) tem 160 cortes e `MAPA_NOMES_TXT` (linha 633) nomeia as 159. Sem duplicatas, cortes crescentes, nenhuma coluna órfã. Mapa em si está saudável.

**O que dá para reaproveitar:**
- `COLUNAS_DETECTADAS` (array `{id, nome, estado}`, linha 858) é a fonte única da verdade — qualquer painel novo só lê/escreve nela e chama `atualizarVisualChip` (linha 878) para redesenhar. Não precisa mexer no motor de processamento.
- `adicionarColunaInterface` (857), `alternarEstado` (867) e as classes `.chip-*` (186–196) já dão o ciclo de 5 estados com cor. Um painel de miniaturas seria uma SEGUNDA visão sobre os mesmos dados.
- `tipoSimulacao` (676), `TERMOS_SENSIVEIS` (690) e `extrairCampoTxt` (944) já classificam e extraem valores — tudo pronto para gerar amostras por coluna.
- O container `#chipsContainer` (307) fica em `#columnManager` (280), ponto natural para pendurar uma barra de ferramentas (busca + selecionar tudo) e um botão "ver como grade".

**Bugs e falhas reais encontrados:**
1. **Falso positivo de sensibilidade (o mais grave)**: `TERMOS_SENSIVEIS` contém `"NOME"` e `verificarSensibilidade` (844) usa `includes`. Resultado: `NOME-BAIRRO` (127), `NOME-FONTE` (131), `NOME-RESERVA` (132) e `NOME-ENDER-ALT` (150) nascem como 👻 Anonimizar (hash). São nomes geográficos, não pessoais — hasheá-los destrói o mapa/estatística sem ganho de LGPD. Se a pessoa não perceber e não usar o preset, o dado morre em silêncio.
2. **Ciclo de estados pune o erro**: levar uma coluna de Manter até Excluir custa 4 cliques (`alternarEstado`, 870–874); um clique errado a mais volta ao início e recomeça. Em CSV, de Dublê (3) pula direto para Excluir (0).
3. **Preset com efeito colateral**: `aplicarPresetSGCG` (920) reescreve `col.nome` do id 24 ("ECO-AGUA pop" → "pub") — mutação de dado escondida num botão visual.
4. **Só o primeiro arquivo manda**: `analisarArquivoInicial` (777) analisa `files[0]` e aplica as colunas a todos. Se um arquivo do lote tiver layout diferente, o corte erra em silêncio.
5. **Encoding de borda**: `detectarEncoding` (763) decodifica 64 KB com `fatal:true`; um caractere UTF-8 cortado no byte 65536 dá falso negativo e o arquivo inteiro é lido como windows-1252.

**O que falta (confirmado por ausência no código)**: sem seleção múltipla, sem "selecionar tudo", sem busca/filtro, sem amostra de dados por coluna, sem agrupamento. O container rola 350 px (CSS linha 182) — 159 chips numa grade de ~7 por linha dão ~23 telas de rolagem.

## 4. Capacidades ranqueadas (valor × esforço)

1. **Barra de ações em massa** — "Manter todas / Excluir todas / Excluir não marcadas" operando sobre `COLUNAS_DETECTADAS`. Altíssimo valor, esforço mínimo (um `forEach` + `atualizarVisualChip`).
2. **Busca/filtro de colunas por nome** — input que esconde chips com `display:none`. Essencial com 159 itens; trivial em vanilla JS.
3. **Seleção múltipla com ação conjunta** — checkbox em cada chip/cartão + "aplicar estado X nas selecionadas". Resolve o "4 cliques por coluna".
4. **Agrupamento por família** — dobrar as 159 colunas em ~8 grupos (prefixos de `MAPA_NOMES_TXT`: ECO-, CONSMED, SIT-FATURA, DT-, CODOPE…). HTML `<details>` resolve sem dependência.
5. **Miniatura com amostra de dados** — cartão por coluna com 2–3 valores reais lidos via `extrairCampoTxt` das primeiras linhas do arquivo (já está em memória no modo CSV; no TXT, ler um slice pequeno). Maior valor de decisão, esforço médio (nova renderização paralela).
6. **Corrigir o falso positivo "NOME"** — trocar `includes("NOME")` por correspondência exata de lista. Uma linha, evita destruir dado geográfico.
7. **Contador de estados** — "3 manter · 12 simular · 144 excluídas" no topo. Dá confiança antes de processar; quase grátis.

Restrições respeitadas: tudo roda em JS puro dentro do `anonimizador.html`, sem lib, sem fetch, sem localStorage, sem acento em identificadores.

## Fontes

- https://iterationinsights.com/article/removing-columns-in-power-query-editor/
- https://learn.microsoft.com/en-us/power-query/best-practices
- https://arx.deidentifier.org/anonymization-tool/configuration/
- https://www.openaire.eu/discover-amnesia-anonymity-for-your-data
- https://amnesia.openaire.eu/ (fact sheet OpenAIRE)
- https://github.com/frappe/frappe/issues/36066
- Código: `anonimizador.html` linhas 180–197, 260–340, 620–692, 763–933, 944–948 (leitura própria)
