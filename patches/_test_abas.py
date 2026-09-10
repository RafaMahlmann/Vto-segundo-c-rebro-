#!/usr/bin/env python3
"""Teste rapido de todas as abas apos adicionar botao ZIP."""
import os
os.environ['PATH'] = r'C:\Users\xrafa\Programas\vto-repo\venv_agente\Scripts;' + os.environ.get('PATH', '')

from playwright.sync_api import sync_playwright

PAGE_URL = r'file:///C:\Users\xrafa\Programas\vto-repo\index.html'
ABAS = ['prazo', 'dilacao', 'fluxo', 'matriculas', 'estatisticas']

try:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={'width': 1400, 'height': 900})
        page.goto(PAGE_URL)
        page.wait_for_load_state('networkidle')
        page.wait_for_timeout(1000)
        
        for aba in ABAS:
            btn_text = {
                'prazo': 'Calculadora de Prazo',
                'dilacao': 'Calculadora de Dilacao',
                'fluxo': 'Fluxo de Vistorias',
                'matriculas': 'Matriculas',
                'estatisticas': 'Estatisticas'
            }[aba]
            page.click(f'text={btn_text}')
            page.wait_for_timeout(500)
            is_active = page.evaluate(f"() => document.getElementById('aba-{aba}').classList.contains('active')")
            print(f'Aba {aba}: ativa={is_active}')
            page.screenshot(path=rf'C:\Users\xrafa\Programas\vto-repo\agente_screenshots\teste_aba_{aba}.png')
        
        # Testa Ctrl+Z (undo)
        page.click("text=Matriculas")
        page.wait_for_timeout(300)
        # Adiciona uma matricula
        page.fill('#novaMatricula', '99999999')
        page.click('text=Adicionar')
        page.wait_for_timeout(300)
        count_antes = page.evaluate('() => matriculas.length')
        print(f'Matriculas antes do undo: {count_antes}')
        
        page.keyboard.press('Control+z')
        page.wait_for_timeout(300)
        count_depois = page.evaluate('() => matriculas.length')
        print(f'Matriculas apos Ctrl+Z: {count_depois}')
        print(f'Undo funcionou: {count_depois < count_antes}')
        
        browser.close()
        print('Teste de abas finalizado.')
except Exception as e:
    print('Erro:', e)
    import traceback
    traceback.print_exc()
