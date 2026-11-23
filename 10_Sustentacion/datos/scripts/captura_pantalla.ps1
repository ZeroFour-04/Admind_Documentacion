# Guarda en PNG lo que se ve en la pantalla principal, entera o un rectángulo.
# Sirve para las capturas del manual de usuario: el panel del navegador de Claude Code no guarda archivos.
# Uso:
#   powershell -ExecutionPolicy Bypass -File captura_pantalla.ps1 -Salida C:\ruta\U01.png
#   powershell -ExecutionPolicy Bypass -File captura_pantalla.ps1 -Salida C:\ruta\U01.png -X 820 -Y 140 -Ancho 1440 -Alto 900
# Sin rectángulo captura la pantalla entera (para ubicar el panel la primera vez).
param(
    [Parameter(Mandatory = $true)][string]$Salida,
    [int]$X = -1, [int]$Y = -1, [int]$Ancho = 0, [int]$Alto = 0
)

Add-Type -AssemblyName System.Drawing
Add-Type -AssemblyName System.Windows.Forms
Add-Type @"
using System;
using System.Runtime.InteropServices;
public static class PuntosReales {
    [DllImport("user32.dll")] public static extern bool SetProcessDPIAware();
}
"@
# Sin esto, con la escala de Windows al 125 % o 150 % las coordenadas salen corridas.
[PuntosReales]::SetProcessDPIAware() | Out-Null

$pantalla = [System.Windows.Forms.Screen]::PrimaryScreen.Bounds
if ($X -lt 0 -or $Ancho -le 0) {
    $X = $pantalla.X; $Y = $pantalla.Y; $Ancho = $pantalla.Width; $Alto = $pantalla.Height
}

$imagen = New-Object System.Drawing.Bitmap $Ancho, $Alto
$lienzo = [System.Drawing.Graphics]::FromImage($imagen)
$lienzo.CopyFromScreen($X, $Y, 0, 0, $imagen.Size)
$carpeta = Split-Path -Parent $Salida
if ($carpeta -and -not (Test-Path $carpeta)) { New-Item -ItemType Directory -Force $carpeta | Out-Null }
$imagen.Save($Salida, [System.Drawing.Imaging.ImageFormat]::Png)
$lienzo.Dispose(); $imagen.Dispose()
Write-Output ("Guardada {0} ({1} x {2} px; pantalla {3} x {4})" -f $Salida, $Ancho, $Alto, $pantalla.Width, $pantalla.Height)
