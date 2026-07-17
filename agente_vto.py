#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Agente de teste para o fluxo de vistorias VTO.

Este agente:
1. Le as regras dos documentos MD (docs/)
2. Gera casos de teste realistas de matriculas e servicos
3. Abre o navegador e preenche o fluxo de vistorias VTO automaticamente
4. Tira screenshots e gera um relatorio simples

Uso:
    source venv_agente/Scripts/activate
    python agente_vto.py
"""

import os
import re
import random
import datetime
from pathlib import Path
from playwright.sync_api import sync_playwright, expect

# ============================================================
# CONFIGURACOES
# ============================================================
BASE_DIR = Path(__file__).resolve().parent
PAGE_URL = BASE_DIR / "index.html"
SCREENSHOTS_DIR = BASE_DIR / "agente_screenshots"
SCREENSHOTS_DIR.mkdir(exist_ok=True)

# Cenarios possiveis para o agente escolher
CENARIOS = [
    "regular",
    "irregular_com_sancao",
    "irregular_com_dilacao",
    "convenio",
    "habite_se",
    "obras",
]

# Mapa de servicos disponiveis em cada coluna do fluxo
SERVICOS_POR_COLUNA = {
    1: {
        "servicos": ["8403", "8421", "8563"],
        "intermediarios": ["8402", "8400", "8407", "8409", "8419", "8425"],
        "habite_se": ["8470", "8480", "8485"],
    },
    2: {
        "servicos": ["8405", "8416", "8574"],
        "intermediarios": ["8403", "8421", "8402", "8400", "8407", "8409", "8419", "8425"],
        "dilacao": ["8432", "8433", "8434"],
        "habite_se": ["8470", "8480", "8485"],
    },
    3: {
        "servicos": ["8428", "8417"],
        "intermediarios": ["8403", "8421", "8402", "8400", "8407", "8409", "8419", "8425"],
        "dilacao": ["8432", "8433", "8434"],
        "habite_se": ["8470", "8480", "8485"],
    },
}

NOMES_SERVICO = {
    "8403": "1a Vistoria + AS",
    "8421": "1a Vistoria",
    "8563": "1a Vistoria Obras",
    "8405": "2a Vistoria",
    "8416": "2a Vistoria Convenio",
    "8574": "2a Vistoria Obras",
    "8428": "3a Vistoria",
    "8417": "Autuacao Municipal",
    "8402": "Rec. Tarifaria",
    "8400": "Solic. Cliente",
    "8407": "Topografia",
    "8409": "Orient. Tecnica",
    "8419": "Carta Anuencia",
    "8425": "Vistoria Refluxo",
    "8432": "Dilacao 30 dias",
    "8433": "Dilacao 60 dias",
    "8434": "Dilacao 90 dias",
    "8470": "Habite-se +600",
    "8480": "Habite-se -600",
    "8485": "Habite-se Social",
}


# ============================================================
# FUNCOES AUXILIARES
# ============================================================
def gerar_matricula():
    """Gera um numero de matricula aleatorio de 8 digitos."""
    return "".join(random.choices("0123456789", k=8))


def ler_regras_docs():
    """Extrai trechos relevantes dos arquivos MD para contexto."""
    regras = []
    arquivos = [
        "05-instrucao-tecnica-vto-completo.md",
        "03-codigos-resultados-vto.md",
        "04-objetivos-definicoes-vto.md",
    ]
    for nome in arquivos:
        caminho = BASE_DIR / "docs" / nome
        if caminho.exists():
            texto = caminho.read_text(encoding="utf-8")
            # Pega secoes sobre prazos, ciclo e codigos de servico
            for secao in ["## 2.1 Entrada das demandas", "## 3.1 Ciclo das Vistorias", "## 4.1 Metodologia"]:
                idx = texto.find(secao)
                if idx >= 0:
                    fim = texto.find("\n## ", idx + 1)
                    trecho = texto[idx:fim if fim > 0 else idx + 1500]
                    regras.append(f"--- {nome} ---\n{trecho[:1500]}")
    return "\n\n".join(regras)


def datas_para_cenario(cenario):
    """Gera datas coerentes para o cenario escolhido."""
    hoje = datetime.date.today()
    datas = {"base": hoje.strftime("%Y-%m-%d")}

    if cenario == "regular":
        # Uma unica vistoria recente
        datas[1] = (hoje - datetime.timedelta(days=random.randint(5, 30))).strftime("%Y-%m-%d")
    elif cenario == "obras":
        datas[1] = (hoje - datetime.timedelta(days=random.randint(40, 70))).strftime("%Y-%m-%d")
        datas[2] = (hoje - datetime.timedelta(days=random.randint(5, 30))).strftime("%Y-%m-%d")
    elif cenario in ("irregular_com_sancao", "convenio"):
        datas[1] = (hoje - datetime.timedelta(days=130)).strftime("%Y-%m-%d")
        datas[2] = (hoje - datetime.timedelta(days=65)).strftime("%Y-%m-%d")
        datas[3] = (hoje - datetime.timedelta(days=5)).strftime("%Y-%m-%d")
    elif cenario == "irregular_com_dilacao":
        datas[1] = (hoje - datetime.timedelta(days=150)).strftime("%Y-%m-%d")
        datas[2] = (hoje - datetime.timedelta(days=80)).strftime("%Y-%m-%d")
        datas["dilacao"] = (hoje - datetime.timedelta(days=70)).strftime("%Y-%m-%d")
    elif cenario == "habite_se":
        datas[1] = (hoje - datetime.timedelta(days=random.randint(10, 40))).strftime("%Y-%m-%d")

    return datas


def montar_caso():
    """Monta um caso de teste completo com matricula e sequencia de servicos."""
    cenario = random.choice(CENARIOS)
    matricula = gerar_matricula()
    datas = datas_para_cenario(cenario)
    servicos = []

    if cenario == "regular":
        cod = random.choice(["8403", "8421"])
        servicos.append({"coluna": 1, "codigo": cod, "data": datas[1]})

    elif cenario == "obras":
        servicos.append({"coluna": 1, "codigo": "8563", "data": datas[1]})
        servicos.append({"coluna": 2, "codigo": "8574", "data": datas[2]})

    elif cenario == "irregular_com_sancao":
        servicos.append({"coluna": 1, "codigo": "8403", "data": datas[1]})
        servicos.append({"coluna": 2, "codigo": "8405", "data": datas[2]})
        servicos.append({"coluna": 3, "codigo": "8428", "data": datas[3]})

    elif cenario == "convenio":
        servicos.append({"coluna": 1, "codigo": "8403", "data": datas[1]})
        servicos.append({"coluna": 2, "codigo": "8416", "data": datas[2]})
        servicos.append({"coluna": 3, "codigo": "8417", "data": datas[3]})

    elif cenario == "irregular_com_dilacao":
        servicos.append({"coluna": 1, "codigo": "8403", "data": datas[1]})
        servicos.append({"coluna": 2, "codigo": "8405", "data": datas[2]})
        servicos.append({"coluna": 2, "codigo": "8433", "data": datas["dilacao"]})

    elif cenario == "habite_se":
        servicos.append({"coluna": 1, "codigo": "8403", "data": datas[1]})
        servicos.append({"coluna": 1, "codigo": random.choice(["8470", "8480", "8485"]), "data": datas[1]})

    return {
        "matricula": matricula,
        "cenario": cenario,
        "servicos": servicos,
    }


# ============================================================
# AUTOMACAO COM PLAYWRIGHT
# ============================================================
def preencher_modal(page, data_criacao, data_baixa=None):
    """Preenche o modal de datas que aparece ao clicar em um servico."""
    page.fill("#modalDataCriacao", data_criacao)
    if data_baixa:
        page.fill("#modalDataBaixa", data_baixa)
    # Clica no botao salvar (procura por texto visivel)
    page.click(".modal-btn.salvar")
    # Aguarda o overlay sumir
    page.wait_for_selector("#modalOverlay.ativo", state="hidden", timeout=5000)


def executar_caso(page, caso, idx):
    """Executa um caso de teste no navegador."""
    matricula = caso["matricula"]
    print(f"\n[Caso {idx + 1}] Matricula: {matricula} | Cenario: {caso['cenario']}")

    # Garante que esta na aba Fluxo de Vistorias
    page.click("text=Fluxo de Vistorias VTO")
    page.wait_for_timeout(300)

    # Preenche a matricula no 1o card
    input_matricula = page.locator("#matriculaInputCard1")
    input_matricula.fill(matricula)
    page.wait_for_timeout(500)  # tempo para o JS processar

    # Clica nos servicos do caso
    for s in caso["servicos"]:
        coluna = s["coluna"]
        codigo = s["codigo"]
        data = s["data"]

        # Se necessario, navega ate o card correspondente (no modo carrossel)
        # No modo grade todos estao visiveis, mas garantimos foco
        card = page.locator(f"#coluna{coluna}")
        card.scroll_into_view_if_needed()
        page.wait_for_timeout(200)

        # Clica no botao do servico pelo data-cod via JS (funciona mesmo dentro da roleta)
        encontrado = page.evaluate(
            """(args) => {
                const [coluna, codigo] = args;
                const btn = document.querySelector(`#coluna${coluna} button.servico-btn[data-cod='${codigo}']`);
                if (btn) { btn.click(); return true; }
                return false;
            }""",
            [coluna, codigo],
        )
        if not encontrado:
            print(f"  AVISO: botao {codigo} nao encontrado na coluna {coluna}")
            continue
        page.wait_for_timeout(400)

        # Verifica se o modal abriu
        if page.locator("#modalOverlay.ativo").is_visible():
            # Para servicos de sancao nao abre modal, mas os demais sim
            preencher_modal(page, data, data)
            print(f"  + Servico {codigo} registrado em {data}")
        else:
            print(f"  + Servico {codigo} clicado (sem modal)")

    # Clica em Enviar
    page.locator("#btnEnviarFluxo").click()
    page.wait_for_timeout(300)

    # Trata o confirm do navegador (aceita ir para Matriculas)
    page.on("dialog", lambda dialog: dialog.accept())
    page.wait_for_timeout(500)

    # Screenshot do resultado
    screenshot_path = SCREENSHOTS_DIR / f"caso_{idx + 1}_{caso['cenario']}_{matricula}.png"
    page.screenshot(path=str(screenshot_path), full_page=True)
    print(f"  Screenshot: {screenshot_path.name}")


def main(quantidade=3):
    """Funcao principal do agente."""
    print("=" * 60)
    print("AGENTE DE TESTE - FLUXO DE VISTORIAS VTO")
    print("=" * 60)

    # Le regras (apenas para log/contexto)
    print("\nLendo regras dos documentos MD...")
    regras = ler_regras_docs()
    print(f"Regras carregadas: {len(regras)} caracteres")

    # Gera casos de teste
    print(f"\nGerando {quantidade} casos de teste...")
    casos = [montar_caso() for _ in range(quantidade)]
    for i, c in enumerate(casos, 1):
        print(f"  {i}. {c['cenario']} -> matricula {c['matricula']}")

    # Executa no navegador
    print("\nIniciando navegador...")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=150)
        context = browser.new_context(viewport={"width": 1400, "height": 900})
        page = context.new_page()

        page.goto(f"file:///{PAGE_URL}")
        page.wait_for_load_state("networkidle")
        print(f"Pagina carregada: {PAGE_URL}")

        for i, caso in enumerate(casos):
            executar_caso(page, caso, i)

        # Screenshot final da aba Matriculas
        page.click("text=Matriculas")
        page.wait_for_timeout(500)
        final_path = SCREENSHOTS_DIR / "final_matriculas.png"
        page.screenshot(path=str(final_path), full_page=True)
        print(f"\nScreenshot final da aba Matriculas: {final_path.name}")

        browser.close()

    print("\n" + "=" * 60)
    print("AGENTE FINALIZADO")
    print(f"Screenshots salvos em: {SCREENSHOTS_DIR}")
    print("=" * 60)


if __name__ == "__main__":
    main(quantidade=3)
