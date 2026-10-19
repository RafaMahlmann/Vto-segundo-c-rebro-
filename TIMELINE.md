# Linha do Tempo de Trabalho — VTO Segundo Cerebro

## METADATA DO PROJETO

- **Projeto:** VTO Segundo Cerebro
- **Cliente:** Rafa (gestor de VTO Sanepar)
- **Regra de Transferencia:** Monobloco HTML — Google Docs → Bloco de Notas → .html
- **Repositorio GitHub:** `RafaMahlmann/Vto-segundo-c-rebro-`
- **Data de Inicio:** 2026-07-11
- **Data deste registro:** 2026-08-19
- **Versao atual do app:** 3.9
- **Status:** Partes 1 a 6 concluidas. Projeto funcional e operacional.

---

## RESUMO EXECUTIVO DO ESTADO ATUAL

O aplicativo esta **completo nas funcionalidades planejadas ate o momento**. Todas as 5 abas estao operacionais. O sistema de gerenciamento de matriculas com timeline, contador de 180 dias, cards de sancao, dashboard Canvas, import/export CSV/JSON e undo/redo esta funcionando. Nao ha bugs conhecidos.

As "Partes" mencionadas abaixo foram definidas organicamente durante o desenvolvimento, nao como um plano rigido pre-estabelecido.

---

## PARTE 1: FUNDACAO E ESTRUTURA BASE

**Periodo:** 2026-07-11

### Entregas
- [x] Recriacao do arquivo HTML original que havia quebrado no fluxo Google Docs → Bloco de Notas
- [x] Estabelecimento da **Regra Inquebrantavel** (monobloco HTML, zero dependencias)
- [x] Criacao do repositorio GitHub
- [x] Extracao e transformacao de 5 PDFs da Sanepar em 6 MDs semanticos (pasta `/docs/`)
- [x] Aba 1: Calculadora de Prazo (datas com dias uteis/corridos)
- [x] Aba 2: Calculadora de Dilacao (30/60/90 dias)

### Documentos Extraidos dos PDFs
| Arquivo | Origem | Conteudo | Dificuldade |
|---------|--------|----------|-------------|
| `01-legenda-categorias-matriculas.md` | PDF Sanepar | 8 categorias de classificacao de matriculas | Baixa |
| `02-resumo-estatistico-juveve.md` | PDF Sanepar | Indicadores comparativos Abril/Maio 2024 | Baixa |
| `03-codigos-resultados-vto.md` | IA OPE 21169 | 4 grupos de codigos de resultado (A/B/C/D) | Media |
| `04-objetivos-definicoes-vto.md` | IA OPE 169 | Glossario completo de siglas e definicoes | Baixa |
| `05-instrucao-tecnica-vto.md` | IT OPE 1580 | Documento-mae (resumo das 16 paginas) | Alta |
| `05-instrucao-tecnica-vto-completo.md` | IT OPE 1580 | Versao completa extraida pagina por pagina de PDF de 44MB | Muito Alta |

**Nota tecnica:** O PDF de 44MB (IT OPE 1580) era imagem escaneada. Foi necessario converter pagina por pagina com `pdf2image` (dpi=120) e extracao manual de texto.

---

## PARTE 2: FLUXO DE VISTORIAS E MATRICULAS

**Periodo:** 2026-07-11 a 2026-07-12

### Entregas
- [x] Aba 3: Fluxo de Vistorias VTO com 3 colunas visuais (azul/laranja/rosa)
- [x] 18 codigos de servico distribuidos nas 3 fases
- [x] Cards de sancao (1a SANCAO + MULTA DOBRO) com ativacao automatica
- [x] Aba 4: Registro de Matriculas (CRUD completo)
- [x] Tabela mestre estilo Excel com 10 colunas
- [x] 30 matriculas mock para demonstracao
- [x] Timeline inferior compacta (~110px) com contador de 180 dias
- [x] Modal de alta velocidade (auto-focus, Tab, Enter, Espaco, Esc)
- [x] Sistema undo/redo (Ctrl+Z / Ctrl+Shift+Z) com historico de 50 estados
- [x] Exportar CSV + Importar CSV (auto-detecta delimitador e formato de data)
- [x] Exportar JSON + Abrir Arquivo JSON
- [x] Clicar na matricula na tabela atualiza a timeline em tempo real
- [x] Todos os badges de prazo (OK/Alerta/Critico) com cores dinamicas
- [x] Cards de resumo (Total/OK/Atencao/Critico)

### Feedback do Usuario e Ajustes Realizados
| Feedback | Acao |
|----------|------|
| Botoes azul/vermelho "grotescos" | Trocados por `.btn-acao` cinzas discretos com hover suave |
| Timeline muito grande | Reduzida de 180px para 110px, fontes menores |
| Cores fortes nos badges | Reduzidas para tons pastel |
| "Ir para Matriculas" | Corrigido para "Ir para a tabela" |
| "matriculativa" (acento) | Corrigido para "Matriculas" (sem acento para compatibilidade Google Docs) |

---

## PARTE 3: DASHBOARD DE ESTATISTICAS

**Periodo:** 2026-07-13

### Entregas
- [x] Aba 5: Estatisticas e Indicadores VTO
- [x] 4 cards de KPI (Total Matriculas, Media Dias Execucao, Taxa em Aberto, % Excedido 180d)
- [x] Grafico Canvas: Distribuicao por Fase (barras verticais com gradiente)
- [x] Grafico Canvas: Situacao das Matriculas (rosca/donut com legenda)
- [x] Grafico Canvas: Evolucao Mensal (linha dupla: criacoes + baixas, 12 meses)
- [x] Grafico Canvas: Tempo Medio por Codigo (barras horizontais)
- [x] Integracao: graficos renderizam ao abrir aba e quando dados mudam
- [x] Max-width 1100px + max-width 520px nos cards para manter proporcoes em telas grandes

---

## ESTADO ATUAL DETALHADO

### Funcionalidades Operacionais (100%)
| Funcionalidade | Status | Notas |
|----------------|--------|-------|
| Analise de Prazo para Devolucao (Sancao) | OK | 30 dias corridos do faturamento (desde v3.3) |
| Calculadora de Dilacao | OK | Botoes 30/60/90 + input manual + caso especial (v3.7) |
| Fluxo de Vistorias VTO | OK | 3 colunas, 20 codigos, selecao de matricula ativa |
| Cards de Sancao | OK | Auto-ativação baseada em datas, 3 estados visuais |
| CRUD de Matriculas | OK | Adicionar, remover, selecionar, tabela Excel |
| Timeline Inferior | OK | Pontos de evento, marcador 180 dias, contador dinamico |
| Modal de Datas | OK | Alta velocidade (teclado 100%), sem clique necessario |
| Undo/Redo | OK | 50 estados, Ctrl+Z / Ctrl+Shift+Z |
| Importar/Exportar CSV | OK | Auto-detecta delimitador, mapeamento flexivel de colunas |
| Salvar/Abrir JSON | OK | Formato nativo da aplicacao |
| Dashboard Canvas | OK | 4 KPIs + 4 graficos, responsivos |
| Mock Data | OK | 30 matriculas geradas automaticamente |
| Responsividade Mobile | OK | Media queries para <768px |

### Arquivos do Projeto
```
/mnt/agents/output/
├── index.html                    # Aplicativo principal (monobloco)
├── README.md                     # Documentacao semantica para IA
├── TIMELINE.md                   # Este arquivo
└── docs/
    ├── 01-legenda-categorias-matriculas.md
    ├── 02-resumo-estatistico-juveve.md
    ├── 03-codigos-resultados-vto.md
    ├── 04-objetivos-definicoes-vto.md
    ├── 05-instrucao-tecnica-vto.md
    └── 05-instrucao-tecnica-vto-completo.md
```

---

## DECISOES ARQUITETURAIS IMPORTANTES PARA CONTINUIDADE

1. **Zero dependencias:** Nunca adicionar CDN, import, require ou framework. Se precisar de graficos, usar Canvas API nativa. Se precisar de componentes, criar funcoes HTML puras.

2. **Estrutura de dados unica:** Tudo gira em torno do array `matriculas[]`. Nunca quebrar essa estrutura sem atualizar todas as funcoes que a consomem (renderMatriculas, atualizarTimeline, renderGraficos, exportarCSV, exportarJSON, verificarSancoes).

3. **Regra inquebrantavel de transferencia:** Antes de qualquer modificacao, perguntar: "Isso funciona se copiar → Google Docs → Bloco de Notas → .html?" Caracteres especiais, acentos em nomes de variaveis e dependencias externas podem quebrar.

4. **Sincronizacao de abas:** Quando a aba Estatisticas esta ativa e dados mudam, `renderMatriculos()` chama `renderGraficos()` automaticamente. Se adicionar nova aba que depende de dados, seguir o mesmo padrao.

