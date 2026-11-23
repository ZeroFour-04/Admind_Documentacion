param(
    [Parameter(Mandatory = $true)][string]$Docx,
    [Parameter(Mandatory = $true)][string]$Pdf,
    [switch]$GuardarDocx
)
# Abre el .docx en Word, actualiza el índice y los campos, y exporta el PDF.
$ErrorActionPreference = "Stop"
$word = New-Object -ComObject Word.Application
$word.Visible = $false
$word.DisplayAlerts = 0
try {
    $doc = $word.Documents.Open($Docx, $false, $false)
    # Dos pasadas: la primera llena el índice y puede mover las páginas; la segunda ajusta los números.
    for ($i = 0; $i -lt 2; $i++) {
        if ($doc.TablesOfContents.Count -gt 0) { $doc.TablesOfContents.Item(1).Update() }
        $doc.Fields.Update() | Out-Null
        $doc.Repaginate()
    }
    "Paginas: " + $doc.ComputeStatistics(2)
    if ($GuardarDocx) { $doc.Save() }
    # 17 = PDF; 1 = marcadores a partir de los títulos
    $doc.ExportAsFixedFormat($Pdf, 17, $false, 0, 0, 1, 1, 0, $true, $true, 1, $true, $true, $false)
    $doc.Close($false)
}
finally {
    $word.Quit()
}
"PDF: " + $Pdf
