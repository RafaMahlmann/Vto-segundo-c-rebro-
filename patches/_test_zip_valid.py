#!/usr/bin/env python3
"""Testa se o ZIP gerado pelo JS e valido."""
import os, struct, zipfile, io

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
        
        # Executa a funcao JS e retorna o ZIP como array de bytes base64
        zip_b64 = page.evaluate("""() => {
            const html = '<!DOCTYPE html>\\n<html><head><title>Teste</title></head><body>Hello</body></html>';
            const zip = criarZipStored('index.html', html);
            // Converte para base64
            let binary = '';
            const len = zip.byteLength;
            for (let i = 0; i < len; i++) {
                binary += String.fromCharCode(zip[i]);
            }
            return btoa(binary);
        }""")
        
        # Decodifica e valida
        import base64
        zip_bytes = base64.b64decode(zip_b64)
        print(f'ZIP gerado: {len(zip_bytes)} bytes')
        
        # Tenta abrir como zip
        z = zipfile.ZipFile(io.BytesIO(zip_bytes))
        print('Arquivos no ZIP:', z.namelist())
        
        # Extrai e verifica conteudo
        content = z.read('index.html').decode('utf-8')
        print(f'Conteudo extraido: {len(content)} chars')
        print('Contem <!DOCTYPE html>:', '<!DOCTYPE html>' in content)
        print('ZIP valido:', 'SIM')
        
        browser.close()
except Exception as e:
    print('Erro:', e)
    import traceback
    traceback.print_exc()
