param(
    [Parameter(Mandatory = $true)][string]$Crudo,
    [Parameter(Mandatory = $true)][string]$DocxFinal,
    [Parameter(Mandatory = $true)][string]$PdfFinal
)
# Abre el .docx armado a mano en Word, actualiza la tabla de contenido y los
# campos, guarda el .docx y exporta el PDF con marcadores de titulos.
$ErrorActionPreference = 'Stop'
$w = New-Object -ComObject Word.Application
$w.Visible = $false
$w.DisplayAlerts = 0
try {
    $d = $w.Documents.Open($Crudo)
    $d.Repaginate()
    $d.TablesOfContents.Item(1).Update()
    $d.Fields.Update() | Out-Null
    $d.Repaginate()
    $d.TablesOfContents.Item(1).UpdatePageNumbers()
    $d.Repaginate()
    if (Test-Path $DocxFinal) { Remove-Item $DocxFinal -Force }
    if (Test-Path $PdfFinal) { Remove-Item $PdfFinal -Force }
    $d.SaveAs([ref]$DocxFinal, [ref]16)
    $d.ExportAsFixedFormat($PdfFinal, 17, $false, 0, 0, 1, 1, 0, $true, $true, 1, $true, $true, $false)
    $paginas = $d.ComputeStatistics(2)
    Write-Output "paginas=$paginas"
    $d.Close(0)
}
finally {
    $w.Quit()
}
