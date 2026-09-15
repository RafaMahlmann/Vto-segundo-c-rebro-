# AGENTS.md — Protocolo de trabalho para IA neste projeto

> **Leia este arquivo INTEIRO antes de tocar em qualquer código.**
> Ele existe porque sessões anteriores de IA destruíram partes funcionais do
> aplicativo ao fazer alterações "pequenas". O histórico de git mostra 5
> commits revertidos em sequência (ícones Font Awesome, chips refeitos, banner
> de atualização, bump de versão) — todos desfazendo estragos de sessões de IA.
> As regras abaixo são inegociáveis.

---

## 1. O que é este projeto (30 segundos)

- `index.html` **é o aplicativo inteiro**: ~3.110 linhas / ~263 KB, HTML + CSS + JS monobloco.
- Desses 263 KB, ~96 KB são o **anonimizador embutido em Base64** (`<script id="anonimizadorFonte">`).
- **Zero dependências externas.** Sem CDN, sem framework, sem fonte externa, sem biblioteca de ícones.
- Motivo: o arquivo precisa sobreviver ao fluxo **Google Docs → Bloco de Notas → renomear para .html**.
- 6 abas: `prazo` (Calculadora de Sanção de Esgoto), `dilacao`, `fluxo`, `matriculas`, `estatisticas`, `anonimizador`.
- A aba 6 roda o **Anonimizador LGPD v19** dentro de um `iframe srcdoc`, alimentado pelo Base64 embutido.
  **Não existe dependência de arquivo irmão.** O `anonimizador.html` da raiz é só a fonte de edição.
- O usuário (Rafa) é gestor de VTO da Sanepar e **disléxico**: linhas curtas, uma ideia por parágrafo.

---

## 2. Fonte da verdade

- **O código (`index.html`) é a verdade.** Documentos `.md` descrevem intenção e podem estar desatualizados.
- **Se um documento divergir do código, NÃO "corrija" o código para bater com o documento.** Pare e pergunte ao Rafa.
- Divergências conhecidas hoje (não são bugs do código):
  - O app está em **v4.4** (título, badge, 4 rodapés, `VERSAO_LOCAL`, `sw.js` e `version.json` sobem juntos).
  - README descreve a aba 1 como "soma de dias úteis/corridos"; ela foi substituída pela **Calculadora de Sanção de Esgoto** (`calcularPrazoSancao`).
  - README diz "nenhum uso de `fetch()`"; existe **uma exceção autorizada**: o verificador de nova versão (seção 5, linhas ~2398–2426).

---

## 3. PROTOCOLO DE EDIÇÃO CIRÚRGICA — a regra mais importante

1. **Nunca reescreva o `index.html` inteiro.** Proibido gerar o arquivo do zero, "reorganizar" blocos ou reformatar trechos que não foram pedidos. Toda alteração é uma **substituição localizada** de trecho.
2. **Toque apenas no que foi pedido.** Se o pedido é a aba Dilação, nada na navegação, no CSS global ou nas outras 4 abas pode mudar. Um `diff` com linhas fora do escopo = sinal de que você fez algo errado.
3. **Antes de editar, declare o plano:** qual(is) trecho(s) serão alterados (função / id / linhas aproximadas) e o que **não** será tocado. Mudança que cruza mais de uma aba ou mais de uma seção do mapa (seção 5) exige confirmação do Rafa antes.
4. **Use âncoras.** Localize o trecho exato pelos comentários `// ===== NOME =====`, `<!-- ABA N -->` ou pelo `id` do elemento. Se a âncora não for encontrada, **pare e avise** — não improvise nem "aproxime".
5. **Preserve estilo local.** O código não usa acentos em identificadores por compatibilidade com o fluxo Google Docs. Mantenha o padrão do trecho vizinho (aspas, indentação, nomes).
6. **Depois de editar, rode o checklist** (seção 6) antes de dizer que está pronto.

---

## 4. Proibições explícitas (todas já aconteceram e tiveram que ser revertidas)

