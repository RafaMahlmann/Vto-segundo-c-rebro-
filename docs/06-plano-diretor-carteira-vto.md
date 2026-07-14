# Plano Diretor - Carteira VTO e Colaboracao Offline

## Objetivo Estrategico

Evoluir o VTO Segundo Cerebro de uma planilha operacional com timeline individual para um sistema local de acompanhamento de carteira. O aplicativo deve permitir que varias matriculas sejam acompanhadas ao longo do tempo, reclassificadas automaticamente a cada abertura com base na data atual, e priorizadas por risco operacional.

O foco deixa de ser apenas "registrar vistorias" e passa a ser:

1. saber quais matriculas estao mais proximas de estourar 180 dias;
2. saber quais servicos estao demorando demais entre criacao e baixa;
3. organizar a fila de trabalho por urgencia real;
4. permitir trabalho compartilhado sem servidor, por arquivos JSON mesclaveis.

---

## Premissas Inquebraveis

1. O aplicativo continua sendo um arquivo HTML monobloco.
2. Nao pode depender de servidor, banco externo, CDN, framework, `fetch`, `import`, `require` ou `module`.
3. Dados persistem por exportacao/importacao de JSON e CSV.
4. O Google Drive pode ser usado como pasta compartilhada de arquivos, mas nao como backend de sincronizacao em tempo real.
5. A colaboracao deve ocorrer por mesclagem controlada de arquivos gerados por usuarios diferentes.
6. O app deve continuar abrindo direto no navegador, mesmo em ambiente simples.

---

## Conceito Principal: Carteira de Matriculas

A matricula cadastrada passa a ser tratada como item de uma carteira em acompanhamento. Uma matricula pode estar tranquila hoje e se tornar critica no futuro apenas pela passagem do tempo.

Portanto, o arquivo salvo deve guardar fatos permanentes:

- numero da matricula;
- servicos;
- data de criacao do servico;
- data de baixa;
- observacoes;
- origem da alteracao;
- datas de criacao/atualizacao do registro.

O app deve recalcular estados temporais a cada abertura:

- dias restantes para 180;
- dias passados desde o dia zero;
- fase atual;
- risco;
- servico em aberto;
- atraso do servico;
- acao sugerida;
- prioridade na fila.

---

## Dois Modos de Visualizacao

### 1. Modo Individual

Usado para analisar uma matricula selecionada.

Deve conter:

- timeline individual;
- regua fixa de 0 a 180 dias;
- marcadores 0, 60, 120 e 180;
- eventos de criacao e baixa;
- barras de duracao de servicos;
- indicador de hoje;
- contador de dias restantes;
- alerta de prazo excedido.

Objetivo: explicar a historia temporal de uma matricula.

### 2. Modo Coletivo

Usado para gerir a carteira inteira.

Deve conter:

- radar de 180 dias;
- lista priorizada por risco;
- filtros por status, fase, servico, prazo e atraso;
- agrupamentos por faixa de risco;
- indicadores de servicos abertos ha mais de 30 dias;
- ranking das matriculas que exigem consulta/acao primeiro.

Objetivo: transformar o app em cockpit operacional.

---

## Painel de Risco Operacional

Criar uma aba futura chamada preferencialmente:

- Radar VTO;
- Carteira VTO;
- Painel de Risco;
- Fila Critica.

Campos sugeridos da tabela priorizada:

| Campo | Funcao |
|-------|--------|
| Matricula | Identificacao principal |
| Fase | 1a, 2a, 3a vistoria, sancao, excedida |
| Ultimo servico | Codigo mais recente ou aberto |
| Dias do servico | Dias entre criacao e baixa, ou criacao ate hoje |
| Dias 180 | Dias consumidos desde o dia zero |
| Restantes | Dias ate 180 |
| Risco | OK, atencao, critico, excedido |
| Acao sugerida | Consultar SGC, programar vistoria, atualizar baixa, avaliar sancao |

Ordem padrao:

1. excedidas;
2. faltando ate 15 dias;
3. faltando ate 30 dias;
4. servicos abertos ha mais de 30 dias;
5. servicos executados acima de 30 dias;
6. demais matriculas.

---

## Regra de Priorizacao

Cada matricula deve receber uma pontuacao de risco calculada em tempo real.

Exemplo conceitual:

```text
risco = pontosPrazo180 + pontosServicoAberto + pontosFase + pontosExcedido
```

Sugestao inicial:

| Condicao | Pontos |
|----------|--------|
| Passou de 180 dias | +100 |
| Faltam ate 15 dias | +80 |
| Faltam ate 30 dias | +60 |
| Faltam ate 60 dias | +35 |
| Servico aberto acima de 60 dias | +50 |
| Servico aberto entre 31 e 60 dias | +30 |
| Baixa executada acima de 30 dias | +15 |
| Esta na 3a vistoria | +20 |
| Esta na 2a vistoria | +10 |

Essa pontuacao nao substitui a regra legal. Ela serve para ordenar a fila operacional.

---

## Volume de Dados e Performance

O app pode armazenar muitos registros em memoria, mas nao deve renderizar todos de uma vez.

Diretrizes:

