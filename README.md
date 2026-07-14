# VTO Segundo Cerebro — Aplicativo de Gestao de Vistorias Tecnicas Operacionais

## IDENTIDADE DO PROJETO

- **Nome:** VTO Segundo Cerebro
- **Natureza:** Aplicativo web monobloco HTML (zero dependencias externas)
- **Dominio:** Gestao de Vistorias Tecnicas Operacionais (VTO) da Sanepar
- **Norma Base:** IT OPE 1580 — Vistorias Tecnicas Operacionais em Ligacoes Prediais de Esgoto
- **Repositorio:** `RafaMahlmann/Vto-segundo-c-rebro-` (GitHub)
- **Versao Atual:** 3.2 (Timeline Proporcional + 30 Mocks)

---

## REGRA INQUEBRANTAVEL DE TRANSFERENCIA

O aplicativo DEVE funcionar seguindo este fluxo de transferencia:

```
Codigo HTML → Copiar → Google Docs → Bloco de Notas → Renomear para .html → Funciona
```

**Consequencias:**
- Zero dependencias externas (nenhum CDN, nenhum framework, nenhuma biblioteca)
- Nenhum uso de `fetch()`, `import`, `require`, `module`
- Tudo inline: CSS no `<style>`, JavaScript no `<script>`, dados em memoria
- Sem imagens externas (emojis Unicode para icones)
- Sem localStorage (dados persistem via exportar JSON / importar JSON)

---

## ARQUITETURA

### Tecnologia
- HTML5 semantico
- CSS3 (flexbox, grid, custom properties limitadas, canvas)
- JavaScript vanilla (ES6+, sem frameworks)
- Canvas API nativa para graficos

### Estado da Aplicacao
```javascript
// Estrutura de dados principal
let matriculas = [
  {
    numero: "10045213",      // 8 digitos
    servicos: [
      {
        codigo: "8403",       // codigo do servico VTO
        dataCriacao: "2024-01-15",   // data SGC (AAAA-MM-DD)
        dataBaixa: "2024-02-20"      // data vistoria (null = em aberto)
      }
    ],
    ativa: false             // flag de matricula selecionada
  }
];

let matriculaAtiva = null;   // numero da matricula em foco
let servicoPendente = null;  // servico aguardando modal de datas
```

### Historico Undo/Redo
- Sistema de snapshots JSON com pilha de 50 estados
- `Ctrl+Z` desfaz, `Ctrl+Shift+Z` refaz
- Estado salvo automaticamente antes de toda operacao destrutiva

---

## ESTRUTURA DE ABAS

O aplicativo possui 5 abas principais:

### Aba 1: Calculadora de Prazo
- Calcula datas futuras somando dias uteis ou corridos
- Caso de uso: prazo de recurso de multa (30 dias da fatura)
- Input: data inicial, quantidade, tipo (uteis/corridos)
- Output: data final formatada + info adicional

### Aba 2: Calculadora de Dilacao
- Calcula prazos de dilacao (30, 60 ou 90 dias)
- Caso de uso: cliente solicita prazo adicional para regularizar
- Input: data base, quantidade (dropdown), tipo
- Output: data final com badge identificador

### Aba 3: Fluxo de Vistorias VTO
- Interface visual em 3 colunas representando as 3 fases do processo
- 18 codigos de servico distribuidos nas fases
- Cards de sancao com ativacao automatica baseada em datas
- Matricula ativa sincronizada com aba Matriculas

### Aba 4: Matriculas (CRUD Principal)
- Tabela mestre estilo Excel com 10 colunas
- 30 matriculas mock para demonstracao, distribuidas propositalmente entre:
  - Novas (sem servico)
  - 1a vistoria (em aberto / baixada OK / baixada em alerta / com servicos complementares)
  - 2a vistoria (em aberto / baixada / com 1a sancao ativa ou aplicada)
  - 3a vistoria (em aberto / baixada / com multa dobro ativa ou aplicada)
  - Matriculas que ja estouraram os 180 dias
- Resumo em cards (Total/OK/Atencao/Critico)
- Operacoes: adicionar, remover, selecionar, desfazer/refazer
- Timeline inferior sincronizada com matricula selecionada

### Aba 5: Estatisticas (Dashboard Canvas)
- 4 KPIs em cards resumo
- 4 graficos Canvas: barras (fases), rosca (status), linha (evolucao), barras horizontais (tempo/codigo)
- Dados computados em tempo real a partir de `matriculas[]`
- Max-width 1100px para manter proporcoes em telas grandes

---

## FLUXO DE VISTORIAS VTO (3 FASES)

