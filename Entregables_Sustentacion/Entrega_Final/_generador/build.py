# -*- coding: utf-8 -*-
"""Entrega Documentación Metodología Ágil: python build.py <salida.docx>"""
import os
import struct
import sys

import capturas_proc
from ooxml_ma import (
    AMBAR_BG, AMBAR_BORDE, AMBAR_TX, ANCHO_VERTICAL, BLANCO, G500, V50, V600, V700, V900,
    borde_xml, celda, fila, hipervinculo, imagen, parrafo, ppr, rich, run, tabla, Doc,
)

RAIZ = "C:/Users/Alejandro/Documents/A D M I N D"
LOGO = RAIZ + "/Frontend/Admind_Front-End/static/img/logo-marca.png"
CAPTURAS = RAIZ + "/Entregables_Sustentacion/Entrega_Final/capturas"
NOTION = "https://useful-vest-416.notion.site/Seguimiento-Scrum-2-0-AdMind-3f1739efa3338109b3f1e256d441de64"

NOMBRES = ["MANUEL ALEJANDRO ALDANA RINCON", "ANDERSON CAMILO REMISO NIÑO"]

# Figuras: (archivo, qué va, pie de figura)
FIGURAS = {
    "M01": ("M01_tablero.png", "la página del tablero completa, con el recuadro «Cómo se usa» y las bases de datos",
            "Figura 1. Página principal del tablero de seguimiento en Notion: el recuadro «Cómo se usa» y las reglas del tablero."),
    "M02": ("M02_historia.png", "una historia de usuario abierta, con sus tareas, el avance y las dos casillas de la DoD",
            "Figura 2. Una historia de usuario abierta (HU-01): estado, responsable, sprint, story points, avance y sus tareas."),
    "M03": ("M03_backlog.png", "la tabla de Historias de Usuario con story points, sprint y estado",
            "Figura 3. Product Backlog en vista kanban: historias agrupadas por estado, con sprint, story points y avance."),
    "M04": ("M04_sprints.png", "la base de Sprints con SP comprometidos, completados y % de cumplimiento",
            "Figura 4. Base de Sprints: SP comprometidos, SP completados, % de cumplimiento y velocidad base."),
    "M05": ("M05_kanban.png", "el kanban de tareas, o las HU del Sprint 8",
            "Figura 5. Kanban de tareas del tablero, agrupadas por estado."),
}
ALTO_MAX_EMU = 3240000   # 9 cm
ANCHO_MAX_EMU = 5943600  # 16,5 cm (ancho útil)
pendientes = []


def tam_png(datos):
    ancho, alto = struct.unpack(">II", datos[16:24])
    return ancho, alto


def figura(d, clave):
    archivo, que, pie = FIGURAS[clave]
    cargada = capturas_proc.cargar(CAPTURAS, clave)
    if cargada:
        datos, _ = cargada
        w, h = tam_png(datos)
        cx = ANCHO_MAX_EMU
        cy = int(cx * h / w)
        if cy > ALTO_MAX_EMU:
            cy = ALTO_MAX_EMU
            cx = int(cy * w / h)
        rid = d.registrar_imagen(datos)
        ident = d.ident() + 100
        d.add(f"<w:p>{ppr(alinear='center', antes=60, despues=0, keep_next=True)}"
              f"{imagen(rid, cx, cy, clave, ident, pie)}</w:p>")
    else:
        pendientes.append(f"{clave} ({archivo}): {que}")
        titulo = parrafo(run(f"Captura pendiente: {que}", bold=True, color=AMBAR_TX, size=21),
                         alinear="center", antes=0, despues=40)
        sub = parrafo(run(f"Archivo esperado: capturas\\{archivo}", color=AMBAR_TX, size=19),
                      alinear="center", antes=0, despues=0)
        bordes = ("<w:tcBorders>" + "".join(borde_xml(l, sz=6, color=AMBAR_BORDE)
                                            for l in ("top", "left", "bottom", "right")) + "</w:tcBorders>")
        c = celda(ANCHO_VERTICAL, titulo + sub, fill=AMBAR_BG, bordes=bordes, valign="center")
        d.add(tabla([fila([c], alto=3600)], [ANCHO_VERTICAL], bordes_tabla=False))
    d.add(parrafo(pie, estilo="Pie", alinear="center", keep_lines=True))


