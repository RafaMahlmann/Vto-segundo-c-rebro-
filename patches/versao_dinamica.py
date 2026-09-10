with open('index.html', 'r', encoding='utf-8') as f:
    s = f.read()

# 1. Adiciona data-versao no badge do header
s = s.replace(
    '<span class="versao-badge" id="versaoBadge">v3.7</span>',
    '<span class="versao-badge" id="versaoBadge" data-versao>v3.7</span>'
)

# 2. Adiciona data-versao nos footers
s = s.replace(
    '<div class="footer" style="text-align:center;margin-top:14px;font-size:.75rem;color:#adb5bd">v3.7</div>',
    '<div class="footer" style="text-align:center;margin-top:14px;font-size:.75rem;color:#adb5bd" data-versao>v3.7</div>'
)

s = s.replace(
    '<div class="footer">v3.7</div>',
    '<div class="footer" data-versao>v3.7</div>'
)

# 3. Adiciona script de versao dinamica antes do fechamento do </body> ou no inicio do script
# Vou colocar logo apos a abertura do <script> principal
old_script = '<script>'
new_script = '''<script>
// ===== VERSAO DINAMICA =====
(function() {
    const agora = new Date();
    const pad = n => String(n).padStart(2, '0');
    const dataHora = agora.getFullYear() + '-' + pad(agora.getMonth()+1) + '-' + pad(agora.getDate()) + '.' + pad(agora.getHours()) + '-' + pad(agora.getMinutes());
    const versao = 'v3.7.' + dataHora;
    document.querySelectorAll('[data-versao]').forEach(el => { el.textContent = versao; });
})();
'''

s = s.replace(old_script, new_script, 1)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(s)

print('Versao dinamica implementada.')
