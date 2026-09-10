#!/usr/bin/env python3
"""Testa o banner de nova versao."""
import os
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
        
        # Screenshot normal
        page.screenshot(path=r'C:\Users\xrafa\Programas\vto-repo\agente_screenshots\teste_banner_normal.png')
        
        # Ativa banner manualmente via DOM
        page.evaluate('''() => {
            const banner = document.getElementById('bannerVersao');
            document.getElementById('bannerVersaoTexto').textContent = 'Nova versao v9.9 disponivel! Baixe e substitua seu arquivo.';
            const btn = document.getElementById('bannerBtnBaixar');
            if (btn) { btn.textContent = 'Baixar v9.9'; btn.style.display = 'inline-block'; }
            banner.classList.add('ativo');
        }''')
        page.wait_for_timeout(500)
        page.screenshot(path=r'C:\Users\xrafa\Programas\vto-repo\agente_screenshots\teste_banner_ativo.png')
        
        browser.close()
        print('Screenshots salvos!')
except Exception as e:
    print('Erro:', e)
    import traceback
    traceback.print_exc()