- ❌ Adicionar Font Awesome, Bootstrap, Tailwind, Google Fonts ou **qualquer** CDN/biblioteca.
- ❌ Adicionar `fetch()`, `import`, `require` novos (única exceção existente: verificador de versão).
- ❌ Mudar número de versão (badge do header, footers, `version.json`) sem o Rafa pedir.
- ❌ Reescrever textos visíveis na tela sem aplicar a skill `.claude/skills/voz-do-vto/SKILL.md`.
- ❌ Acentos ou cedilha em IDs, classes, nomes de função/variável (quebra no fluxo Google Docs → Bloco de Notas).
- ❌ `localStorage` / `sessionStorage` (dados persistem só via exportar/importar JSON).
- ❌ "Melhorias", refatorações, renomeações ou limpezas não solicitadas.
- ❌ Remover funções "aparentemente não usadas" — num monobloco, quase tudo é chamado por `onclick` inline no HTML.
- ❌ Criar arquivos novos na raiz sem necessidade (scripts de patch temporários vão para a pasta `patches/`).

---

## 5. Mapa do `index.html`

Use este mapa para localizar trechos **sem reescrever o arquivo**. Os números de linha são aproximados (mudam a cada edição); as âncoras de comentário são estáveis.

| Âncora | Linhas aprox. | Conteúdo |
|---|---|---|
| `<style>` | 10–336 | Todo o CSS. Seções comentadas: DILACAO, FLUXO, TABELA, CALENDARIO, SANCAO, BANNER, ESTATISTICAS |
| `<!-- ABA 1 -->` | 360–382 | Calculadora de Sanção de Esgoto |
| `<!-- ABA 2 -->` | 383–435 | Calculadora de Dilação (simples + caso especial) |
| `<!-- ABA 3 -->` | 436–558 | Fluxo de Vistorias VTO (3 colunas, cards de sanção) |
| `<!-- ABA 4 -->` | 559–622 | Matrículas (tabela mestre) |
| `<!-- ABA 5 -->` | ~690–745 | Estatísticas (Canvas) |
| `<!-- ABA 6: ANONIMIZADOR -->` | ~747–757 | `iframe#anonimizadorFrame` (sem `src`) + aviso de falha |
| `// ===== DADOS =====` | 711+ | `matriculas[]`, estrutura central — **nunca mudar sem atualizar todos os consumidores** |
| `// ===== UNDO / REDO =====` | ~809+ | **Duas pilhas**: `historico` (antes) e `historicoFuturo` (desfeito). Chamar `salvarHistorico()` **antes** de alterar `matriculas[]` — quem guarda o estado de agora é o `undo()` |
| `// ===== CONFIGURACAO DE PRAZOS =====` | 769+ | `prazosPorCodigo` (padrão 30 dias, em memória) |
| `// ===== SISTEMA DE ABAS =====` | ~904+ | `mostrarAba()` + auto-foco + carrega a aba 6 sob demanda |
| `// ===== ABA 6: ANONIMIZADOR EMBUTIDO =====` | ~922+ | `carregarAnonimizador()` — decodifica o Base64 para o `srcdoc` |
| `// ===== ABA 1: ... SANCAO =====` | 968+ | `calcularPrazoSancao()` |
| `// ===== ABA 2: DILACAO =====` | 1029+ | `calcularDilacao()` + funções do caso especial |
| `// ===== ABA 4: MATRICULAS =====` | 1087+ | CRUD da tabela |
| `// ===== MODAL =====` | 1456+ | Modal de datas (teclado: Tab/Enter/Espaço/Esc) |
| `// ===== TIMELINE =====` | 1525+ | Timeline inferior proporcional (marcador 180 dias) |
| `// ===== GRAFICOS CANVAS =====` | 1713+ | 4 gráficos da aba Estatísticas |
| `// ===== CONTADOR 180 =====` | 2077+ | Contagem a partir da 1ª data de criação da matrícula |
| `// ===== EXPORTAR/IMPORTAR =====` | ~2420+ | CSV e JSON |
| `// ===== GERAR ZIP PORTATIL =====` | ~2728+ | `prepararHtmlLimpo()` + `gerarZipCompleto()` + `criarZipMulti()` |
| `// ===== DADOS MOCK =====` | 2310+ | `gerarMockData()` — 30 matrículas de demonstração |
| `// ===== VERIFICADOR DE NOVA VERSAO =====` | ~2661+ | Único `fetch()` autorizado + `versaoEhMaior()` |

Consumidores de `matriculas[]` (se mexer na estrutura, todos quebram):
`renderMatriculas`, `atualizarTimeline`, `renderGraficos`, `exportarCSV`,
`exportarJSON`, `verificarSancoes`, contador de 180 dias.

---

## 6. Checklist obrigatório antes de declarar pronto

