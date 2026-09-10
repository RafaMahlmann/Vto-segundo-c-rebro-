import http.server, socketserver, threading, time, subprocess, sys, os

os.chdir(r'C:\Users\xrafa\Programas\vto-repo')
handler = http.server.SimpleHTTPRequestHandler
httpd = socketserver.TCPServer(('', 8765), handler)
t = threading.Thread(target=httpd.serve_forever)
t.daemon = True
t.start()
print('Servidor iniciado em http://localhost:8765/')
time.sleep(1)

# Abre o navegador
subprocess.Popen([r'C:\Program Files\Google\Chrome\Application\chrome.exe', 'http://localhost:8765/index.html'])
print('Navegador aberto. Aguardando 5 segundos...')
time.sleep(5)
httpd.shutdown()
print('Servidor encerrado.')