def recuadro_enlace(d, titulo, intro):
    """Recuadro verde con el enlace al tablero como hipervínculo."""
    pars = [
        parrafo(run(titulo, bold=True, color=V900, size=22), antes=0, despues=60, keep_next=True),
        parrafo(rich(intro, color=V900, size=21), antes=0, despues=80, keep_next=True),
        parrafo(hipervinculo(NOTION, NOTION), antes=0, despues=40),
    ]
    bordes = ("<w:tcBorders>" + borde_xml("top", color=V600) + borde_xml("left", sz=36, color=V600)
              + borde_xml("bottom", color=V600) + borde_xml("right", color=V600) + "</w:tcBorders>")
    c = celda(ANCHO_VERTICAL, "".join(pars), fill=V50, bordes=bordes,
              margenes='<w:tcMar><w:top w:w="110" w:type="dxa"/><w:left w:w="200" w:type="dxa"/>'
                       '<w:bottom w:w="90" w:type="dxa"/><w:right w:w="160" w:type="dxa"/></w:tcMar>')
    d.add(tabla([fila([c])], [ANCHO_VERTICAL], bordes_tabla=False))
    d.espacio(120)


def portada(d):
    d.add(parrafo(" ", antes=0, despues=0, linea=(240, "exact")))
    d.add(f"<w:p>{ppr(alinear='center', antes=0, despues=360)}"
          f"{imagen('rIdLogo', 1800000, 1800000, 'Logo AdMind', 800, 'Logo de AdMind')}</w:p>")
    banda = parrafo(run(" ", size=8), sombra=V600, antes=0, despues=0, linea=(300, "exact"))
    d.add(banda)
    d.add(parrafo("Entrega Documentación Metodología Ágil", estilo="Title", antes=480, despues=160))
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
    d.salto_de_pagina()


def indice(d):
    d.add(parrafo("Contenido", estilo="TituloContenido"))
    d.add(
        "<w:p>"
        '<w:r><w:fldChar w:fldCharType="begin"/></w:r>'
        '<w:r><w:instrText xml:space="preserve"> TOC \\o "1-1" \\h \\z \\u </w:instrText></w:r>'
        '<w:r><w:fldChar w:fldCharType="separate"/></w:r>'
        + run("El índice se genera al abrir el documento en Word.", italic=True, color=G500)
        + '<w:r><w:fldChar w:fldCharType="end"/></w:r></w:p>'
    )