- [ ] Abrir o `index.html` no navegador e conferir o console (F12): **zero erros**.
- [ ] As **5 abas abrem** e renderizam (não só a aba alterada).
- [ ] A funcionalidade pedida funciona com dados reais e com o mock.
- [ ] Adjacências da aba alterada ainda funcionam (ex.: mexeu em data? testa o botão 📅 de calendário).
- [ ] `Ctrl+Z` / `Ctrl+Shift+Z` continuam funcionando.
- [ ] Timeline inferior renderiza ao clicar numa matrícula.
- [ ] Exportar/importar JSON continua funcionando.
- [ ] Textos novos passaram pelas regras de `voz-do-vto` (sem acento em código, botão com verbo, mensagem de erro direta).
- [ ] Existe o script `agente_vto.py` (Playwright) para teste automatizado com screenshots — prefira ele a "conferir só no olho" quando a mudança for estrutural.

Se não deu para testar algo, **diga explicitamente o que não foi testado**. Nunca declare "pronto" no escuro.

---

## 7. Git e segurança

- Antes de qualquer alteração: rodar `git status`. Se houver mudanças não commitadas, **não** commitar, reverter ou "organizar" por conta própria — são trabalho do Rafa em andamento.
- Em mudança grande: **sugerir um commit de segurança antes de começar** (ponto de restauração).
- Nunca `git revert`, `git reset` ou `git checkout --` sem pedido explícito.
- Nunca commitar sem o Rafa pedir.

---

## 8. Versionamento e documentos

- Versão só muda **a pedido**. Quando mudar, atualizar juntos: badge do header, footers das abas, `version.json`, `<title>`, README.md e TIMELINE.md.
- Ao concluir uma entrega relevante, registrar em `TIMELINE.md` (nova "PARTE") para a próxima sessão não trabalhar com mapa velho.
- Ao mudar comportamento documentado no README.md, atualizar o README na mesma entrega — doc divergente é o que faz a próxima IA "corrigir" o código errado.

---

*Criado em 2026-08-19 após análise dos incidentes das sessões anteriores. Atualizado em 2026-09-14. App em v4.4.*

---

## 9. Duas regras que nasceram da Etapa 1–4 (2026-09-14)

**O export NÃO pode serializar o DOM vivo.**
`gerarZipCompleto()` usa `prepararHtmlLimpo()`, que clona o documento e apaga
tudo que foi gerado na tela antes de empacotar. Sem isso o arquivo distribuído
levava as matrículas em texto claro — incidente de LGPD — e duplicava as setas
das roletas a cada ciclo exportar/reabrir.
Mexeu em algo que é renderizado em tempo de execução? Acrescente a limpeza
correspondente em `prepararHtmlLimpo()` — ela é o plano B.

**Não insira nada entre o `</script>` principal e o bloco `RETRATO DO ARQUIVO LIMPO`.**
Esse bloco precisa ser o último do `<body>`. Ele tira a cópia do documento antes
de o app desenhar a primeira coisa, e só então chama `aplicarVersaoDinamica()`,
`gerarMockData()`, `initRoletas()`, `atualizarTodasRoletas()` e
`alternarModoFluxo('grade')`.
Qualquer `<script>`, `defer` ou imagem grande colocado nessa fresta passa a rodar
antes do retrato. O retrato é tirado uma única vez, então o arquivo sairia sujo
em **todo** export daquela sessão — e ninguém perceberia.

**Editou o `anonimizador.html`? Rode `patches/embutir_anonimizador.py`.**
A aba 6 e o ZIP leem os dois do mesmo bloco Base64. Sem regerar, a aba mostra a
versão nova e o pacote distribui a velha — e a v18.2.2 do anonimizador foi
reprovada em pentest. O script deixa o Base64 byte a byte igual ao arquivo em
disco, então dá para conferir a qualquer momento.

**Desfazer e refazer são duas pilhas, não um índice.**
`salvarHistorico()` é chamado **antes** de alterar `matriculas[]` — os 9 pontos
que fazem isso estão certos e não devem mudar. A consequência é que o estado
*atual* nunca está em `historico`: quem o empilha é o `undo()`, em
`historicoFuturo`, no instante em que desfaz.
Foi a falta disso que deixou o Refazer quebrado desde sempre — com uma pilha só
e um índice, o estado pós-alteração não existia em lugar nenhum.
Ao criar uma função que altera `matriculas[]`: chame `salvarHistorico()` antes,
e só isso. Não empilhe nada depois, não mexa em `historicoFuturo`.
Para definir um novo ponto de partida (carga de dados, não alteração do
usuário), use `limparHistorico()` — é o que o `gerarMockData()` faz.