5. **Historico undo:** Sempre chamar `salvarHistorico()` ANTES de modificar `matriculas[]`. Funcoes que ja fazem isso: adicionarMatricula, removerMatricula, salvarDatasModal, marcarEmAberto, importarCSV, abrirArquivoJSON, resetarFluxo.

6. **Contador de 180 dias:** Calculado pela PRIMEIRA data de criacao de qualquer servico da matricula. Nao e alteravel pelo usuario. Se precisar de contagem diferente, criar campo separado.

---

## PARTE 4: TIMELINE PROPORCIONAL E 30 MATRICULAS MOCK

**Periodo:** 2026-07-13

### Problema
- A timeline posicionava o marcador de 180 dias fixo em `left:90%`, sem relacao com os dias reais.
- A escala era calculada apenas a partir dos proprios eventos da matricula, entao a sensacao de "falta pouco" nao era proporcional ao tempo.
- O app tinha apenas 4 matriculas mock, todas dentro do prazo, limitando a demonstracao de estados reais.

### Entregas
- [x] Timeline com escala de proporcionalidade real (abordagem hibrida):
  - `minData` = primeira criacao - 5 dias
  - `maxData` = o mais distante entre: hoje+15, dia 180+15 ou ultimo evento+15
  - Marcador de 180 dias posicionado proporcionalmente via JavaScript
  - Barra "hoje" tambem posicionada proporcionalmente
- [x] 30 matriculas mock variadas e coerentes com o fluxo VTO:
  - 5 novas (sem servico)
  - 8 na 1a vistoria
  - 8 na 2a vistoria
  - 5 na 3a vistoria
  - 4 excedidas (acima de 180 dias)
- [x] Verificacao de coerencia: datas cronologicas, baixas apos criacoes, sequencia 1a → 2a → 3a respeitada
- [x] Atualizacao da versao para 3.2 no README.md, TIMELINE.md e no footer da aba Estatisticas

### Decisao Arquitetural
A escala hibrida foi escolhida para garantir que o dia 180 sempre esteja visivel, mesmo em matriculas novas, sem perder a proporcionalidade real entre eventos.

---

## O QUE FALTA / POSSIVEIS CONTINUACOES (BACKLOG)

Nao ha pendencias obrigatorias. O aplicativo esta funcional e completo. As itens abaixo sao melhorias futuras que o usuario pode solicitar:

### Melhorias de UX
- [ ] Filtros na tabela de matriculas (por status, por fase, por data)
- [ ] Ordenacao de colunas na tabela (clicar no header para ordenar)
- [ ] Pesquisa/busca de matricula em tempo real
- [ ] Paginacao se o numero de matriculas crescer muito (>100)

### Funcionalidades Adicionais
- [ ] Edicao inline de datas na tabela (sem abrir modal)
- [ ] Checklist de EPI antes da vistoria (referencia IT OPE 1580)
- [ ] Vinculacao dos codigos de resultado (IA OPE 21169) aos servicos
- [ ] Multi-gerencia: suporte a varias Gerencias Regionais (GRs)
- [ ] Sincronizacao com SGC (sistema corporativo Sanepar)
- [ ] Relatorio PDF gerado a partir dos dados

### Evolucao dos Graficos
- [ ] Filtros de periodo nos graficos (mes/ano selecionavel)
- [ ] Comparativo entre bairros/gerencias
- [ ] Grafico de tendencia de regularizacoes

### Refatoracoes Tecnicas
- [ ] Modularizacao do JavaScript (mas mantendo monobloco para transferencia)
- [ ] Testes automatizados das regras de negocio
- [ ] Service Worker para funcionamento offline (cache)

---

## PARTE 5: PLANO DIRETOR - CARTEIRA VTO E COLABORACAO OFFLINE

**Periodo:** 2026-07-14

### Problema Identificado
- A timeline individual explica bem uma matricula, mas nao responde sozinha quais matriculas da carteira inteira exigem acao primeiro.
- O processo real precisa acompanhar matriculas ao longo de semanas/meses, reclassificando risco conforme o tempo passa.
- O app e local e monobloco; portanto, nao pode oferecer edicao simultanea real como Google Planilhas.
- Mesmo sem servidor, dois usuarios podem trabalhar em arquivos separados e consolidar depois por mesclagem.

### Direcao Arquitetural
- Tratar o conjunto de matriculas como uma **Carteira VTO** em acompanhamento continuo.
- Manter dois modos de visualizacao:
  - Individual: timeline detalhada da matricula selecionada.
  - Coletivo: radar/fila de risco para varias matriculas.
- Evoluir a tabela para filtros, ordenacao e paginacao antes de suportar grande volume.
- Criar futuramente uma rotina "Mesclar Arquivo" para somar arquivos JSON de usuarios diferentes, atualizar registros iguais e apontar conflitos.

### Documento Criado
- `docs/06-plano-diretor-carteira-vto.md`

### Proximas Entregas Recomendadas
- [ ] Criar filtros e ordenacao por risco na aba Matriculas.
- [ ] Criar paginacao para evitar travamento com grandes carteiras.
- [ ] Criar calculo de prioridade operacional.
- [ ] Criar aba Radar VTO / Carteira VTO.
- [ ] Evoluir JSON com metadados de autor, arquivo e atualizacao.
- [ ] Criar importacao com mesclagem inteligente e tela de conflitos.

---

## PARTE 6: V3.3 ATE V3.7 + BLINDAGEM CONTRA SESSOES DE IA

**Periodo:** 2026-07-14 a 2026-08-19

### Entregas (resumo por versao, conforme historico git)
- **v3.3:** Aba 1 substituida: saiu a "Calculadora de Prazo" generica, entrou a **Analise de Prazo para Devolucao (Sancao de Esgoto)** — 30 dias corridos a partir do faturamento da sancao
- **v3.3.1 / v3.3.2:** cabecalho da tabela de matriculas congelado ao rolar (sticky)
- **v3.4:** vistorias intermediarias, dilacao, habite-se e convenios nas colunas 2 e 3 do fluxo; fase registrada por servico; **sistema de aviso de nova versao** (banner + `version.json` + `fetch()` ao GitHub — unica excecao autorizada a regra de zero dependencias)
- **v3.4.1:** roleta de servicos no grupo da 1a vistoria (prototipo)
- **v3.5:** ajustes visuais no fluxo; auto-foco nos campos ao trocar de aba; navegacao TAB no fluxo; **agente de teste automatizado** (`agente_vto.py`, Playwright, screenshots)
- **v3.6:** campos de data com digitacao direta DD/MM/AAAA (mascara automatica) + botao 📅 de calendario separado
- **v3.7:** largura dos campos de data alinhada; **Calculadora de Dilacao reformulada**:
  - Removido seletor "dias uteis" (dilacao e sempre em dias corridos)
  - Botoes rapidos 30/60/90 + input numerico livre
  - Nova secao **Caso especial — dilacao parcial** (pedido antigo + concessao de 90 dias agora)
  - Textos revisados pela skill `.claude/skills/voz-do-vto`

### Incidente: sessoes de IA destruindo configuracoes
- Uma sessao paralela adicionou Font Awesome, refez UI nao solicitada e bumpou versao sozinha (commits v3.8/v3.9).
- **Tudo foi revertido** (5 commits de revert no topo do historico).
- Causa raiz identificada: nao existia protocolo de edicao, os docs estavam desatualizados em relacao ao codigo e nao havia mapa do `index.html`.

### Blindagem criada (2026-08-19)
- [x] **`AGENTS.md`** — protocolo de edicao cirurgica, proibicoes explicitas, mapa do `index.html`, checklist obrigatorio pos-edicao
- [x] **`CLAUDE.md`** — apontador para o AGENTS.md
- [x] README.md atualizado para v3.7 (aba 1, dilacao, excecao do fetch, padrao de campos de data)
- [x] Scripts de patch temporarios movidos para `patches/`

### Regra para qualquer nova sessao de IA
**Ler AGENTS.md antes de tocar no codigo. O codigo e a fonte da verdade; doc divergente nao autoriza "corrigir" o codigo.**

---

## COMO CONTINUAR EM UMA NOVA SESSAO

Se um novo agente/IA precisar continuar este projeto:

1. **Leia o AGENTS.md PRIMEIRO** — protocolo de edicao cirurgica, proibicoes e mapa do index.html (INEGOCIAVEL)
2. **Leia o README.md** — contem a documentacao completa do aplicativo
3. **Leia este TIMELINE.md** — contem o estado atual e o que ja foi feito
4. **Abra o `index.html`** no navegador para ver o estado funcional
5. **Verifique a pasta `/docs/`** para os documentos semanticos da Sanepar
6. **Nunca quebre a Regra Inquebrantavel** (Google Docs → Bloco de Notas → .html)
7. **Nunca reescreva o index.html inteiro** — edicoes cirurgicas por ancora, conforme AGENTS.md
8. **Sempre teste no browser** apos qualquer modificacao antes de declarar pronto (checklist do AGENTS.md, secao 6)

