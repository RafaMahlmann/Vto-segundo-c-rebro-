import re

with open(r'C:\Users\xrafa\Programas\vto-repo\index.html', encoding='utf-8') as f:
    t = f.read()

script_match = re.search(r'<script>(.*?)</script>', t, re.DOTALL)
if script_match:
    js = script_match.group(1)
    open_braces = js.count('{')
    close_braces = js.count('}')
    print(f'Chaves JS: abertas={open_braces}, fechadas={close_braces}, balanceado={open_braces==close_braces}')
    
    open_parens = js.count('(')
    close_parens = js.count(')')
    print(f'Parenteses: abertos={open_parens}, fechados={close_parens}, balanceado={open_parens==close_parens}')
    
    open_brackets = js.count('[')
    close_brackets = js.count(']')
    print(f'Colchetes: abertos={open_brackets}, fechados={close_brackets}, balanceado={open_brackets==close_brackets}')
else:
    print('Script nao encontrado!')