```
1a VISTORIA (Prog. inicial)          2a VISTORIA (60 dias - Multa)         3a VISTORIA (60 dias - Multa DOBRO)
+----------------------------+       +----------------------------+       +----------------------------+
| 8403 - 1a Vistoria + AS    |  -->  | 8405 - 2a Vistoria         |  -->  | 8428 - 3a Vistoria         |
| 8421 - 1a Vistoria         |       |                            |       |                            |
| 8402 - Rec. Tarifaria      |       | SANCao: 1a SANCAo          |       | SANCao: MULTA DOBRO        |
| 8400 - Solic. Cliente      |       | (ativacao automatica)      |       | (ativacao automatica)      |
| 8409 - Orient. Tecnica     |       +----------------------------+       +----------------------------+
| 8470 - Habite-se +600      |
| 8480 - Habite-se -600      |
+----------------------------+
```

### Ciclos de Prazo
- Cada fase: **60 dias corridos**
- Limite total: **180 dias corridos** (contador na timeline)
- Apos 180 dias: status "Excedido" com alerta visual vermelho

### Cards de Sancao
- **1a SANCAO (codigo simbolico: `1a_sancao`):** ativa automaticamente 60 dias apos baixa do 8405
- **MULTA DOBRO (codigo simbolico: `multa_dobro`):** ativa automaticamente 60 dias apos baixa do 8428
- Estados: inativo (cinza) → ativo (verde pulsante) → aplicado (azul)

---

## TIMELINE INFERIOR (PAINEL FIXO)

```
+--------------------------------------------------------------------------+
|  180 dias restantes  |  Dentro do prazo  |  [▼ Recolher]                 |
|  O=======O===========O====================|~~~~ 180d                       |
|  1a Vist.  2a Vist.   3a Vist.   (hoje)   [limite]                       |
+--------------------------------------------------------------------------+
```

- Posicao: fixed bottom, max-height 110px
- Reta graduada com marcos das 3 vistorias
- **Escala de proporcionalidade real:** o marcador de 180 dias e os eventos sao posicionados proporcionalmente aos dias reais desde a 1a criacao da matricula
- Marcador tracejado vermelho no dia 180
- Contador de dias restantes com cores dinamicas (verde → laranja → vermelho)
- Pontos de evento (criacao = azul, baixa = verde, aberto = cinza tracejado)
- Atualiza automaticamente ao selecionar matricula

---

## MODAL DE ALTA VELOCIDADE

Interface para registrar datas de servico com navegacao 100% por teclado:

| Tecla | Acao |
|-------|------|
| `Tab` | Pula entre campos |
| `Enter` | Salva (se data criacao preenchida) ou avanca para baixa |
| `Espaco` | Em aberto (sem baixa) — so funciona no campo de baixa |
| `Esc` | Cancela e fecha modal |

- Auto-focus no campo "Data de Criacao" ao abrir
- Nenhum clique de mouse necessario

---

## FORMATOS DE IMPORTACAO/EXPORTACAO

### CSV (Importar/Exportar)
- Delimitador: auto-detecta `;` ou `,`
- Colunas esperadas: Matricula, Servico, Data_Criacao, Data_Baixa
- Mapeamento flexivel de nomes de coluna
- Conversao automatica de datas (DD/MM/AAAA, AAAA-MM-DD, DD-MM-AAAA)

### JSON (Salvar/Abrir Arquivo)
```json
{
  "versao": "1.0",
  "data_exportacao": "2026-07-13T...",
  "total_matriculas": 30,
  "matriculas": [ ... ]
}
```
- Formato nativo da aplicacao
- Preserva todo o estado incluindo historico

---

## DOCUMENTOS SEMANTICOS RELACIONADOS (Pasta `/docs/`)

Os seguintes documentos foram extraidos de PDFs da Sanepar e transformados em MDs semanticos para consumo por IA:

### 01-legenda-categorias-matriculas.md
- Sistema de classificacao de 8 categorias (matriculas regularizadas, irregulares prefeitura, irregulares Sanepar, para analise, outras analises, improdutivas, multadas, com dilacao de prazo)
- Matriculas de exemplo por categoria (bairro Juveve)

### 02-resumo-estatistico-juveve.md
- Indicadores operacionais comparativos (Abril vs Maio 2024)
- Metricas: total na bacia, irregulares, multas, prorrogacoes, visitas realizadas, regularizacoes
- Dados parciais do bairro Juveve vs total da gerencia

### 03-codigos-resultados-vto.md (IA OPE 21169)
- **Grupo A (10-23):** VTO realizada com interligacao identificada
- **Grupo B (31-35):** VTO sem interligacao com rede coletora
- **Grupo C (51-61):** VTO nao realizada (impedimentos)
- **Grupo D (71-79):** VTO prorrogada (adiamento justificado)
- Referencias normativas: IA/COM/0453, IA/AMB/0033, ABNT 8160/99

### 04-objetivos-definicoes-vto.md (IA OPE 169)
- Glossario completo de siglas: ABNT, SANEPAR, DTI, HD, LPE, PV, RCE, SGC, VTO, AS
- Objetivos da padronizacao entre Gerencias Regionais
- Multi-stakeholder: clientes, Prefeituras, Ministerio Publico