---

## CONTEXTO DE NEGOCIO PARA NOVO AGENTE

O usuario (Rafa) trabalha com Vistorias Tecnicas Operacionais (VTO) da Sanepar. O processo envolve:

1. Receber solicitacao de vistoria (cliente, Prefeitura, Ministerio Publico)
2. Agendar 1a vistoria (codigos 8403/8421/etc.)
3. Se irregular: notificar usuario, aguardar 60 dias
4. Se persistir: 2a vistoria (8405) + 1a SANCAO (multa)
5. Se persistir: 3a vistoria (8428) + MULTA DOBRO
6. Limite total: 180 dias corridos
7. Tudo registrado no SGC (Sistema de Gerenciamento Comercial)

O aplicativo substitui/controle planilhas Excel e papelada manual. O usuario precisa:
- Saber em qual fase cada matricula esta
- Saber quantos dias faltam para a proxima acao
- Calcular prazos de dilacao e recursos
- Gerar relatorios para gestao
- Importar dados de outros sistemas (CSV)

---

*Registro gerado em 2026-07-13. Atualizado em 2026-08-19. Estado: Projeto operacional em v3.9, sem pendencias criticas. Sessoes de IA devem seguir o AGENTS.md.*

---

## PARTE 9 — Fusão VTO + Anonimizador (2026-09-14, v4.4)

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
Tudo subiu junto para v4.4. E a checagem do banner virou `versaoEhMaior()`:
antes era "diferente de", então qualquer descompasso ligava o aviso de nova
versão — inclusive para quem tinha acabado de baixar a versão nova.

**Etapa 4 — Higiene.**
Scripts de teste soltos na raiz foram para `patches/testes_antigos/`.
Documentos atualizados para o mapa de 6 abas.

Teste automatizado da entrega: `patches/_test_etapa1.py` (21 verificações).

---

## PARTE 10 — Refazer (2026-09-14, v4.4)

O `Ctrl+Shift+Z` e o botão Refazer nunca funcionaram. Não era o atalho.

O histórico era uma pilha só com um índice. Como o protocolo manda chamar
`salvarHistorico()` **antes** de alterar `matriculas[]`, a pilha só guardava
estados anteriores — o estado pós-alteração não era gravado em lugar nenhum.
Refazer era impossível por construção, e o `Ctrl+Z` só acertava por
coincidência, porque os dois últimos estados eram iguais.

Passou a ter duas pilhas: `historico` e `historicoFuturo`. O `undo()` empilha o
estado de agora antes de voltar — era esse o estado que faltava. Os 9 pontos que
chamam `salvarHistorico()` não mudaram: o protocolo do `AGENTS.md` continua
valendo palavra por palavra.

De quebra, o `gerarMockData()` passou a chamar `limparHistorico()`: os dados de
demonstração são ponto de partida, não alteração do usuário.

Teste: `patches/_test_etapa5.py` (31 verificações).

### Correções vindas do teste independente (5c)

Um testador por fora achou três coisas, e a primeira era grave.

**O `Ctrl+Z` sequestrava o teclado dentro dos campos.** Digitar uma data e apertar
`Ctrl+Z` não desfazia o texto: desfazia uma **matrícula**, em silêncio, numa aba
que a pessoa nem estava vendo — e o campo não mudava, então nada denunciava.
Parte disso foi piora da própria Etapa 5: o `toLowerCase()` passou a capturar
também o `Ctrl+Shift+Z`, que antes escapava com `Z` maiúsculo.
Agora, dentro de `input`, `textarea` ou campo editável, o atalho é do texto.

**As bolinhas da roleta ficavam defasadas** depois de desfazer: o `aplicarEstado()`
redesenhava tabela e timeline, mas não as roletas do Fluxo.

**O aviso do reset mentia.** Dizia *"Isso nao pode ser desfeito"*, mas o
`resetarFluxo()` chama `salvarHistorico()` — o teste mediu: `Ctrl+Z` devolve os 56
serviços. E o reset não apaga "todos os dados": as matrículas continuam na lista.
O rótulo do botão dizia a mesma inverdade. Os dois foram reescritos pela
`voz-do-vto` para contar a mesma história, e a verdadeira.

Testes: `patches/_test_etapa5c.py` (18), `_test_etapa5.py` (31), `_test_etapa1.py` (24).

---

## PARTE 11 — Retângulo vazio, busca e roleta com efeito (2026-09-21, v4.5)

Todo retângulo de código do Fluxo agora começa **vazio**.
São 11, nas 3 vistorias. Deixar vazio é uma escolha válida.

Clicar no vazio abre a busca.
Digite o código ou parte do nome. A lista filtra na hora.
Código completo (4 dígitos) encaixa sozinho.
A busca só aceita códigos daquele retângulo.
Se o código existe em outro, a mensagem diz onde ele mora.

A roleta ficou inteira: setas, rodinha, bolinhas.
A novidade é que a casa vazia entra no giro.
Com o grupo armado: digitar abre a busca, setas giram, Enter registra, Delete esvazia.

O efeito é só visual: giro que sai e entra, encaixe que assenta, tinta que varre.
Sem som, sem confete. Desliga sozinho com "reduzir movimento" do Windows.

**Escolher um código não grava nada.**
Só o 2º clique (janela de datas) grava, como sempre foi.
Por isso `salvarHistorico()`, `matriculas[]` e o desfazer/refazer não foram tocados.

**Onde mexeu:** CSS novo depois do CSS da roleta, `setupRoletaGrupo()` refeita,
e uma limpeza nova em `prepararHtmlLimpo()` (plano B do export).
O HTML das colunas não mudou: os 45 botões reais continuam lá, só escondidos.

**Regra nova para a próxima sessão:** o palco, a casa vazia e a busca são gerados
em tempo de execução. Quem mexer neles deve manter a limpeza em `prepararHtmlLimpo()`.

**Teste:** `patches/_test_roleta_vazia.py` (61 verificações).
`patches/_test_regressao_completa.py` foi ajustado: a roleta começa vazia, então o teste escolhe o 8403 pela busca.
Script da mudança: `patches/roleta_vazia_busca.py` (ajustes finos depois dele foram direto no `index.html`).

**Falhas que já existiam antes desta entrega (não são da roleta):**
- Console mostra 404: é a checagem de `version.json` no GitHub.
- `_test_etapa1` reprova "sem inchaço" quando o arquivo está em CRLF, como na pasta do Rafa.


---

## PARTE 12 — Calculadora rápida dos 180 dias (2026-10-07, v4.5)

Botão azul redondo (calendário) flutuando no canto direito das abas
**Fluxo de Vistorias** e **Matrículas**. Nas outras abas ele não aparece
(regra por CSS `:has()`, sem tocar em `mostrarAba()`).

Tocar no botão sobe uma folha do fundo da tela (mola de 420ms).
Você joga a data da 1ª vistoria e ela responde **na hora, sem botão de calcular**:
dias corridos, dias que faltam para os 180, barra de progresso e o semáforo
**do próprio app** (>60 verde, 31–60 laranja, ≤30 vermelho, estourado = vermelho
cheio com "⚠ Prazo de 180 dias expirado há X dias").

Se houver matrícula ativa, a folha já abre com a data da 1ª vistoria dela
(e avisa embaixo: "Preenchido com a 1ª vistoria da matrícula N...").
Trocou a data na mão, o aviso some — a data manual sempre vence.

**Onde mexeu (só código novo, 212+ linhas, zero remoções):**
- CSS novo: bloco `/* ===== CALCULADORA RAPIDA 180 DIAS ===== */` (depois do contador 180)
- HTML novo: `#calc180Fab` + `#calc180Overlay` + `#calc180Folha` (entre a aba 4 e a aba 5)
- JS novo: seção `// ===== CALCULADORA RAPIDA 180 DIAS =====` (antes de EXPORTAR CSV),
  reusando `getDiaZero()` e o semáforo do `atualizarContador180()`
- Limpeza "3b" em `prepararHtmlLimpo()` (a folha sai fechada e vazia no export)

**Pegadinha achada pelo Rafa (já resolvida):** o campo usava `aplicarMascaraData`,
que remonta os dígitos a cada tecla — apagar um pedaço no meio da data fazia a
máscara restaurar o valor antigo e a folha não recalculava. O campo virou
`<input type="date">` nativo (edição por pedaços, calendário embutido, sem máscara).
A máscara do app continua igual nas outras abas — não foi tocada.

**Teste:** `patches/_testa_calc180.py` — 10 verificações, todas OK
(load sem erros, 6 abas, FAB só em Fluxo/Matrículas, 3 faixas + estouro,
📅, Esc, prefill, undo/redo 31→30→31, timeline, export limpo, celular 375px).
Backup de antes da mudança: `patches/_backup_index_antes_calc180.html`.

