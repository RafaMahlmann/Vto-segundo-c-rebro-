# Plano de Implementação — Calculadora de Dilação (VTO v3.7)

## Contexto do Projeto
O projeto é um único arquivo HTML monolito (`index.html`, ~2.328 linhas) com CSS e JavaScript embutidos. A **Calculadora de Dilação** está na aba `dilacao` (linhas ~361–398 do HTML, função `calcularDilacao()` nas linhas ~968–984 do JS).

---

## 1. O que será REMOVIDO

### ❌ Select "Tipo de Dias" (corridos / úteis)
- **Motivo:** A dilação é **sempre** em dias corridos. A opção de dias úteis foi uma invenção da IA e não reflete o procedimento real.
- **Impacto:** Remove o `<select id="tipoDiasDilacao">` do HTML e toda a lógica condicional `if (tipoDias === 'uteis')` do JavaScript. Simplifica o código.

---

## 2. O que será MODIFICADO

### 🔧 Dias de Dilação: de select fixo → botões rápidos + input manual
- **Atual:** `<select>` com apenas 30, 60, 90.
- **Novo:** Botões rápidos clicáveis (30, 60, 90) + campo numérico livre para digitar qualquer valor (ex: 365).
- **Comportamento:**
  - Clicar em um botão preenche o input com aquele valor.
  - O usuário pode também digitar diretamente no input.
  - O input aceita apenas números inteiros positivos.

### 🔧 Resultado da dilação simples
- Continua calculando a data final somando os dias corridos à data base.
- Remove a badge de "DIAS ÚTEIS", mantendo apenas "DIAS CORRIDOS" (implícito).

---

## 3. O que será ADICIONADO — Nova Seção "Casos Especiais / Data Base Extra"

Esta é a principal evolução. Ela permite calcular a **dilação parcial** quando o cliente já pediu uma dilação há algum tempo e agora está pedindo mais.

### 📋 Campos novos:

| Campo | Tipo | Descrição |
|-------|------|-----------|
| **Data do Pedido Original** | `date` (DD/MM/AAAA) | Data em que o cliente entregou o pedido de dilação |
| **Dias Totais Solicitados** | `number` | Quanto ele pediu naquela época (ex: 365) |
| **Dias a Conceder Agora** | `number` (padrão: 90) | Como é a primeira vez analisando, o procedimento padrão é conceder 90 dias hoje |

### 📊 Resultados calculados automaticamente:

| Resultado | Cálculo |
|-----------|---------|
| **Dias decorridos** | De "Data do Pedido Original" até **hoje** |
| **Dias restantes do pedido original** | `Dias Totais - Dias Decorridos` |
| **Dias que ainda faltarão pedir depois dos 90 dias** | `Dias Restantes - 90` (se positivo; senão 0) |
| **Data de vencimento dos 90 dias** | Hoje + 90 dias corridos |
| **Nova data base do próximo pedido** | Data de vencimento dos 90 dias |

### 📐 Exemplo prático (do seu caso):

- Data do pedido original: **13/03/2026**
- Dias solicitados: **365**
- Hoje: **18/08/2026**
- Dias decorridos: **158 dias**
- Dias restantes do original: **365 − 158 = 207 dias**
- Concedendo 90 dias hoje → Faltam pedir depois: **207 − 90 = 117 dias**
- Vencimento dos 90 dias: **18/08/2026 + 90 = 16/11/2026**

---

## 4. Texto da Nova Dica (azul)

Substituir a dica atual por:

> **Como usar:**
> 1. **Dilação simples:** Escolha a data base, informe os dias de dilação (use os botões 30/60/90 ou digite um valor manual) e clique em calcular.
> 2. **Casos especiais (dilação parcial):** Use quando o cliente já pediu uma dilação há algum tempo e agora você vai conceder um prazo adicional. Preencha a *data do pedido original* e os *dias totais* que ele solicitou. A ferramenta calcula automaticamente quantos dias já se passaram, quantos faltam, e quanto você deve conceder agora (padrão: 90 dias). Ela também mostra a data de vencimento desses 90 dias e quanto ainda faltará pedir depois.

---

## 5. Resumo das Mudanças no Código

| Arquivo | Área | Tipo de mudança |
|---------|------|-----------------|
| `index.html` | HTML da aba `dilacao` | Remover select de tipo de dias; trocar select de quantidade por botões + input; adicionar nova seção "Caso Especial" |
| `index.html` | CSS embutido | Adicionar estilos para os botões rápidos e para o layout da nova seção |
| `index.html` | JS `calcularDilacao()` | Simplificar (sempre corridos); adaptar para ler do novo input |
| `index.html` | JS novo | Criar `calcularDilacaoCasoEspecial()` com toda a lógica descrita acima |

---

## 6. Estimativa

- **Complexidade:** Média (alterações localizadas em uma única aba, mas com lógica nova de datas)
- **Risco:** Baixo (não afeta as outras abas: Prazo, Fluxo, Matrículas, Timeline)
- **Tempo estimado:** ~1 sessão de implementação + testes

---

## 7. Próximo Passo

Se aprovado, posso iniciar a implementação imediatamente no arquivo `index.html`.
