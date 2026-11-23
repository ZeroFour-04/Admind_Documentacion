# -*- coding: utf-8 -*-
"""Prepara las capturas para el documento: recorta bordes de la interfaz y tapa las fechas visibles
(regla del documento: sin fechas). Los originales no se modifican."""
import io
import glob
import os

from PIL import Image, ImageStat


def _tapar(im, caja):
    """Rellena la caja con el color mediano de su propio contenido (el fondo)."""
    region = im.crop(caja)
    color = tuple(int(v) for v in ImageStat.Stat(region).median[:3])
    im.paste(color, caja)


def _m01(im):
    return im


def _m02(im):
    # Fuera la barra superior (breadcrumb, banner, "Última edición") y la nota "Migradas el ..." de abajo.
    im = im.crop((0, 92, 1600, 706))
    # Columna "Actualizada" (fechas): cinco filas. Coordenadas originales menos 92 en y.
    for cy in (402, 435, 469, 502, 535):
        _tapar(im, (358, cy - 92 - 11, 528, cy - 92 + 11))
    return im


def _m03(im):
    return im


def _m04(im):
    im = im.crop((0, 0, 1200, 409))  # sin la columna Notas (trae fechas)
    _tapar(im, (340, 341, 436, 362))  # "14 de noviembre" del Sprint 8
    return im


def _m05(im):
    for caja in ((664, 336, 934, 380), (664, 549, 934, 592), (664, 788, 934, 834), (974, 384, 1246, 466)):
        _tapar(im, caja)
    return im


PROC = {"M01": _m01, "M02": _m02, "M03": _m03, "M04": _m04, "M05": _m05}


def cargar(carpeta, clave):
    """Devuelve (bytes_png, ruta_origen) o None si la captura no existe."""
    for ext in ("png", "jpg", "jpeg"):
        rutas = glob.glob(os.path.join(carpeta, f"{clave}_*.{ext}"))
        if rutas:
            im = Image.open(rutas[0]).convert("RGB")
            im = PROC[clave](im)
            buf = io.BytesIO()
            im.save(buf, "PNG", optimize=True)
            return buf.getvalue(), rutas[0]
    return None
