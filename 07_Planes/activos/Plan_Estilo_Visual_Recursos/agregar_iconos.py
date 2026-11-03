"""Pone un ícono delante del texto de cada enlace del lateral.

Uso, desde la raíz de Admind_Front-End:
    ./.venv/Scripts/python.exe "<ruta de este archivo>" templates/componentes/lateral.html templates/componentes/_enlaces_gestion.html

Qué hace: para cada <a class="am-lateral__item ..."> toma el espacio de nombres de su {% url 'ns:nombre' %},
busca su ícono en ICONOS y lo escribe justo después del «>» de apertura, antes del texto. El texto queda
pegado a </a>, que es lo que miran las pruebas (">Pagos</a>"). El enlace «Cambiar de conjunto» del pie no
lleva ícono (una prueba exige su forma exacta). Se puede correr más de una vez: lo que ya tiene ícono no se toca.
Si encuentra un espacio de nombres que no conoce, se detiene y lo dice: no adivina un ícono.
"""
import re
import sys
from pathlib import Path

ICONOS = {
    "paneles": "i-inicio",
    "reservas": "i-calendario",
    "areas": "i-area",
    "reglas": "i-reglas",
    "anuncios": "i-anuncio",
    "documentos": "i-documento",
    "notificaciones": "i-campana",
    "triage": "i-bandeja",
    "casos": "i-maletin",
    "infracciones": "i-alerta",
    "ingresos": "i-puerta",
    "pagos": "i-tarjeta",
    "parqueaderos": "i-carro",
    "visitantes": "i-visitantes",
    "conjuntos": "i-edificio",
    "usuarios": "i-usuarios",
    "unidades": "i-unidades",
}
SIN_ICONO = {"conjuntos:selector"}  # «Cambiar de conjunto», en el pie del lateral

ENLACE = re.compile(r'(<a class="am-lateral__item[^>]*>)(?!<svg)([^<]+)(</a>)')
URL = re.compile(r"\{% url '(\w+):([\w-]+)'")


def con_iconos(texto, ruta):
    puestos = 0

    def poner(coincidencia):
        nonlocal puestos
        apertura, contenido, cierre = coincidencia.groups()
        url = URL.search(apertura)
        if url is None:
            raise SystemExit(f"{ruta}: un enlace del lateral sin {{% url %}}: {apertura}")
        espacio, nombre = url.groups()
        if f"{espacio}:{nombre}" in SIN_ICONO:
            return coincidencia.group(0)
        if espacio not in ICONOS:
            raise SystemExit(f"{ruta}: no hay ícono para el espacio de nombres «{espacio}». Agrégalo a ICONOS y a _iconos.html.")
        puestos += 1
        icono = f'<svg class="am-icono" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><use href="#{ICONOS[espacio]}"></use></svg>'
        return f"{apertura}{icono}{contenido}{cierre}"

    return ENLACE.sub(poner, texto), puestos


def main(rutas):
    if not rutas:
        raise SystemExit("Falta la ruta de al menos un archivo.")
    for ruta in map(Path, rutas):
        original = ruta.read_text(encoding="utf-8")
        nuevo, puestos = con_iconos(original, ruta)
        if nuevo != original:
            ruta.write_text(nuevo, encoding="utf-8", newline="")
        print(f"{ruta}: {puestos} iconos puestos")


if __name__ == "__main__":
    main(sys.argv[1:])
