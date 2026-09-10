import re, subprocess, os

with open(r'C:\Users\xrafa\Programas\vto-repo\index.html', encoding='utf-8') as f:
    t = f.read()

js = re.search(r'<script>(.*?)</script>', t, re.DOTALL).group(1)

js_path = r'C:\Users\xrafa\Programas\vto-repo\patches\_temp_js.js'
with open(js_path, 'w', encoding='utf-8') as f:
    f.write(js)

node = r'C:\Users\xrafa\AppData\Local\Programs\Kimi\resources\resources\runtime\node'
result = subprocess.run([node, '--check', js_path], capture_output=True, text=True)
print('STDOUT:', result.stdout)
print('STDERR:', result.stderr)
print('Return code:', result.returncode)

os.remove(js_path)