**Não mudou:** versão (continua v4.5), nenhuma função existente, nenhuma outra aba.

---

## PARTE 13 — Seletor de colunas do Anonimizador (2026-10-07, v4.5 / anon v19.0.0)

A etapa "2. Configuração de Colunas" do anonimizador virou uma **galeria de cartões**
(propostas S1+S2 combinadas, aprovadas pelo Rafa):

- Cada coluna é um **cartão** com nome, **amostra real dos dados** (3 primeiros
  valores lidos do arquivo) e **5 bolinhas de cor**: azul Manter, roxo Anonimizar,
  laranja Dublê, verde Simular, cinza Excluir. **1 clique na bolinha já muda o
  estado** — não tem mais ciclo de 5 cliques.
- **Clique no cartão = selecionar.** Abre a **barra de ação em massa** que sobe
  do fundo (preta, arredondada): "N colunas selecionadas" + as 5 cores em tamanho
  grande. Aplicar roda em cascata (12ms por cartão, efeito pop).
- **Busca instantânea** por nome (ignora acento), botões "Selecionar visíveis" e
  "Limpar seleção", e **contador vivo** ("10 Manter · 1 Dublê · 10 Simular · 138 Excluir")
  que pulsa a cada mudança.
- No modo CSV a bolinha verde (Simular) **some** — simulação só existe no TXT/SGCG.

**Onde mexeu (só no anonimizador.html, ~250 linhas novas):**
- CSS: bloco `/* ===== SELETOR DE COLUNAS ===== */` antes de `</style>`
- HTML: toolbar de busca + contador + aviso de vazio + `#selcBarra` (barra fixa)
  ao redor do `#chipsContainer` (que ganhou a classe `selc-grade`)
- JS: `adicionarColunaInterface()` agora monta o cartão; `atualizarVisualChip()`
  **não toca mais o innerHTML** (a amostra sobrevive à troca de estado e ao preset);
  seção nova `// ===== SELETOR DE COLUNAS =====` com seleção, busca, contador,
  massa e `carregarAmostras()` (lê os primeiros 64KB do arquivo com o encoding detectado)
- Gancho em `analisarArquivoInicial()`: limpa seleção/amostras e marca
  `body.selc-modo-csv` quando o arquivo é CSV
- Base64 regerado com `patches/embutir_anonimizador.py` (regra da seção 9)

**Bug de ferramenta achado e corrigido:** `embutir_anonimizador.py` dizia "Nada a
fazer" quando o index.html tinha CRLF ao redor das marcas — a regex exigia `\n` puro.
Agora aceita `\r?\n` e escreve o bloco na mesma quebra do arquivo.

**Decisões de compatibilidade:**
- `alternarEstado()` (ciclo antigo) continua no código, só não é mais chamada pela interface.
- As cores/classes de estado (`chip-normal`, `chip-anon`...) são as mesmas — preset,
  processamento e log não mudaram.
- Botões novos blindados contra o `button { width:100% }` global do anonimizador.

**Teste:** `patches/_testa_seletor.py` — 18 verificações, todas OK
(load sem erros, 6 abas, 6 cartões CSV com amostras reais, bolinha 1 clique,
busca com/sem resultado, Simular escondido no CSV, barra de massa, excluir em massa,
159 cartões no TXT, preset SGCG com amostras preservadas, contador correto).
Prints: `propostas/2026-10-07/prints/08..10_seletor_*.png`.
Backups: `patches/_backup_anonimizador_antes_seletor.html` e `_backup_index_antes_seletor.html`.

**Não mudou:** versão, processamento, preset Power Query, nenhuma outra aba do app.

**Bug conhecido (pré-existente, NÃO corrigido nesta entrega — fase separada):**
`TERMOS_SENSIVEIS` marca por substring, então NOME-BAIRRO, NOME-FONTE etc. caem como
"Anonimizar" por padrão no TXT. Está documentado em
`propostas/2026-10-07/pesquisa-seletor-colunas.md`.

---

## PARTE 14 — Falsos positivos do detector de colunas (2026-10-07, v4.5 / anon v19.0.0)

O detector de colunas sensíveis era por substring: qualquer coluna com "NOME"
no nome nascia roxa (Anonimizar). Quatro colunas do SGCG não são nome de pessoa
e caíam nessa por engano:

- NOME-BAIRRO (127), NOME-FONTE (131), NOME-RESERVA (132), NOME-ENDER-ALT (150)

**Correção cirúrgica (2 trechos no anonimizador.html):**
- Lista nova `TERMOS_SENSIVEIS_EXCECOES` com as 4 colunas.
- `verificarSensibilidade()` devolve `false` se o nome bate numa exceção.

As 4 agora nascem azuis (Manter). NOME-CLIENTE continua Simular; o resto do
detector não mudou. Nascimento correto importa para quem processa **sem** o
preset Power Query (com preset, essas colunas viram Excluir de qualquer jeito).

**Teste:** `_testa_seletor.py` ganhou as verificações 8f/8g
(4 exceções nascem Manter, NOME-CLIENTE continua Simular) — 24 verificações OK.
Base64 regerado (`embutir_anonimizador.py`).

---

## PARTE 15 — Pontinho de ajuda do Exportar ZIP (2026-10-08, v4.5)

Um **"?" laranja pulsante** ao lado do botão Exportar ZIP, no header.
Clica nele e abre um modal explicando, em linguagem simples:

- o que é o ZIP (o programa inteiro num arquivo só);
- como usar em outro computador (abrir o ZIP, 2 cliques no index.html, sem instalar nada);
- como compartilhar com um colega (mandar o ZIP por e-mail ou WhatsApp);
- que o ZIP sai limpo, sem as matrículas da tela.

Texto passou pela lente de simplicidade e pelas regras da voz-do-vto
(frases curtas, sem jargão, uma ideia por parágrafo).

**Onde mexeu (3 inserções, zero remoções):**
- CSS: `.btn-zip-info` + pulso (desliga com "reduzir movimento"), junto ao `.btn-zip`
- HTML: botão `?` logo depois do Exportar ZIP no header
- JS: `abrirAjudaZip()` — reusa o `#modalOverlay` da Ajuda, então Esc fecha
  e o export limpo continua garantido pelo retrato

**Teste:** `patches/_testa_ajuda_zip.py` — 8 verificações OK
(pontinho visível, modal abre com o texto completo, Esc fecha e restaura,
ajuda antiga intacta, export sem modal aberto, celular 375px, console zerado).
Print: `propostas/2026-10-07/prints/11_ajuda_zip.png`.

**Não mudou:** versão (v4.5), fluxo do export, nenhuma aba.

---

## PARTE 16 — Versao v4.6 (2026-10-08)

Bump pedido pelo Rafa junto com o pontinho de ajuda do ZIP.
Subiram juntos: title, badge, 4 rodapes, versao dinamica, VERSAO_LOCAL,
sw.js (vto-cache-v4.6), version.json (4.6), README, package.json.
Quem estiver na 4.5 vai ver o banner de nova versao.

---

## PARTE 17 — Integra Etapa 5c com v4.5/v4.6 + versao v4.7 (2026-10-16)

Duas frentes de trabalho tinham avancado separadas sem se cruzar: este
checkout local tinha a Etapa 5c (correcoes de Ctrl+Z, roleta e aviso do
reset — Parte 10) commitada só localmente sobre a v4.4, enquanto o GitHub
já tinha avançado até a v4.6 (Partes 11 a 16) sem essas 3 correções.

**Mesclagem:** a Etapa 5c virou commit próprio, o GitHub foi puxado, e os
dois lados foram unidos com `git merge`. O `index.html` uniu sozinho, sem
conflito — só o `TIMELINE.md` precisou de resolução manual (as duas Partes
novas, cada lado tinha escrito a sua no fim do arquivo). Testado no
navegador pós-merge: as 3 correções da Etapa 5c continuam valendo (Ctrl+Z
num campo de texto não mexe mais em matrícula), zero erro de console,
anonimizador carrega, 30 matrículas mock intactas. Enviado ao GitHub.

**Bump para v4.7:** pedido pelo Rafa — mudança real (a integração acima)
exige versão nova, mesmo sem funcionalidade visível nova. Subiram juntos:
title, badge, 4 rodapes, versao dinamica, VERSAO_LOCAL, sw.js
(vto-cache-v4.7), version.json (4.7), README, package.json.

**Pasta "Calculadora pós sanção" (nunca foi do git):** investigada a
pedido do Rafa. Confirmado que é o protótipo original e solto da
calculadora de prazo — o `script.js` dela é linha a linha o mesmo
algoritmo de `calcularPrazoSancao()`, que já está no `index.html` desde a
v3.3 (Parte 6). Sem uso, sem referência em lugar nenhum do app. A exclusão
pelo agente de IA foi bloqueada pela permissão do ambiente; o Rafa precisa
apagar a pasta manualmente.

---

