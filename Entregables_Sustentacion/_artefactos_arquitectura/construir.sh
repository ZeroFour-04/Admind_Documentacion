#!/usr/bin/env bash
# Arma las dos páginas: cabeza + estilo + cuerpo + script. Uso: ./construir.sh [url_arquitectura] [url_produccion]
cd "$(dirname "$0")"
armar(){ # $1 nombre, $2 html del enlace a la otra página
  { cat "_$1.cabeza.html"; echo "<style>"; cat _estilo.css; echo "</style>"
    awk -v enlace="$2" '{ gsub(/<!--ENLACE_OTRA-->/, enlace); print }' "_$1.cuerpo.html"
    echo "<script>"; cat _comun.js; echo "</script>"; } > "$1.html"
}
A="${1:-}"; P="${2:-}"
armar arquitectura "${P:+La otra página: <a href=\"$P\">AdMind en producción</a>, con las pruebas, el CI, SonarCloud y el despliegue.}"
armar produccion "${A:+La otra página: <a href=\"$A\">Arquitectura de AdMind</a>, con el sistema, las capas, el aislamiento y la base.}"
