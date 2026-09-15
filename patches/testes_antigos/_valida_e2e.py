
import zipfile, sys
z = zipfile.ZipFile(r"C:\Users\xrafa\Programas\vto-repo\_teste_e2e.zip")
bad = z.testzip()
print("testzip:", bad)
print("arquivos:", z.namelist())
for n in z.namelist():
    data = z.read(n)
    print(n, "->", len(data), "bytes")
sys.exit(1 if bad else 0)
