# AGENTS.md — Protocolo de trabalho para IA neste projeto

> **Leia este arquivo INTEIRO antes de tocar em qualquer código.**
> Ele existe porque sessões anteriores de IA destruíram partes funcionais do
> aplicativo ao fazer alterações "pequenas". O histórico de git mostra 5
> commits revertidos em sequência (ícones Font Awesome, chips refeitos, banner
> de atualização, bump de versão) — todos desfazendo estragos de sessões de IA.
> As regras abaixo são inegociáveis.

---

## 1. O que é este projeto (30 segundos)

- `index.html` **é o aplicativo inteiro**: ~2.430 linhas / ~147 KB, HTML + CSS + JS monobloco.
- **Zero dependências externas.** Sem CDN, sem framework, sem fonte externa, sem biblioteca de ícones.
- Motivo: o arquivo precisa sobreviver ao fluxo **Google Docs → Bloco de Notas → renomear para .html**.
- 5 abas: `prazo` (Calculadora de Sanção de Esgoto), `dilacao`, `fluxo`, `matriculas`, `estatisticas`.
- O usuário (Rafa) é gestor de VTO da Sanepar e **disléxico**: linhas curtas, uma ideia por parágrafo.

---

## 2. Fonte da verdade

- **O código (`index.html`) é a verdade.** Documentos `.md` descrevem intenção e podem estar desatualizados.
- **Se um documento divergir do código, NÃO "corrija" o código para bater com o documento.** Pare e pergunte ao Rafa.
- Divergências conhecidas hoje (não são bugs do código):
  - README.md e TIMELINE.md dizem "v3.2"; o app está em **v3.7**.
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
| `<!-- ABA 5 -->` | 623–708 | Estatísticas (Canvas) |
| `// ===== DADOS =====` | 711+ | `matriculas[]`, estrutura central — **nunca mudar sem atualizar todos os consumidores** |
| `// ===== UNDO / REDO =====` | 716+ | Snapshots; chamar `salvarHistorico()` **antes** de alterar `matriculas[]` |
| `// ===== CONFIGURACAO DE PRAZOS =====` | 769+ | `prazosPorCodigo` (padrão 30 dias, em memória) |
| `// ===== SISTEMA DE ABAS =====` | 813+ | `mostrarAba()` + auto-foco por aba |
| `// ===== ABA 1: ... SANCAO =====` | 968+ | `calcularPrazoSancao()` |
| `// ===== ABA 2: DILACAO =====` | 1029+ | `calcularDilacao()` + funções do caso especial |
| `// ===== ABA 4: MATRICULAS =====` | 1087+ | CRUD da tabela |
| `// ===== MODAL =====` | 1456+ | Modal de datas (teclado: Tab/Enter/Espaço/Esc) |
| `// ===== TIMELINE =====` | 1525+ | Timeline inferior proporcional (marcador 180 dias) |
| `// ===== GRAFICOS CANVAS =====` | 1713+ | 4 gráficos da aba Estatísticas |
| `// ===== CONTADOR 180 =====` | 2077+ | Contagem a partir da 1ª data de criação da matrícula |
| `// ===== EXPORTAR/IMPORTAR =====` | 2146+ | CSV e JSON |
| `// ===== DADOS MOCK =====` | 2310+ | `gerarMockData()` — 30 matrículas de demonstração |
| `// ===== VERIFICADOR DE NOVA VERSAO =====` | 2398+ | Único `fetch()` autorizado (lê `version.json` do GitHub) |

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

*Criado em 2026-08-19 após análise dos incidentes das sessões anteriores. App em v3.7.*
