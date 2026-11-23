# -*- coding: utf-8 -*-
"""Parte 1: portada e índice."""
from ooxml import (
    G500, V50, V600, V700, V900, BLANCO,
    imagen, parrafo, ppr, run,
)

NOMBRES = ["MANUEL ALEJANDRO ALDANA RINCON", "ANDERSON CAMILO REMISO NIÑO"]  # confirmados por Alejo 2026-11-14


def construir(d):
    # --- Portada
    d.add(parrafo(" ", antes=0, despues=0, linea=(240, "exact")))
    # Logo de unos 5 cm, centrado
    d.add(f"<w:p>{ppr(alinear='center', antes=0, despues=360)}"
          f"{imagen('rIdLogo', 1800000, 1800000, 'Logo AdMind', 800, 'Logo de AdMind')}</w:p>")

    banda = parrafo(run(" ", size=8), sombra=V600, antes=0, despues=0, linea=(300, "exact"))
    d.add(banda)
    d.add(parrafo("Manual Técnico", estilo="Title", antes=480, despues=160))
    d.add(parrafo("AdMind — Plataforma de administración de conjuntos residenciales",
                  estilo="Subtitle", despues=480))
    d.add(banda)

    def dato(etiqueta, valor, antes=400):
        valores = valor if isinstance(valor, (list, tuple)) else [valor]
        d.add(parrafo(run(etiqueta.upper(), color=G500, size=19, bold=True), alinear="center", antes=antes,
                      despues=20, linea=(240, "auto"), keep_next=True))
        for v in valores:
            d.add(parrafo(run(v, color=V900, size=28, bold=True), alinear="center", antes=0, despues=0,
                          linea=(260, "auto")))

    dato("Integrantes", NOMBRES, antes=560)
    dato("Asignatura", "Ingeniería de Software II")
    dato("Docente", "Oscar Gómez")
    dato("Universidad", "Universidad de Cundinamarca")
    dato("Fecha", "14 de noviembre de 2026")

    # --- Índice
    d.salto_de_pagina()
    d.indice()