## PARTE 18 — Filtro de linhas no Anonimizador (2026-10-16, anon v19.0.0)

O botão verde "Aplicar Padrão Power Query" escondia um filtro travado:
só processava linhas onde a coluna LOCAL (posições fixas 3-6 do TXT) fosse
exatamente "001". Sem jeito de trocar — toda cidade/unidade que não fosse
a 001 ficava de fora, mesmo sendo uma decisão do Rafa, não do código.

**Pesquisa primeiro:** antes de construir, procurei por bibliotecas prontas
de filtro estilo Excel/Power Query (pedido do Rafa). Não existe nada de
graça e sem dependência — as robustas são Syncfusion/Handsontable (pagas)
ou presas a framework (React/jQuery). Incompatível com a regra de zero
dependência do projeto. Ficaram 3 convenções validadas que foram copiadas
pro design: busca dentro da lista de valores, limite de 1000 valores
distintos pra colunas de alta cardinalidade, confirmar antes de aplicar.

**O que entrou:** o filtro virou um painel próprio ("Filtrar linhas antes
de processar"), separado da aplicação das regras de anonimização do botão
verde. Cada filtro tem duas abas:
- **Digitar valores** (padrão): cola ou digita uma lista (matrícula, por
  exemplo) — não escaneia o arquivo, é instantâneo. Pensado pra colunas
  de alta cardinalidade (160 mil matrículas não cabem em checklist).
- **Marcar da lista**: varre o arquivo inteiro, lista os valores que
  realmente aparecem naquela coluna (com contagem), com busca e
  marcar/desmarcar tudo. Bom pra colunas com poucas variações (LOCAL,
  UNIDADE, CATEG).

Vários filtros empilham e combinam sempre com **E** — ex.: UNIDADE = 220
e CATEG = 011, ou uma lista de matrículas e LOCAL = 001 ao mesmo tempo.
Editar um filtro existente reabre na aba certa, com o estado anterior.
Trocar de arquivo zera os filtros. O botão verde continua só com as
regras de anonimização; quem quer restringir linhas usa o painel.

**Onde mexeu (anonimizador.html, depois reembutido no index.html):**
`FILTRAR_LOCAL_001` (flag binária) virou `FILTROS_LINHA` (lista de regras);
`linhaPassaFiltros()` checa as duas pelos 2 pontos que já filtravam
(`coletarPools()` e o laço principal); `PRESET_SGCG_APLICADO` assumiu o
papel que a flag velha tinha na ordenação de colunas do preset.

**Bug achado e corrigido durante o teste:** o botão "Aplicar filtro"
reusava a classe `.btn-pq`, que é `display:none` por padrão (só o botão
verde principal liga ela via JS) — o botão de confirmar ficava invisível
e fora da viewport. Criada `.filtro-btn-aplicar` dedicada. Um segundo bug:
reabrir um filtro do tipo "lista" pra editar caía sempre na aba "Digitar"
em vez de "Marcar da lista" — `filtroEditar()` checava o tipo errado.

**Teste:** arquivo TXT sintético de 20 linhas com 3 grupos controlados
(UNIDADE/LOCAL/CATEG/MATRICULA), injetado via `DataTransfer` direto no
`#fileInput` (sem precisar de diálogo). Confirmado: contagem por valor
bate, os dois modos combinam com E de verdade (uma matrícula do grupo
certo passa, uma do grupo errado é barrada mesmo estando na lista
digitada), editar preserva estado, trocar de arquivo zera tudo. Depois,
`patches/_testa_seletor.py` (24) e `patches/_test_regressao_completa.py`
(21) — nenhuma quebra no resto do app.

---

## PARTE 19 — Prévia ao vivo nos cartões (2026-10-16, anon v19.0.0)

Clicar numa bolinha de estado (Manter/Anonimizar/Dublê/Simular/Excluir)
agora atualiza na hora os 3 valores de amostra do cartão, mostrando como
aquele dado ficaria — sem precisar rodar o processamento inteiro pra
descobrir se "convence ou não" (motivação do Rafa: pegar erro antes).

**Risco de segurança levado a sério:** as funções reais de hash/dublê/
sintético (`gerarHash`, `formatarDubleMatricula`, `valorSintetico`) leem e
escrevem em `SALT_HEX`, `MAPA_DUBLE`, `USADOS_DUBLE`, `CONSISTENCIA` — o
sal e os mapas do **lote de verdade**. Se a prévia usasse essas mesmas
funções, clicar numa bolinha pra só olhar poderia gastar um número de
dublê que o processamento real precisava, ou prender o hash da prévia ao
sal errado. Por isso nasceu um motor de prévia **isolado**: `PREVIA_SALT`,
`PREVIA_MAPA_DUBLE`, `PREVIA_USADOS_DUBLE`, `PREVIA_CONSISTENCIA` — mesmas
fórmulas (mesmo SHA-256 + sal + contador), memória própria, nunca toca no
estado real. Testado e provado: depois de usar a prévia à vontade,
`SALT_HEX` real continua `null` e `MAPA_DUBLE` real continua vazio.

**Escopo reduzido conscientemente:** Simular em ENDERECO e LOTE depende de
um mapeamento de ruas/lotes construído varrendo o arquivo inteiro (só
acontece hoje no processamento de verdade). Replicar isso na prévia exigia
ou escanear o arquivo de novo a cada clique, ou compartilhar os contadores
de ocorrência do pool real (o que mudaria sutilmente o resultado do
processamento real depois). Nenhuma das duas valia o risco — essas duas
colunas mostram um aviso ("depende do arquivo inteiro — ver após
processar") em vez de simular. Também não repliquei a sutileza de
TELEFONE (remove hífen) e `DT-` (desloca data) em estado Manter — a
prévia nesse estado mostra o valor cru.

**Onde mexeu:** `carregarAmostras()` passou a chamar a prévia transformada
em vez de mostrar sempre o cru; `selcDefinirEstado()` (clique individual)
e `aplicarPresetSGCG()` (clique em massa) chamam a mesma função depois de
mudar o estado. `selcRenderAmostra()` (função antiga, só mostrava o
original) foi removida — nada mais a chamava.

**Teste:** script Playwright fora do repo (scratchpad), com um TXT
sintético (nome, CPF, matrícula reais) — confirma que a prévia muda
com cada estado, é consistente entre cliques, e não toca no sal/mapas
reais. `patches/_testa_seletor.py` precisou de 3 ajustes: a coluna
MATRICULA sempre nasceu em Dublê, então a amostra dela nunca foi o valor
cru — os testes antigos checavam o comportamento de antes da prévia
existir, por coincidência passavam porque liam o index.html com o
anonimizador velho ainda embutido. Corrigidos pra checar o dublê (8
dígitos, ≠ original). 24 + 21 testes, tudo verde.

---

## PARTE 20 — Edição manual por coluna, 6º estado (2026-10-16, anon v19.0.0)

Pedido do Rafa: às vezes ele quer controlar à mão o que sai numa coluna —
poucas linhas, pra gerar uma amostra que "convence" antes de confiar no
automático. Virou um 6º estado, cor índigo (nenhuma das 5 usava essa
faixa), ✍️.

**Como funciona:** clicar na 6ª bolinha de um cartão não aplica na hora
(diferente dos outros 5 — Manter/Anonimizar/Dublê/Simular/Excluir são
1 clique) porque precisa de dado digitado. Abre um painel: escolhe quantas
linhas (1 a 50), carrega os valores originais do arquivo, cada um já
editável — escreve por cima, sem coluna de comparação ao lado (o Rafa
testou a primeira versão com "original ao lado + campo editável" e achou
confuso, ter que ler uma coluna pra escrever na outra; a versão final é só
o campo, já populado com o original, edita direto). Linha que não for
editada sai **vazia** no arquivo final — é a regra que o Rafa pediu
("o resto ele deleta").

**Aviso de risco, sempre visível, não é popup que passa:** banner vermelho
fixo no topo do painel + checkbox obrigatório ("Entendi o risco") que
precisa estar marcado pro botão Aplicar habilitar. Mais forte que um
`confirm()` nativo — o Rafa pediu insistentemente esse alerta, com razão:
edição manual contorna o anonimizador automático, então um erro de
digitação aqui pode vazar dado real sem a ferramenta perceber.

**Reorganização do espaço (skill `game-feel-ui`, plano aprovado antes de
codar):** o botão verde + o filtro de linhas + a entrada da edição manual
viraram uma seção "⚙️ Opções avançadas de processamento", fundo cinza
recuado, sem brilho (mundo visual continua o "iOS claro" do resto da
ferramenta — a skill é clara que glow só funciona em fundo escuro).

**Engenharia (onde mexeu):** `EDICOES_MANUAIS` (Map colId → Map
numeroLinhaAbsoluto → valor digitado). `numeroLinhaAbsoluto` é um contador
novo no laço principal de processamento, incrementado por linha
substantiva **antes** do filtro de linhas — o editor usa a mesma contagem
pra achar de novo a linha certa. Um ramo novo (`item.estado === 5`) no
mesmo formato dos outros 4 ramos existentes. `colId` passou a viajar
dentro de cada item do loop (não existia antes — precisei adicionar nos
dois pontos, TXT e CSV, onde `valoresOriginais` é montado).

**Teste:** script Playwright fora do repo — carrega 4 linhas num cartão,
edita a 1ª, deixa a 2ª e a 4ª com o original, apaga a 3ª, roda o
processamento de verdade (não só a prévia) e lê o CSV de saída linha por
linha: edição aparece, original preservado aparece, linha apagada sai
vazia, e a coluna MATRICULA (Dublê automático, nem tocada) continua
funcionando do lado. 12 verificações, tudo OK. Depois,
`patches/_testa_seletor.py` (24) e `patches/_test_regressao_completa.py`
(21) de novo, sem quebra.

---

## PARTE 21 — Ajuste de UX na edição manual (2026-10-16, anon v19.0.0)

Feedback do Rafa depois de testar a Parte 20: faltava clareza de "o que eu
mudei" e faltava uma conferida antes de aplicar de verdade.

- **Cor dinâmica:** campo nasce cinza (ainda igual ao original). Digitar
  algo diferente vira preto e negrito na hora — fica óbvio o que foi
  mexido sem comparar duas colunas.
- **Etapa de revisão:** o botão "Revisar antes de aplicar" leva pra uma
  tela que mostra as N linhas como vão sair ("3 de 4 alteradas, 1 sem
  mudança"), com a original ao lado de quem mudou. De lá, "← Voltar e
  editar" volta pra lista — **sem perder o que já foi digitado** — ou
  "Confirmar e aplicar" (com o checkbox de risco, que migrou pra essa
  etapa, já que é o momento real de decisão).

**Onde mexeu:** `MANUAL_REVISAO_VALORES` guarda os valores digitados
quando entra na revisão (os inputs da lista deixam de existir nessa tela,
é só leitura). `manualRenderLista()` ganhou um parâmetro opcional pra
reconstruir a lista de edição com esses valores preservados, em vez de
voltar ao original. Teste Playwright (fora do repo) cobre cor dinâmica,
contagem da revisão e "voltar preserva o digitado" — 16 verificações, e
o processamento real linha a linha continua batendo.
`patches/_testa_seletor.py` (24) e `_test_regressao_completa.py` (21),
sem quebra.

---

## PARTE 22 — Carimbo de versão deixava de mentir (2026-10-19)

O Rafa abriu um arquivo velho na Sanepar, viu "v4.7.2026-10-19.11-43" e
achou que era o de hoje — não era. Investigado: o GitHub estava certo
(confirmado lendo o `raw.githubusercontent.com` direto, decodificando o
Base64 do anonimizador embutido — as 4 entregas estavam lá, batendo byte
a byte com o `embutir_anonimizador.py` local). O arquivo que ele abriu é
que não era este.

**A causa raiz do mal-entendido:** `aplicarVersaoDinamica()` carimbava a
**hora em que o arquivo foi aberto**, não a versão do código. Um arquivo
de semanas atrás, aberto hoje, carimbava a data de hoje do mesmo jeito —
by design, o carimbo nunca poderia provar "isso é a entrega mais
recente". Virou `DATA_ENTREGA`, uma constante fixa (`'19/10/2026'`) que
só muda quando sobe código novo, igual o `VERSAO_LOCAL`. Badge e os 4
rodapés agora mostram "v4.7 · 19/10/2026" — a data da entrega, não da
abertura. Gerei um ZIP novo na hora e mandei pro Rafa, confirmando antes
(decodificando o Base64 de dentro do ZIP) que as 4 entregas estavam lá.

**Regra para a próxima sessão:** atualizar `DATA_ENTREGA` junto com
`VERSAO_LOCAL` a cada entrega relevante — os dois ficam logo depois um do
outro no código, perto da linha 3173.

Teste: `patches/_test_regressao_completa.py` (21), sem quebra.

---

## PARTE 23 — Aba Auditoria documenta os testes desde a reconstrução (2026-10-19)

Pedido do Rafa: "fizemos um monte de auditorias e testes e faltou
atualizar essa parte" — a aba Auditoria & Segurança do anonimizador só
tinha a tabela do pentest de 01/09/2026 (v18.2.2 reprovada → v19.0.0
aprovada). Todo o trabalho depois disso — fusão, filtro de linhas,
prévia, edição manual — não aparecia ali.

Entrou uma seção nova, **separada** da tabela do pentest (que é um
registro histórico de ataque adversarial e não deve ser editado):
"Testes automatizados desde a reconstrução", deixando claro que é
regressão funcional contra dado sintético, não um novo pentest — são
evidências diferentes, não substituem uma a outra.

Antes de escrever, rodei o teste que tinha ficado pendente desde 15/09:
`patches/_test_zip_leak_csv.py` — importa uma matrícula-armadilha via
CSV, exporta o ZIP, procura a armadilha dentro. **Resultado: 0
ocorrências.** Isso fechou um buraco real na documentação: ninguém tinha
confirmado, por escrito, que dado importado (não só o que já estava
gravado) também não vaza no export.

Teste: `patches/_testa_seletor.py` (24) e `_test_regressao_completa.py`
(21), sem quebra. Base64 reembutido no index.html.

---

## PARTE 24 — Versão v4.8 (2026-10-19)

Bump pedido pelo Rafa: três funcionalidades grandes (filtro de linhas,
prévia ao vivo, edição manual) tinham subido sob a v4.7 sem o número
mudar. Subiram juntos: title, badge, 4 rodapés, `VERSAO_LOCAL`, `sw.js`
(vto-cache-v4.8), `version.json` (4.8), README, `package.json`.
`DATA_ENTREGA` continua `19/10/2026` — já estava certa, não mudou.
Quem estiver na v4.7 vai ver o banner de nova versão.

Teste: `patches/_test_regressao_completa.py` (21), sem quebra.

---

## PARTE 25 — Fila de edição manual na barra preta + versão v4.9 (2026-10-19)

Pedido do Rafa: a barra preta de ação em massa (aparece ao selecionar
várias colunas) tinha as 5 cores automáticas, mas não o Manual — porque
"aplicar em massa" não faz sentido pra digitar dado à mão em 10 colunas
de uma vez. Só que sumir de vez também não fazia sentido pra ele, que
queria velocidade pra começar a editar várias colunas sem caçar cartão
por cartão.

**Virou fila.** Bolinha índigo na barra preta abre o editor da primeira
coluna selecionada, igual já funcionava num cartão avulso. Ao confirmar,
abre sozinho o editor da próxima — sem precisar clicar de novo. Um
badge "Coluna 2 de 10 · cancelar fila" mostra onde você está. Pode
"Pular esta coluna →" a qualquer momento (não mexe nela, só avança) ou
cancelar a fila inteira (as colunas já confirmadas antes de cancelar
continuam valendo — só as que faltavam ficam de fora).

**Nada mudou na segurança:** cada coluna da fila passa pelo editor
completo — carregar linhas, editar, revisar, marcar "Entendi o risco" —
um de cada vez. A fila só automatiza o clique inicial, não pula etapa
nenhuma de revisão.

**Onde mexeu:** `MANUAL_FILA` (array de colIds restantes) e
`MANUAL_FILA_TOTAL` (tamanho original, 0 = fora de fila).
`manualAbrirEditor()` mostra o badge só quando `MANUAL_FILA_TOTAL > 0`;
fora de fila (clique num cartão avulso) continua exatamente como antes.
`manualConfirmarRevisao()` passou a chamar `manualAvancarFila()` em vez
de fechar direto.

**Teste:** script Playwright fora do repo — seleciona 3 colunas, confirma
a 1ª de verdade, pula a 2ª, cancela na 3ª, confirma que só a 1ª mudou de
estado e que o editor avulso (sem fila) continua sem o badge. 14
verificações OK. `patches/_testa_seletor.py` (24) e
`_test_regressao_completa.py` (21), sem quebra.

**Versão v4.9** (pedido do Rafa): subiram juntos title, badge, 4 rodapés,
`VERSAO_LOCAL`, `sw.js`, `version.json`, README, `package.json`.

---

## PARTE 26 — Simular vira format-aware em todas as colunas (Proposta 1)

O achado do Rafa, direto: ele selecionou as 159 colunas, aplicou
Anonimizar (roxo) esperando uma planilha simulada pra prototipar um
app, e todas viraram hash de 32 caracteres — "220" (3 dígitos) virou um
código de 32, nome composto virou ilegível. "Essa função hash tá muito
fraca... nós estamos anonimizando pra simular algo parecido lá fora."

**A causa raiz:** Anonimizar (hash puro, SHA-256) é assim por design —
é o estado pra destruir de propósito, auditado como irreversível. Quem
deveria preservar formato é Simular, mas só tinha gerador dedicado pra
9 tipos (nome, CPF, RG, telefone, endereço, número, CEP, lote). Das 159
colunas do SGCG, isso cobre uns 10 — as outras ~150 caíam no mesmo hash
cru de 32 caracteres, mesmo em Simular. Era essa lacuna, não o
Anonimizar, que impedia o Rafa de gerar a planilha simulada que queria.

**A correção:** `fabricarGenericoFormatAware()`, função pura — preserva
a FORMA do original, caractere por caractere: dígito vira dígito, letra
maiúscula vira letra maiúscula, letra minúscula vira minúscula, o resto
(espaço, barra, @, traço) fica igual. "220" vira outro número de 3
dígitos. "JOAO DA SILVA" vira outro nome de 2 palavras, maiúsculo,
mesmo formato. Um e-mail mantém a forma `usuario@dominio.com`.

**Datas são caso à parte:** randomizar dígito a dígito podia gerar
"99/37/2028" (mês inválido). `pareceDataBruta()` detecta o formato cru
do SGCG (AAAAMMDD ou AAAA-MM-DD) e usa o `deslocarData()` que já existe
(mesmo mecanismo das colunas `DT-` em Manter) — sempre uma data real,
deslocada e coerente pela matrícula.

**Consistência preservada:** os dois geradores passam pelo
`valorSintetico()`/`previaValorSintetico()` já existentes — mesmo valor
original, mesma coluna, sempre o mesmo valor sintético dentro do lote
(cache por `tipo + valor normalizado`). Isso não mudou meta nenhuma do
mecanismo, só ganhou mais um "tipo" (`GENERICO`) na mesma engrenagem.

**Os 9 tipos conhecidos não mudaram.** `tipoSimulacao()` continua
checando nome primeiro; só o fallback final trocou de hash pra
genérico. A prévia nos cartões (Parte 19) ganhou o mesmo tratamento, com
o sal isolado de sempre — não toca no lote real.

**Teste:** script Playwright fora do repo — UNIDADE "220" processa pra
outro número de 3 dígitos, LOCAL "001" pra uma série diferente (cada
coluna com sua própria aleatoriedade), data bruta vira DD/MM/AAAA válida
(mês 1–12, dia 1–31), duas linhas com o mesmo original geram o mesmo
sintético, e NOME-CLIENTE continua usando o gerador de nomes dedicado.
14 verificações OK. `patches/_testa_seletor.py` (24) e
`_test_regressao_completa.py` (21), sem quebra.

**Falta (combinado com o Rafa):** agora que Simular preserva formato em
qualquer coluna, as 6 linhas de ajuda ao lado de cada bolinha (que
ficaram pendentes por essa mesma lacuna) podem entrar — a frase do verde
finalmente é verdade em qualquer coluna, não só nas 10 conhecidas.

---

## PARTE 27 — Detecção de tipo + edição manual em lote dentro dos cartões (2026-10-19, v4.11)

O Rafa achou vaga a primeira proposta ("parece que tá fazendo coisa tão
simples") e pediu base em conhecimento consolidado. Pesquisado antes de
codar: Microsoft Presidio, Purview e Google DLP (reconhecedor = padrão +
validação + palavra-chave), SDV do MIT (detecção é só ponto de partida,
a pessoa confirma; gerar falso sem guardar o mapa de volta), visions /
pandas-profiling (do tipo genérico ao mais específico), NIST FF1 (o
padrão de "embaralhar mantendo formato" exige 1 milhão de combinações —
campo de 3 dígitos é pequeno demais pra isso).

**1. Fórmulas num lugar só (`FABRICAS`).** Os geradores de CPF, RG,
telefone, nome, CEP e número estavam copiados em 3 lugares (processamento,
prévia, edição manual). Viraram um objeto só; quem chama escolhe a fonte
do acaso (sal do lote, sal da prévia ou `crypto` puro no chute manual).
Entraram CNPJ (com a regra alfanumérica da Receita, em vigor desde
jul/2026) e Data (AAAAMMDD, AAAA-MM-DD e DD/MM/AAAA; 31/02 não passa).
CPF e CNPJ inventados agora mantêm a pontuação do original.

**2. Reconhecedores de tipo.** Ao carregar o arquivo, até 2.000 linhas são
lidas e cada coluna é testada contra 12 tipos (CPF, CNPJ, e-mail, data,
telefone, CEP, matrícula, RG, valor, nome, código/categoria, número de
imóvel). Nível na escala do Purview: alta / média / baixa — tipo com
dígito verificador sozinho chega em média; com a palavra no nome da
coluna, alta. CEP na faixa do Paraná (80000–87999) conta como prova.
Coluna com menos de 5 valores não arrisca palpite. Cada cartão ganhou um
selo ("CPF? · média"); clicar explica o porquê ("100% das 30 linhas
passam no dígito verificador") e pergunta "É isso?" — sim, ou escolhe
outro tipo. "Confirmar as N" confirma de uma vez os de confiança alta.

**3. Tipo confirmado guia o Simular.** Uma coluna de nome qualquer que
guarda CPF passa a receber CPF inventado com DV válido no arquivo inteiro.
Endereço e lote continuam pelo nome (trocam por valor real do mesmo
bairro/quadra, melhor que qualquer gerador) — o selo deles diz isso.

**4. Edição manual em lote, dentro dos cartões (pedido do Rafa).** A caixa
grande por cima da tela saiu. Selecionou colunas → bolinha índigo da barra
preta → o cartão cresce ali mesmo na grade. "← Anterior / Próxima →"
navega entre os cartões sem perder nada. As mesmas N linhas (1 a 50) valem
pra todas as colunas — cada linha vira um registro inteiro.
- Cada campo já nasce com um **chute** do tipo da coluna, **conferido**
  contra todos os valores reais carregados: se bater, chuta de novo (até
  50 vezes; se não der, avisa em vez de travar).
- "↺" traz o original pra escrever por cima. "Chutar de novo" troca só o
  que a pessoa não digitou.
- Valor igual a um dado real (da mesma linha ou de outra) fica vermelho
  com o aviso, e só passa marcando "manter igual de propósito".
- **Uma revisão no fim do lote**: resumo por coluna, as linhas iguais a
  dado real listadas, aviso de risco. Com pendência, não aplica.
- **Recorte**: ligado por padrão quando são várias colunas — o arquivo
  final sai só com as N linhas (aviso fixo nas opções avançadas, com
  botão pra desligar). Soma com recorte anterior em vez de cortar linha
  que outro lote já editou.
- A barra preta some enquanto o lote está aberto (cobria os campos).

**Teste:** 4 scripts Playwright fora do repo — prévia (15), simulação
genérica (14), tipos (27: os 11 tipos detectados certo, inclusive o CPF
escondido em COMPLEMENTO, e o arquivo final com CPF válido nessa coluna)
e lote manual (35: navegar, voltar, chute ≠ todos os reais, aviso de
igual, revisão bloqueando com pendência, arquivo final com 5 linhas e os
valores exatamente como revisados). `patches/_testa_seletor.py` (24) e
`_test_regressao_completa.py` (21), sem quebra. Aba Auditoria atualizada.

**Achados fora do escopo (não mexidos, avisados ao Rafa):**
- `MAPA_DELTA_DATA` não é limpo em `destruirSalEfemero()`: dois lotes na
  mesma sessão reaproveitam o deslocamento de data por matrícula — quebra
  a promessa "lotes diferentes não se cruzam" da aba Auditoria.
- No modo CSV o cabeçalho é processado como se fosse linha de dado.
- A última linha some se o arquivo não terminar com quebra de linha
  (sobra no `buffer` e nunca é processada).

**Versão v4.11:** subiram juntos title, badge, 4 rodapés, `VERSAO_LOCAL`,
`sw.js`, `version.json`, README, `package.json`.

---

## PARTE 28 — Nada some, nada sobra, nada cruza (2026-10-19, v4.12)

**Pedido do Rafa:** corrigir os 3 achados fora do escopo da PARTE 27.
Na correção apareceram mais 2 defeitos no mesmo código; entraram juntos.

**1. Datas não cruzam mais entre lotes.** `destruirSalEfemero()` agora
limpa `MAPA_DELTA_DATA`. Antes, dois lotes seguidos na mesma aba
reaproveitavam o deslocamento de data de cada matrícula — dava pra
cruzar os dois arquivos.

**2. Cabeçalho do CSV não vira registro.** A linha 0 do CSV é pulada no
processamento: o arquivo final já escreve o cabeçalho dele.

**3. A última linha não some.** Arquivo sem quebra de linha no fim
perdia o último registro (ficava no `buffer`). Corrigido nos 5 lugares
que leem o arquivo: processamento, coleta dos pools de troca, valores
distintos do filtro, carga da edição manual e detecção de tipo.

**4. Troca de rua e de lote alinhada por posição.** O recorte da v4.11
(e rua vazia no meio do bairro) desalinhava o contador de ocorrências:
uma linha podia receber a própria rua de volta, e rua vazia ganhava rua.
Agora a coleta grava a posição de cada linha no pool (`POOL.posRua`,
`POOL.posLote`, com a mesma numeração do processamento) e a troca usa
essa posição. Rua vazia continua vazia.

**5. Lote sozinho na quadra não vaza mais.** Sem ninguém pra trocar, o
número REAL do lote passava direto (setor + quadra + lote identificam o
imóvel). Agora vira um lote inventado no mesmo formato.

**Teste:** script Playwright fora do repo com 17 verificações, rodado
nas duas versões. Na v4.11: 9 falhas (datas 20 de 20 iguais, cabeçalho
virando linha, última linha sumindo no CSV, no TXT e na edição manual,
8 a 12 linhas com a própria rua em 6 lotes, rua vazia preenchida, 1 a 3
com a própria rua no recorte, 4 lotes reais vazando — os números variam
porque o sal muda a cada rodada). Na v4.12: 17 de 17, em toda rodada.
As 4 suítes anteriores (15 + 14 + 27 + 35), `_testa_seletor.py` e
`_test_regressao_completa.py` passaram sem mudança. Aba Auditoria
ganhou a linha "Nada some, nada sobra, nada cruza".

**Versão v4.12:** subiram juntos title, badge, 4 rodapés, `VERSAO_LOCAL`,
`sw.js`, `version.json`, README, `package.json`.

---

## PARTE 29 — Copiar o VTO, com assistente (2026-10-19, v4.13)

**Pedido do Rafa:** "esse negócio de pasta, zip, ficou confuso". Salvar
um ZIP, ver o que o app mostra e fazer uma coisa assistida.

**O que estava esquisito (visto salvando um ZIP de verdade):**
- Janela cinza do navegador, sem acento: "O pacote vai levar o
  aplicativo vazio... Gerar o ZIP?".
- O ZIP caía calado em Downloads, sem dizer onde nem o que fazer depois.
- Dentro do ZIP, dois `.html` (`index.html` e `anonimizador.html`):
  ninguém sabia qual abrir. O segundo era sobra do tempo em que o
  Anonimizador era arquivo irmão; hoje ele vai dentro do VTO em Base64.
- Os arquivos do ZIP não tinham data (Windows mostrava em branco;
  extraídos, ficavam com 1980).
- A ajuda do "?" dizia "um arquivo só" (eram dois) e mandava "abrir a
  pasta" de um ZIP ainda não extraído.
- Achado no caminho: clicar no fundo escuro de qualquer ajuda fechava
  como se fosse a janela das datas. A caixa ficava com o texto da ajuda
  e o próximo serviço registrado quebrava (`modalTitulo` nulo).

**O que mudou:**
- Botão do topo virou **📦 Copiar o VTO** (verbo + o programa, para não
  confundir com "Salvar Arquivo", que é o JSON dos dados).
- Abre um assistente no lugar do `confirm()`:
  1. **Para que é a cópia?** "Usar no computador" (arquivo `.html`) ou
     "Mandar para alguém" (o mesmo arquivo dentro de um ZIP, que passa
     melhor por e-mail). A frase de cima diz que as matrículas não vão.
  2. **Salvar:** no Edge/Chrome abre o "Salvar como" do Windows, já em
     Downloads e com o nome certo — a pessoa escolhe a pasta. Fechou sem
     salvar: volta para a escolha. Sem o "Salvar como" (Firefox, ou
     bloqueado pela empresa): download normal.
  3. **Cópia salva:** nome do arquivo, onde está e como abrir. No ZIP:
     "botão direito → Extrair tudo → Extrair", e por que extrair.
- A cópia é **um arquivo só**, `VTO-v4.13.html`, solto ou dentro do ZIP.
  O banner de nova versão baixa com o mesmo nome.
- ZIP com data e hora de verdade.
- Clique no fundo fecha a janela certa (config, ajuda ou datas).

**Teste:** script Playwright fora do repo com 34 verificações: sem
janela do navegador, Esc, clique no fundo nas 3 janelas e registro de
serviço depois, download do `.html` e do ZIP, ZIP íntegro com um
arquivo e a data de hoje, "Salvar como" simulado (nome sugerido, pasta,
cancelar, bloqueio da empresa, nome com `<b>` aparece como texto),
matrícula-armadilha fora da cópia, celular 375 px, a cópia abre com as 6
abas e o Anonimizador. Atualizados para o fluxo novo:
`_test_regressao_completa.py`, `_test_zip_leak_csv.py` (armadilha: 0),
`_test_etapa1.py` (24) e `_testa_ajuda_zip.py`. `_testa_seletor.py` sem
mudança. AGENTS.md: mapa do ZIP atualizado.

**Não testado:** o "Salvar como" real do Windows (o navegador de teste
não mostra essa janela; foi simulado). Conferir no Edge da Sanepar.

**Versão v4.13:** subiram juntos title, badge, 4 rodapés, `VERSAO_LOCAL`,
`sw.js`, `version.json`, README, `package.json`.

---

## PARTE 30 — Salvar do Anonimizador sem surpresa (2026-10-19, v4.14)

**Pedido do Rafa:** simular um TXT e um CSV e conferir o salvar
(exportar, escolher pasta), que estava estranho.

**O que estava estranho (simulado pela aba 6 do VTO):**
- Com um arquivo só, o nome original sumia: `SGCG_outubro.txt` saía
  `_ANONIMIZADO.csv`. A tela prometia "NomeOriginal + Sufixo" — e com
  dois arquivos era assim mesmo. Comportamento diferente pela quantidade.
- Na pasta escolhida, o lote seguinte **gravava por cima** do anterior
  (mesmo `_ANONIMIZADO.csv`), sem perguntar.
- A janela de pasta abria em Downloads, que o Edge/Chrome **recusa**
  (Downloads, Documentos e Área de Trabalho só servem por subpasta).
  Fechando a janela, nada acontecia e o log parava em "sal gerado".
- "Downloads (Padrão)" escrito numa opção e a outra vinha marcada.
- O certificado ia sempre para Downloads, com nome fixo
  `CERTIFICADO_ANONIMIZACAO.txt`, mesmo com pasta escolhida.
- Nenhum aviso de "pronto": só o log preto.

**O que mudou (`anonimizador.html`, embutido no `index.html`):**
- **3. Nome do arquivo final:** sempre nome do original + o fim do nome
  (`nomeSaidaDe`), com prévia ao vivo ("Vai sair: ...") e o aviso de que
  sai em CSV (separado por ;) mesmo vindo de TXT. Caracteres que o
  Windows recusa viram `_`. Fim do nome vazio: diz por que não pode.
- **4. Onde salvar:** "⬇️ Pasta Downloads" vem marcada (sem dois
  diálogos do navegador). "📁 Escolher uma pasta" explica antes que é
  preciso criar uma pasta dentro de Downloads/Documentos/Área de Trabalho.
  A pasta é escolhida **antes** do sal nascer; a pasta fica lembrada na
  aba (os próximos lotes não perguntam de novo) com "Trocar pasta".
- **Nunca grava por cima** (`nomeLivreNaPasta`): `nome (2).csv`,
  `nome (3).csv`... vale para o CSV e para o certificado.
- Erro ao gravar na pasta: cai em Downloads e esquece a pasta — antes os
  arquivos seguintes iam para os dois lugares.
- **Caixa de pronto** abaixo do botão: arquivos, onde estão e o que falta
  (o certificado). Pasta recusada: caixa laranja explicando o que fazer.
- **Certificado** com nome do lote (`<arquivo>_CERTIFICADO.txt` ou
  `LOTE_N_ARQUIVOS_CERTIFICADO.txt`), salvo no mesmo lugar do CSV.
  Botão: "📜 Salvar o certificado do lote". Some quando começa um lote novo.

**Teste:** script Playwright fora do repo com 37 verificações (TXT, CSV,
dois CSV, pasta simulada com dois lotes seguidos, pasta recusada,
bloqueada pela empresa, erro ao gravar, permissão perdida). As outras 6
suítes do Anonimizador e do VTO, `_test_regressao_completa.py`,
`_testa_seletor.py`, `_test_etapa2_validacao.py` (baixou
`dados_ficticios_ANONIMIZADO.csv` pela aba 6), `_test_zip_leak_csv.py`
e `_test_etapa1.py` passaram. Aba Auditoria: linha "Salvar sem apagar nada".

**Não testado:** as janelas reais do Edge (escolher pasta, "pode editar
arquivos?", recusa de Downloads). O navegador de teste não mostra essas
janelas; foram simuladas. Conferir no Edge da Sanepar.

**Versão v4.14:** subiram juntos title, badge, 4 rodapés, `VERSAO_LOCAL`,
`sw.js`, `version.json`, README, `package.json`.
