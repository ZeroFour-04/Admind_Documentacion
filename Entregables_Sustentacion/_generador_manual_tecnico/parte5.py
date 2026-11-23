# -*- coding: utf-8 -*-
"""Parte 5: anexos. A (endpoints) y B (glosario). Todo en carta vertical."""
from descripciones import DESC
from parte3 import ENDPOINTS_MD

ANCHOS_ANEXO = [3100, 1000, 2300, 2960]  # suman 9360 = ANCHO_VERTICAL


def leer_endpoints():
    """{módulo: [(ruta, métodos, vista, descripción)]} a partir de endpoints_api.md."""
    modulos, actual = {}, None
    for linea in open(ENDPOINTS_MD, encoding="utf-8"):
        linea = linea.rstrip("\n")
        if linea.startswith("## "):
            actual = linea[3:].strip()
            modulos[actual] = []
        elif actual and linea.startswith("| `/"):
            celdas = [c.strip() for c in linea.strip().strip("|").split("|")]
            ruta, metodos, vista, texto = celdas[0], celdas[1], celdas[2], celdas[3] if len(celdas) > 3 else ""
            modulos[actual].append((ruta.strip("`"), metodos, vista.strip("`"), texto))
    return modulos


def anexo_a(d):
    d.h1("Anexo A. Endpoints de la API")
    d.p("Rutas reales de la API en la rama `main` (`b89d9f2`) el 14 de noviembre de 2026: **97 rutas**, una tabla por "
        "módulo. Los métodos son los que acepta cada ruta; la vista es la clase de `views.py` que la atiende.")
    d.p("Toda ruta exige la cabecera `Authorization: Token <token>`, salvo cuatro, que no piden token: el ingreso "
        "(`/auth/login/`), la recuperación de contraseña (`/auth/recuperar/`), el restablecimiento de la "
        "contraseña (`/auth/recuperar/confirmar/`) y la confirmación del restablecimiento del segundo factor "
        "(`/auth/dos-factores/restablecer/confirmar/`), que se valida con un enlace firmado enviado al correo.")
    modulos = leer_endpoints()
    total = sum(len(v) for v in modulos.values())
    assert total == 97, total
    faltan = []
    for modulo, rutas in modulos.items():
        d.h3(f"{modulo} ({len(rutas)} {'ruta' if len(rutas) == 1 else 'rutas'})")
        filas = []
        for ruta, metodos, vista, texto in rutas:
            frase = texto or DESC.get(vista, "")
            if not frase:
                faltan.append((modulo, vista))
            filas.append([ruta, metodos, vista, frase])
        d.tabla(["Ruta", "Métodos", "Vista", "Qué hace"], filas, ANCHOS_ANEXO, mono=(0, 2), tam=18, tam_codigo=16,
                junta=len(rutas) <= 7)
    assert not faltan, faltan


GLOSARIO = [
    ("Auditoría", "Registro de solo inserción de las acciones del sistema: el modelo y su QuerySet no admiten "
                  "`update()` ni `delete()`."),
    ("Bloqueo", "Los 3 minutos exclusivos que tiene una persona para llenar y enviar una solicitud sobre una franja."),
    ("Conjunto activo", "El conjunto con el que se trabaja en la sesión. Sale del token y nunca de la petición."),
    ("ContextVar", "Variable «por petición» de Python: aunque dos peticiones corran a la vez, cada una ve su propio "
                   "valor. Guarda el conjunto activo mientras se atiende la petición."),
    ("FK compuesta", "Llave foránea de dos columnas (`area_id`, `conjunto_id`) que hace imposible, en la base de "
                     "datos, apuntar a una fila de otro conjunto."),
    ("Franja", "Un bloque de horario de un área en una fecha: (área, fecha, hora de inicio, hora de fin). El estado "
               "vive en la solicitud, no en la franja."),
    ("Huella del token", "El SHA-256 del token de sesión. Es lo único que se guarda del token en la base de datos."),
    ("Índice único parcial", "Índice «único, pero solo entre las filas que cumplen una condición». Es lo que "
                             "resuelve la concurrencia de las reservas: solo cuentan las solicitudes bloqueantes."),
    ("`ManagerDeConjunto`", "Reemplaza `Modelo.objects` y agrega a toda consulta el filtro por el conjunto activo. "
                            "Sin conjunto activo lanza `SinConjuntoActivo`."),
    ("Prueba del intruso", "Prueba automática que recorre todas las rutas de la API actuando desde otro conjunto, "
                           "para comprobar que ninguna entrega ni modifica datos ajenos."),
    ("Regla alfa", "Regla de reserva del conjunto, sin área: una sola por tipo y versionada. La define "
                   "Administración."),
    ("Regla beta", "Regla de reserva de una zona o área: una sola por tipo en cada zona y versionada. La define "
                   "Administración."),
    ("Regla del sistema", "Regla fija en el código (`apps/reglas/sistema.py`) que nadie puede apagar, como que la "
                          "solicitud no esté en el pasado."),
    ("Segundo factor (TOTP)", "Código de 6 dígitos que cambia con el tiempo y genera una aplicación autenticadora. Lo "
                              "exigen los roles con permisos sensibles."),
    ("Tabla global", "Tabla sin `conjunto_id`, como `Persona`, `Usuario` o `Conjunto`. Están en una lista cerrada que "
                     "una prueba vigila."),
]


def anexo_b(d):
    d.h1("Anexo B. Glosario")
    d.p("Términos técnicos del proyecto, en una frase cada uno.", keep_next=True)
    d.tabla(["Término", "Significa"], [[f"**{t}**" if "`" not in t else t, s] for t, s in GLOSARIO], [2500, 6860],
            tam=20)


def construir(d):
    d.cerrar_seccion(portada=True)      # cierra la sección de la portada y los capítulos 1 a 9
    anexo_a(d)
    d.cerrar_seccion()                  # el Anexo B empieza en página nueva, también vertical
    anexo_b(d)
