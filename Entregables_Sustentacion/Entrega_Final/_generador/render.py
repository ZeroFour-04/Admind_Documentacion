import sys, fitz, pathlib
pdf, salida = sys.argv[1], pathlib.Path(sys.argv[2])
dpi = int(sys.argv[3]) if len(sys.argv) > 3 else 70
salida.mkdir(parents=True, exist_ok=True)
for viejo in salida.glob("p*.png"):
    viejo.unlink()
doc = fitz.open(pdf)
print("paginas:", len(doc))
for i, pagina in enumerate(doc, 1):
    pagina.get_pixmap(dpi=dpi).save(salida / f"p{i:02d}.png")
