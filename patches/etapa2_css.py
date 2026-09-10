with open('index.html', 'r', encoding='utf-8') as f:
    s = f.read()

# Adiciona CSS para card laranja e mini-abas
old_css = '.resposta-gerada-texto{width:100%;min-height:220px;padding:14px;font-size:.88rem;line-height:1.6;color:#343a40;border:none;outline:none;resize:vertical;font-family:inherit;background:white}'

new_css = '''.resposta-gerada-texto{width:100%;min-height:220px;padding:14px;font-size:.88rem;line-height:1.6;color:#343a40;border:none;outline:none;resize:vertical;font-family:inherit;background:white}
/* ===== CARD RESPOSTA COM ABAS M1/M2 ===== */
.card-resposta{margin-top:18px;border:1px solid #ffd699;border-radius:10px;overflow:hidden;background:#fff8e6}
.card-resposta-header{display:flex;justify-content:space-between;align-items:center;padding:10px 14px;background:#ffeeba;border-bottom:1px solid #ffd699}
.card-resposta-titulo{font-size:.9rem;font-weight:700;color:#856404}
.mini-tabs{display:flex;gap:4px}
.mini-tab{padding:5px 12px;font-size:.78rem;font-weight:600;border:2px solid #ffd699;border-radius:6px;background:transparent;color:#856404;cursor:pointer;transition:all .2s;font-family:inherit}
.mini-tab:hover{background:rgba(255,255,255,.5)}
.mini-tab.ativa{background:white;border-color:#856404;color:#856404}
.card-resposta-body{padding:14px}
.modelo-resposta{display:none}
.modelo-resposta.ativa{display:block}
.card-resposta-body textarea{width:100%;min-height:180px;padding:12px;font-size:.88rem;line-height:1.6;color:#343a40;border:1px solid #ffd699;border-radius:6px;outline:none;resize:vertical;font-family:inherit;background:white}'''

s = s.replace(old_css, new_css)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(s)

print('Etapa 2 (CSS card laranja e mini-abas) concluida.')
