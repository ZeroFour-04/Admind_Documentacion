# -*- coding: utf-8 -*-
"""Entrega del Código del Proyecto (3 páginas): python build_codigo.py <salida.docx>"""
import sys

from ooxml import (
    BLANCO, G500, V50, V600, V900, Doc, bordes_tc, celda, fila, hipervinculo, imagen, parrafo, ppr, rich, run,
    tabla,
)

LOGO = "C:/Users/Alejandro/Documents/A D M I N D/Frontend/Admind_Front-End/static/img/logo-marca.png"
NOMBRES = ["MANUEL ALEJANDRO ALDANA RINCON", "ANDERSON CAMILO REMISO NIÑO"]
ANCHO = 9360

BACK = "https://github.com/ZeroFour-04/Admind_Backend"
FRONT = "https://github.com/ZeroFour-04/Admind_Front-End"
APP = "https://admind.detkor.com"
SONAR = "https://sonarcloud.io/project/overview?id=ZeroFour-04_{}"

# Datos verificados con gh el 2026-11-18 (la fecha no va en el documento)
PR_BACK, PR_FRONT = 17, 11
SHA_BACK, SHA_FRONT = "2dd5c44", "10e2d04"


def par(contenido, **kw):
    kw.setdefault("antes", 0)
    kw.setdefault("despues", 0)
    kw.setdefault("linea", (252, "auto"))
    return parrafo(contenido, **kw)


def enlace(url, texto=None):
    return hipervinculo(url, texto or url)


def ficha(nombre, subtitulo, url, tecnologias, resumen):
    enc = celda(ANCHO, par(run(nombre, bold=True, color=BLANCO, size=24) +
                           run("  ·  " + subtitulo, color=BLANCO, size=21), keep_next=True),
                fill=V600, bordes=bordes_tc(color=V600), span=2, valign="center")
    filas = [fila([enc], header=True)]
    datos = [
        ("Enlace", par(enlace(url), keep_next=True)),
        ("Tecnologías", par(rich(tecnologias, size=21), keep_next=True)),
        ("Resumen", par(rich(resumen, size=21))),
    ]
    for i, (et, contenido) in enumerate(datos):
        fill = V50 if i % 2 == 0 else None
        filas.append(fila([
            celda(1700, par(run(et, bold=True, color=V900, size=21)), fill=fill, valign="top"),
            celda(ANCHO - 1700, contenido, fill=fill, valign="top"),
        ]))
    return tabla(filas, [1700, ANCHO - 1700], margen_celda=(90, 120))


def construir(d):
    # --- Portada
    d.add(parrafo(" ", antes=0, despues=0, linea=(240, "exact")))
    d.add(f"<w:p>{ppr(alinear='center', antes=0, despues=360)}"
          f"{imagen('rIdLogo', 1800000, 1800000, 'Logo AdMind', 800, 'Logo de AdMind')}</w:p>")
    banda = parrafo(run(" ", size=8), sombra=V600, antes=0, despues=0, linea=(300, "exact"))
    d.add(banda)
    d.add(parrafo("Entrega del Código del Proyecto", estilo="Title", antes=480, despues=160))
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

    # --- Página 2: repositorios
    d.add(parrafo("Repositorios", estilo="Heading1", page_break_before=True))
    d.p("El código de AdMind está en dos repositorios de GitHub: la API y la interfaz web.")
    d.add(ficha(
        "Backend", "API REST", BACK,
        "Python, Django 5.2, Django REST Framework 3.18, PostgreSQL, reportlab (PDF), openpyxl (Excel) y pytest.",
        "API de AdMind con 22 apps de dominio (cuentas, permisos, conjuntos, unidades, reservas, casos, pagos, "
        "reportes y auditoría, entre otras) y flujo por capas controlador → servicio → repositorio. Tiene "
        "funciones, un procedimiento y triggers de PostgreSQL en migraciones, reportes en PDF y Excel, correo en "
        f"HTML y segundo factor (TOTP). 823 pruebas con 94 % de cobertura. Rama `main` en `{SHA_BACK}`, "
        f"{PR_BACK} PR fundidos."))
    d.espacio(300)
    d.add(ficha(
        "Frontend", "Interfaz web", FRONT,
        "Python, Django (plantillas), Alpine.js, HTML y CSS con el sistema de diseño de AdMind, y pytest.",
        "Interfaz web hecha con plantillas de Django y Alpine.js, con componentes `am-*` y color por conjunto. "
        "No toca la base de datos: habla con la API desde el servidor mediante `cliente_api`. Tiene pantallas "
        "por rol (Superusuario, Administración, Secretaría, Residente y Vigilancia), menú según permisos y "
        f"páginas de error propias. 523 pruebas. Rama `main` en `{SHA_FRONT}`, {PR_FRONT} PR fundidos."))

    # --- Página 3: otros enlaces y Git
    d.add(parrafo("Otros enlaces", estilo="Heading1", page_break_before=True))
    anchos = [2300, 3900, 3160]
    cab = [celda(anchos[i], par(run(t, bold=True, color=BLANCO, size=21)), fill=V600,
                 bordes=bordes_tc(color=V600), valign="center")
           for i, t in enumerate(["Recurso", "Enlace", "Qué es"])]
    datos = [
        ("Aplicación desplegada", APP, "admind.detkor.com", "AdMind en funcionamiento."),
        ("GitHub Actions · Backend", BACK + "/actions", "Admind_Backend · Actions",
         "Integración continua: toda la suite con PostgreSQL y cobertura mínima del 70 %."),
        ("GitHub Actions · Frontend", FRONT + "/actions", "Admind_Front-End · Actions",
         "Integración continua: toda la suite en cada PR y cada push."),
        ("SonarCloud · Backend", SONAR.format("Admind_Backend"), "SonarCloud · Admind_Backend",
         "Análisis de calidad del código (proyecto público)."),
        ("SonarCloud · Frontend", SONAR.format("Admind_Front-End"), "SonarCloud · Admind_Front-End",
         "Análisis de calidad del código (proyecto público)."),
    ]
    filas = [fila(cab, header=True)]
    for i, (rec, url, texto, que) in enumerate(datos):
        fill = V50 if i % 2 == 1 else None
        filas.append(fila([
            celda(anchos[0], par(run(rec, bold=True, color=V900, size=21)), fill=fill, valign="top"),
            celda(anchos[1], par(enlace(url, texto)), fill=fill, valign="top"),
            celda(anchos[2], par(rich(que, size=21)), fill=fill, valign="top"),
        ]))
    d.add(tabla(filas, anchos, margen_celda=(90, 120)))
    d.espacio(240)

    d.add(parrafo("Flujo de Git", estilo="Heading2"))
    d.p("El trabajo se organiza en tres ramas: `main`, que es la versión estable y la que se despliega; "
        "`desarrollo`, donde se integra el trabajo; y `pruebas`. Cada cambio nace en una rama corta que entra a "
        "`desarrollo` por *pull request*, y no se funde hasta que GitHub Actions corre toda la suite en verde. "
        "Lo que llega a `main` se despliega de forma continua en la aplicación.")


def main():
    with open(LOGO, "rb") as f:
        logo = f.read()
    d = Doc(titulo="Entrega del Código del Proyecto", autor="Equipo AdMind",
            nombre_encabezado="Entrega del Código del Proyecto", logo_png=logo)
    construir(d)
    d.guardar(sys.argv[1], ultima_portada=True)
    print("guardado:", sys.argv[1])


if __name__ == "__main__":
    main()