### 05-instrucao-tecnica-vto.md (IT OPE 1580) + 05-instrucao-tecnica-vto-completo.md
- Documento-mae de 16 paginas (extraido de PDF de 44MB via OCR pagina por pagina)
- Diretrizes e procedimentos completos para VTO em ligacoes prediais
- Competencias, fluxo de processo, procedimentos de vistoria, preenchimento do AS
- Relacionamento cruzado com IA OPE 21169, IA OPE 169 e documentos de categoria

### 06-plano-diretor-carteira-vto.md
- Plano diretor de evolucao do aplicativo para carteira de matriculas em acompanhamento
- Define dois modos de visualizacao: individual (timeline 0-180) e coletivo (radar/fila de risco)
- Estabelece diretrizes de paginacao, filtros, priorizacao operacional e mesclagem de arquivos JSON sem servidor

---

## GLOSSARIO DE SIGLAS DO DOMINIO

| Sigla | Significado | Contexto |
|-------|-------------|----------|
| **VTO** | Vistoria Tecnica Operacional | Atividade principal do app |
| **SGC** | Sistema de Gerenciamento Comercial | Sistema corporativo Sanepar |
| **AS** | Atendimento de Servicos | Formulario de registro da vistoria |
| **DTI** | Dispositivo Tubular de Inspecao | Acesso ao ramal predial |
| **LPE** | Ligacao Predial de Esgoto | Conexao do imovel a rede |
| **PV** | Poco de Visita | Manutencao de redes coletoras |
| **RCE** | Rede Coletora de Esgoto | Infraestrutura publica |
| **HD** | Hidrometro | Medidor de consumo |
| **ETE** | Estacao de Tratamento de Esgoto | Destino do esgoto coletado |
| **PHS** | Projeto Hidrossanitario | Documentacao tecnica |
| **EPI** | Equipamento de Protecao Individual | Seguranca do operador |
| **END** | Esgoto Nao Domestico | Efluente especial |
| **ABNT** | Associacao Brasileira de Normas Tecnicas | Normas tecnicas |
| **SANEPAR** | Companhia de Saneamento do Parana | Concessionaria |
| **GR** | Gerencia Regional | Unidade operacional |
| **GCML** | Gerencia Comercial | Analise comercial |

---

## DECISOES ARQUITETURAIS CRITICAS

1. **Monobloco HTML:** Escolha obrigatoria devido a restricao de transferencia via Google Docs/Bloco de Notas
2. **Sem localStorage:** Dados nao persistem entre sessoes do navegador; uso de exportar/importar JSON
3. **Canvas para graficos:** Chart.js e similares exigem CDN; Canvas API nativa atende sem dependencias
4. **Max-width nos graficos:** 1100px para manter proporcoes consistentes em telas grandes
5. **Mock data de 30 matriculas:** Dados aleatorios gerados via `gerarMockData()` para demonstracao imediata
6. **Sistema de sanacao simbolica:** Codigos `1a_sancao` e `multa_dobro` nao sao codigos Sanepar oficiais; sao flags internas do app
7. **Prazo padrao de 30 dias:** `calcularStatusExecucao()` usa 30 dias como referencia para status OK/Alerta/Critico por servico
8. **Contador de 180 dias:** Calculado a partir da PRIMEIRA data de criacao da matricula ate a data atual
9. **Evolucao para carteira VTO:** O app deve evoluir para acompanhar grandes conjuntos de matriculas, reclassificando riscos diariamente com base na data atual, sem depender de servidor.
10. **Colaboracao offline:** Como nao ha backend em nuvem, trabalho em equipe deve ser resolvido por exportacao/importacao e mesclagem inteligente de arquivos JSON.

---

## REGRAS DE NEGOCIO

### Status de Execucao por Servico
- **OK:** Baixa realizada em ate 30 dias da criacao
- **Alerta:** Baixa realizada entre 30-60 dias
- **Critico:** Baixa apos 60 dias ou sem baixa (em aberto)

### Status Geral da Matricula (180 dias)
- **No prazo:** Mais de 120 dias restantes
- **Atencao:** Entre 60 e 120 dias restantes
- **Critico:** Entre 1 e 60 dias restantes
- **Excedido:** Passou dos 180 dias

### Fases do Processo
- **1a Vitoria:** Programacao inicial (codigos 8403, 8421, 8402, 8400, 8409, 8470, 8480)
- **2a Vitoria:** Revisao apos 60 dias (codigo 8405) + 1a SANCAO
- **3a Vitoria:** Revisao final apos mais 60 dias (codigo 8428) + MULTA DOBRO

---

*Documento gerado em 2026-07-13. Versao do aplicativo: 3.2*