1. `matriculas[]` pode conter a carteira completa.
2. A tela deve renderizar apenas a pagina atual.
3. Usar paginacao de 50, 100 ou 200 matriculas.
4. Filtros devem ser aplicados antes da renderizacao.
5. Estatisticas devem usar agregacao em memoria, sem criar milhares de elementos DOM.
6. Importacoes grandes devem mostrar progresso e evitar travar a interface quando possivel.

Meta tecnica:

- 1.000 matriculas: deve funcionar confortavelmente;
- 10.000 matriculas: deve funcionar com paginacao e filtros;
- 100.000 matriculas: exige cuidado especial, processamento em lotes e renderizacao virtual/paginada.

---

## Colaboracao Sem Servidor

Como o app e local, duas pessoas nao editam o mesmo arquivo em tempo real como no Google Planilhas. A solucao viavel e trabalhar com arquivos JSON independentes e mesclagem inteligente.

Fluxo recomendado:

1. Cada pessoa abre uma copia do app.
2. Cada pessoa importa o arquivo-base mais recente da carteira.
3. Cada pessoa trabalha em um conjunto de matriculas.
4. Cada pessoa exporta seu JSON atualizado.
5. Um usuario importa/mescla os JSONs.
6. O app combina registros iguais, adiciona novos e aponta conflitos.
7. O arquivo consolidado volta para o Google Drive.

---

## Modelo de Mesclagem

Cada matricula deve ter uma chave primaria:

```text
matricula.numero
```

Cada servico deve idealmente ter um identificador interno estavel:

```text
servico.id = codigo + dataCriacao + origemImportacao + sequencial
```

Enquanto nao houver `servico.id`, a chave provisoria pode ser:

```text
numeroMatricula + codigo + dataCriacao
```

Regras sugeridas:

### Matricula existe apenas no arquivo importado

Adicionar matricula inteira.

### Matricula existe nos dois arquivos

Mesclar servicos.

### Servico existe apenas no arquivo importado

Adicionar servico.

### Mesmo servico existe nos dois arquivos

Comparar campos.

Se o arquivo importado tiver informacao mais completa, atualizar:

- `dataBaixa` preenchida substitui `dataBaixa` vazia;
- observacao mais recente pode substituir observacao antiga;
- campos novos podem ser incorporados.

### Conflito

Gerar lista de conflitos quando:

- a mesma matricula e o mesmo servico possuem datas diferentes;
- dois usuarios preencheram baixas diferentes;
- houve alteracao manual divergente no mesmo campo.

O app deve permitir escolher:

- manter atual;
- usar importado;
- duplicar como novo servico;
- resolver manualmente.

---

## Metadados Necessarios para Mesclagem

Adicionar futuramente ao JSON:

```json
{
  "versao": "2.0",
  "arquivoId": "vto-2026-07-14-rafa",
  "geradoEm": "2026-07-14T10:00:00",
  "autor": "Rafa",
  "matriculas": []
}
```

Em cada matricula:

```json
{
  "numero": "10045225",
  "criadoEm": "2026-07-14T10:00:00",
  "atualizadoEm": "2026-07-14T11:30:00",
  "atualizadoPor": "Rafa",
  "servicos": []
}
```

Em cada servico:

```json
{
  "id": "10045225-8405-2026-02-28-001",
  "codigo": "8405",
  "dataCriacao": "2026-02-28",
  "dataBaixa": "2026-03-20",
  "criadoEm": "2026-07-14T10:00:00",
  "atualizadoEm": "2026-07-14T11:30:00",
  "atualizadoPor": "Rafa"
}
```

---

## Funcionalidades Futuras Prioritarias

### Fase A - Fundacao da Carteira

- Criar filtros na aba Matriculas.
- Criar paginacao.
- Ordenar por risco.
- Criar calculo de prioridade operacional.
- Separar dado permanente de estado calculado.

### Fase B - Radar VTO

- Criar aba de visualizacao coletiva.
- Criar cards de risco.
- Criar tabela priorizada.
- Criar radar 0-180 dias agregado.
- Criar filtro de servicos abertos acima de 30 dias.

### Fase C - Timeline Individual 0-180

- Trocar escala hibrida por regua fixa 0-180.
- Manter blocos 0-60, 60-120, 120-180.
- Mostrar "dia X de 180".
- Mostrar eventos fora do prazo em area excedida.

### Fase D - Colaboracao Offline

- Adicionar metadados no JSON.
- Criar importacao "Mesclar Arquivo".
- Criar relatorio de mesclagem.
- Criar tela de conflitos.
- Exportar arquivo consolidado.

### Fase E - Robustez

- Melhorar importacao de CSV grande.
- Criar processamento em lotes.
- Adicionar validacoes de datas.
- Criar backup antes de mesclagens complexas.

---

## Decisao Arquitetural Recomendada

O VTO Segundo Cerebro deve continuar local e monobloco, mas passar a funcionar como um sistema de arquivos versionados simples:

- JSON e o banco portatil;
- Google Drive e a pasta compartilhada;
- mesclagem e o mecanismo de colaboracao;
- filtros e radar sao o cockpit diario;
- timeline individual e a explicacao detalhada de cada caso.

Essa abordagem evita servidor, respeita a regra de transferencia e ainda permite trabalho em equipe com controle suficiente para o contexto operacional.

