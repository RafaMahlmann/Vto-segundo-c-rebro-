#!/usr/bin/env python3
"""Teste rapido: abre o VTO no navegador e tira screenshot do header."""
import sys, os, subprocess

# Ativa o venv
os.environ['PATH'] = r'C:\Users\xrafa\Programas\vto-repo\venv_agente\Scripts;' + os.environ.get('PATH', '')

from playwright.sync_api import sync_playwright

PAGE_URL = r'file:///C:\Users\xrafa\Programas\vto-repo\index.html'

try:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={'width': 1400, 'height': 900})
        page.goto(PAGE_URL)
        page.wait_for_load_state('networkidle')
        page.wait_for_timeout(1000)
        
        # Screenshot do header
        page.screenshot(path=r'C:\Users\xrafa\Programas\vto-repo\agente_screenshots\teste_zip_header.png')
        print('Screenshot salvo: teste_zip_header.png')
        
        # Clica no botao ZIP e espera
        btn = page.locator('button.btn-zip')
        if btn.is_visible():
            print('Botao ZIP visivel!')
            btn.click()
            page.wait_for_timeout(2000)
            page.screenshot(path=r'C:\Users\xrafa\Programas\vto-repo\agente_screenshots\teste_zip_click.png')
            print('Screenshot apos click salvo: teste_zip_click.png')
        else:
            print('Botao ZIP NAO visivel!')
        
        browser.close()
        print('Teste finalizado com sucesso.')
except Exception as e:
    print('Erro:', e)
    sys.exit(1)
