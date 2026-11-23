# -*- coding: utf-8 -*-
"""Arma el Manual Técnico por partes: python build.py <hasta_parte> <salida.docx>"""
import importlib
import sys

from ooxml import Doc

LOGO = "C:/Users/Alejandro/Documents/A D M I N D/Frontend/Admind_Front-End/static/img/logo-marca.png"
PARTES = ["parte1", "parte2", "parte3", "parte4", "parte5"]


def main():
    hasta = int(sys.argv[1])
    salida = sys.argv[2]
    with open(LOGO, "rb") as f:
        logo = f.read()
    d = Doc(
        titulo="AdMind — Manual Técnico",
        autor="Equipo AdMind",
        nombre_encabezado="Manual Técnico de AdMind",
        logo_png=logo,
    )
    for nombre in PARTES[:hasta]:
        try:
            modulo = importlib.import_module(nombre)
        except ModuleNotFoundError as error:
            if error.name == nombre:
                break
            raise
        modulo.construir(d)
    # Hasta la parte 4 todo es una sola sección (con portada); la parte 5 agrega las demás.
    d.guardar(salida, ultima_portada=(hasta < 5))
    print("guardado:", salida)


if __name__ == "__main__":
    main()
