#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de release do VTO.
Atualiza o numero de versao em todos os arquivos e faz commit + push.

Uso:
    python patches/release.py 3.8
"""
import sys
import re
import subprocess
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parent.parent

def ler_versao_atual():
    version_json = BASE_DIR / 'version.json'
    if version_json.exists():
        m = re.search(r'"versao":\s*"([0-9.]+)"', version_json.read_text(encoding='utf-8'))
        if m:
            return m.group(1)
    return None

def atualizar_index_html(nova_versao):
    path = BASE_DIR / 'index.html'
    t = path.read_text(encoding='utf-8')

    # Atualiza <title>
    t = re.sub(r'<title>VTO v[0-9.]+', f'<title>VTO v{nova_versao}', t)
    # Atualiza badge estatico (fallback)
    t = re.sub(r'<span class="versao-badge" id="versaoBadge" data-versao>v[0-9.]+</span>',
               f'<span class="versao-badge" id="versaoBadge" data-versao>v{nova_versao}</span>', t)
    # Atualiza footers com data-versao
    t = re.sub(r'data-versao>v[0-9.]+</div>', f'data-versao>v{nova_versao}</div>', t)
    # Atualiza VERSAO_LOCAL
    t = re.sub(r"const VERSAO_LOCAL = '[0-9.]+';", f"const VERSAO_LOCAL = '{nova_versao}';", t)
    # Atualiza versao dinamica
    t = re.sub(r"const versao = 'v[0-9.]+\.' \+ dataHora;", f"const versao = 'v{nova_versao}.' + dataHora;", t)
    # Atualiza footer da timeline
    t = re.sub(r'<div class="footer">v[0-9.]+ - Timeline Proporcional</div>',
               f'<div class="footer">v{nova_versao} - Timeline Proporcional</div>', t)

    path.write_text(t, encoding='utf-8')
    print(f'  index.html atualizado para v{nova_versao}')

def atualizar_version_json(nova_versao):
    path = BASE_DIR / 'version.json'
    t = path.read_text(encoding='utf-8')
    t = re.sub(r'"versao":\s*"[0-9.]+"', f'"versao": "{nova_versao}"', t)
    path.write_text(t, encoding='utf-8')
    print(f'  version.json atualizado para v{nova_versao}')

def atualizar_readme(nova_versao):
    path = BASE_DIR / 'README.md'
    if not path.exists():
        return
    t = path.read_text(encoding='utf-8')
    # Versao atual
    t = re.sub(r'\*\*Versao Atual:\*\* [0-9.]+', f'**Versao Atual:** {nova_versao}', t)
    # Versao no final
    t = re.sub(r'Versao do aplicativo: [0-9.]+', f'Versao do aplicativo: {nova_versao}', t)
    # Remocao na vX.Y
    t = re.sub(r'removido na v[0-9.]+', f'removido na v{nova_versao}', t)
    path.write_text(t, encoding='utf-8')
    print(f'  README.md atualizado para v{nova_versao}')

def atualizar_timeline(nova_versao):
    path = BASE_DIR / 'TIMELINE.md'
    if not path.exists():
        return
    t = path.read_text(encoding='utf-8')
    t = re.sub(r'\*\*Versao atual do app:\*\* [0-9.]+', f'**Versao atual do app:** {nova_versao}', t)
    t = re.sub(r'Estado: Projeto operacional em v[0-9.]+', f'Estado: Projeto operacional em v{nova_versao}', t)
    path.write_text(t, encoding='utf-8')
    print(f'  TIMELINE.md atualizado para v{nova_versao}')

def fazer_commit_push(nova_versao, mensagem=None):
    if mensagem is None:
        mensagem = f'release: bump versao para v{nova_versao}'
    subprocess.run(['git', 'add', 'index.html', 'version.json', 'README.md', 'TIMELINE.md'], cwd=BASE_DIR, check=True)
    subprocess.run(['git', 'commit', '-m', mensagem], cwd=BASE_DIR, check=True)
    subprocess.run(['git', 'push', 'origin', 'main'], cwd=BASE_DIR, check=True)
    print(f'  Commit e push feitos: {mensagem}')

def main():
    if len(sys.argv) < 2:
        atual = ler_versao_atual()
        print(f'Versao atual: v{atual}')
        print(f'Uso: python patches/release.py <nova_versao>')
        sys.exit(1)

    nova_versao = sys.argv[1]
    atual = ler_versao_atual()

    print(f'Atualizando v{atual} -> v{nova_versao}...')
    atualizar_index_html(nova_versao)
    atualizar_version_json(nova_versao)
    atualizar_readme(nova_versao)
    atualizar_timeline(nova_versao)

    mensagem = sys.argv[2] if len(sys.argv) > 2 else f'release: bump versao para v{nova_versao}'
    fazer_commit_push(nova_versao, mensagem)
    print(f'Release v{nova_versao} concluido!')

if __name__ == '__main__':
    main()