def contenido(d):
    # 1 ------------------------------------------------------------------
    d.h1("1. Introducción")
    d.p(rich("Gestionamos AdMind con **Scrum**: el trabajo se escribe como historias de usuario (HU) medidas en "
             "*story points* (SP), se agrupa en sprints y cada historia solo cuenta como terminada cuando cumple la "
             "*Definition of Done* (DoD). El seguimiento vive en un tablero de **Notion** público, que reúne el "
             "backlog, las tareas y los sprints en tres bases de datos relacionadas. Este documento explica cómo "
             "está armado el tablero, cómo trabajamos y cómo fue el avance sprint a sprint, incluido lo que nos "
             "costó y lo que cambiamos. Tablero: ")
        + hipervinculo(NOTION, "Seguimiento Scrum 2.0 · AdMind") + run("."))

    # 2 ------------------------------------------------------------------
    d.h1("2. Cómo está organizado el tablero")
    d.p("El tablero tiene tres bases de datos que se enlazan entre sí. Una vista de **alertas** muestra solo lo "
        "incoherente (por ejemplo, una HU marcada como terminada sin la DoD completa).")
    d.tabla(
        ["Base de datos", "Qué guarda", "Cómo se relaciona"],
        [
            ["**Historias de Usuario** (Product Backlog)",
             "Cada HU con prioridad, rol, story points del *poker planning*, sprint, responsable, «Depende de», "
             "avance, alerta y las dos casillas de la DoD.",
             "Se migró del Excel de planeación con 38 historias. «Depende de» enlaza una HU con las que necesita."],
            ["**Tareas**",
             "Cada HU se parte en tareas con estado (sin empezar, en progreso, bloqueada, finalizada) y capa "
             "(backend, frontend o pruebas). Hay un kanban.",
             "Cada tarea pertenece a una HU y hereda su responsable. El avance de la HU se calcula con sus tareas."],
            ["**Sprints**",
             "SP comprometidos, SP completados, % de cumplimiento, avance de tareas y la velocidad para planear "
             "el siguiente.",
             "Suma los SP de las HU de cada sprint. Una HU solo aporta SP cuando está finalizada."],
        ],
        [2000, 4000, 3360],
    )
    figura(d, "M01")

    # 3 ------------------------------------------------------------------
    d.h1("3. Reglas de trabajo y Definition of Done")
    d.vinetas([
        "Una HU solo suma SP en estado **Finalizado**, y solo llega ahí con la DoD marcada.",
        "**DoD humana:** el PR de `desarrollo` a `pruebas` lo revisa el otro integrante, y la prueba manual la hace "
        "quien no programó la HU.",
        "Lo que no se termina vuelve al backlog con sus SP intactos.",
        "La capa de cada tarea (backend, frontend o pruebas) muestra si alguien se queda solo en una parte, para "
        "rotar el trabajo.",
    ])
    figura(d, "M02")

    # 4 ------------------------------------------------------------------
    d.h1("4. Planeación: backlog, poker planning y velocidad")
    d.p("El backlog nació de la planeación inicial con 38 historias. Los story points salieron de un *poker "
        "planning* entre los dos integrantes y, con el tiempo, el backlog creció con las historias nuevas.")
    d.p("**Velocidad.** Sin historial, el Sprint 1 se planeó con una base teórica de 81,7 SP (26,43 min por SP sobre "
        "2160 min de capacidad); en la práctica comprometimos 25 SP. Desde el segundo sprint planeamos con el "
        "promedio de los SP completados en los sprints anteriores.")
    figura(d, "M03")

    # 5 ------------------------------------------------------------------
    d.h1("5. Desarrollo por sprint")
    d.p("La tabla resume cada sprint con los SP comprometidos y el estado de sus historias. Los números salen del "
        "tablero.")
    d.tabla(
        ["Sprint", "Historias", "SP comp.", "SP compl.", "Estado de las HU"],
        [
            ["1", "HU-01, 02, 03, 04, 05 y 26", "25", "25", "Todas finalizadas"],
            ["2", "HU-06, 07, 08 y 09", "20", "20", "Todas finalizadas"],
            ["3", "HU-10, 11, 12 y 13", "26", "26", "Todas finalizadas"],
            ["4", "HU-14 a HU-19", "28", "28", "Todas finalizadas"],
            ["5", "HU-20, 21, 25, 27, 28, 29 y la mini HU «Tipos de zona (con y sin reserva)»", "33", "28",
             "Finalizadas todas menos HU-20 (sin empezar)"],
            ["6", "HU-22, 23, 24 y HU-30 a HU-34", "38", "30",
             "Finalizadas todas menos HU-32 (sin empezar)"],
            ["7", "HU-35, 36, 37, 38 y HU-40 «Mejorar Visual en General» (agregada)", "31", "12",
             "Finalizadas HU-35 y HU-40; HU-36, 37 y 38 sin empezar"],
            ["8", "19 HU: HU-39, HU-40 «Implementar accesibilidad» y HU-41 a HU-57", "86", "38",
             "9 finalizadas (HU-41, 42, 44, 48, 49, 53, 54, 56 y 57); en revisión HU-39, 40 y 43; en progreso "
             "HU-45, 46, 47, 50 y 51; sin empezar HU-52 y HU-55"],
        ],
        [900, 2900, 800, 800, 3960], centro=(0, 2, 3),
    )
    figura(d, "M04")

    d.h2("Sprints 1 a 3: un arranque difícil")
    d.p("Al principio nos costó avanzar y cerrar las HU al 100 %. En el Sprint 1 el trabajo técnico terminó, pero el "
        "tablero marcó 0 de 25 SP: ninguna HU cumplía la DoD, porque faltaban el PR revisado por el otro integrante "
        "y la prueba manual de quien no la programó (la rama `pruebas` ni siquiera existía en el backend). Además, "
        "las HU estaban **interrelacionadas**. HU-03, el asistente para crear un conjunto, cumplía 3 de 5 criterios "
        "porque dependía de áreas, reglamento, reglas y auditoría, que eran de otros sprints. Por eso agregamos al "
        "tablero el campo «Depende de». Solo hacia el Sprint 3 quedaron completas todas las HU del Sprint 1.")
    d.h2("El ajuste: redistribuir las historias")
    d.p("Una vez entendido el porqué, **redistribuimos las HU** para que cada sprint pudiera cerrar sus historias "
        "sin esperar a otro, y empezamos a mirar las dependencias al planear.")
    d.h2("Sprints 4 y 5: la mejora")
    d.p("El cambio se notó. El Sprint 4 cerró sus 6 HU y el Sprint 5 cerró 6 de 7 (28 de 33 SP); la HU-20 quedó "
        "sin empezar.")
    d.h2("Sprints 6 a 8: más carga")
    d.p("El Sprint 6 fue el más cargado (38 SP) y cerró 7 de sus 8 HU; solo HU-32 quedó sin empezar. El **Sprint 7 "
        "creció** porque entró HU-40, la mejora visual general, y apareció un **Sprint 8** con 13 HU nuevas (HU-45 a "
        "HU-57): Sonar, despliegue, ajustes de producción, procedimientos y triggers, reportes, JWT, CORS, Swagger, "
        "correo en HTML, pantallas, un bug de casos, documentación y presentación. Esa carga extra vino de lo que "
        "pidió la sustentación técnica y de lo nuevo del Proyecto de Gestión del Conocimiento (PGC) de la "
        "universidad, que se hace cada tres semestres y este semestre pidió una sustentación de negocio de AdMind.")
    d.p("El Sprint 8 es el mayor del proyecto: 19 HU y 86 SP. En el tablero tiene 9 HU finalizadas, entre ellas las "
        "pruebas unitarias (94 % de cobertura), GitHub Actions, los procedimientos y triggers, los reportes, el "
        "correo en HTML, las pantallas y los manuales. SonarCloud ya corre en los PR de los dos repositorios, aunque "
        "faltan corregir vulnerabilidades, y el despliegue coincide con `main`, con tareas todavía abiertas. "
        "**JWT, CORS y Swagger aún no están en `main`**, y el bug de casos no ha empezado.")
    figura(d, "M05")

    # 6 ------------------------------------------------------------------
    d.h1("6. Lecciones aprendidas")
    d.p("Lo que cambiamos a mitad de camino y lo que haríamos distinto desde el primer día:")
    d.vinetas([
        "**Partir las HU** para que ninguna dependa de otra de un sprint posterior; si una HU necesita áreas, "
        "reglas o auditoría, esas piezas entran antes o en el mismo sprint.",
        "**Marcar las dependencias desde la planeación**, con el campo «Depende de», y no descubrirlas al "
        "cerrar el sprint.",
        "**Hacer la DoD humana al cierre de cada HU** y no al final del sprint: el PR revisado y la prueba del otro "
        "integrante evitan que todo se acumule y el sprint termine en 0 SP.",
        "**Crear la rama pruebas y la revisión cruzada desde el primer sprint**, para que la DoD se pueda cumplir.",
        "**Dejar margen para lo nuevo:** el Sprint 8 mostró que los requisitos de la sustentación pueden llegar tarde.",
    ])

    # 7 ------------------------------------------------------------------
    d.h1("7. Enlace al tablero")
    recuadro_enlace(d, "Tablero de seguimiento Scrum en Notion",
                    "El tablero es público: contiene el backlog, las tareas y los sprints descritos en este documento.")


def main():
    salida = sys.argv[1]
    with open(LOGO, "rb") as f:
        logo = f.read()
    d = Doc(titulo="Entrega Documentación Metodología Ágil", autor="Equipo AdMind",
            nombre_encabezado="Entrega Documentación Metodología Ágil", logo_png=logo)
    portada(d)
    indice(d)
    contenido(d)
    d.guardar(salida, ultima_portada=True)
    print("guardado:", salida)
    for p in pendientes:
        print("PENDIENTE:", p)


if __name__ == "__main__":
    main()
