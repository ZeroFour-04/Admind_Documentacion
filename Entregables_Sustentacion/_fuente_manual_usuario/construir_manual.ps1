# Arma AdMind_Manual_Usuario.docx y su PDF con Word (COM), a partir de meta.json y cap*.json.
# Solo ASCII en este archivo: todo el texto en espanol vive en los JSON (UTF-8).
# Uso:
#   powershell -ExecutionPolicy Bypass -File construir_manual.ps1 -Fuente <carpeta> -Capturas <carpeta> -Logo <png> -Salida <ruta.docx>
param(
    [Parameter(Mandatory = $true)][string]$Fuente,
    [Parameter(Mandatory = $true)][string]$Capturas,
    [Parameter(Mandatory = $true)][string]$Logo,
    [Parameter(Mandatory = $true)][string]$Salida
)
$ErrorActionPreference = 'Stop'

function Rgb([string]$h) {
    return [Convert]::ToInt32($h.Substring(0, 2), 16) + 256 * [Convert]::ToInt32($h.Substring(2, 2), 16) + 65536 * [Convert]::ToInt32($h.Substring(4, 2), 16)
}
function Leer([string]$ruta) { return [IO.File]::ReadAllText($ruta, [Text.Encoding]::UTF8) }

$VERDE600 = '0E6B5A'; $VERDE700 = '0B5546'; $VERDE900 = '06302A'; $VERDE50 = 'EEF5F2'
$TEXTO = '14201D'; $GRIS500 = '64706C'; $GRIS200 = 'D6DCDA'
$AMBARF = 'FBF0DC'; $AMBART = '6B4A05'; $AMBARB = 'D9A441'
$ANCHO = 470.2   # ancho util en puntos (carta, margenes de 2,5 cm)

# ---------- lectura del contenido ----------
$meta = (Leer (Join-Path $Fuente 'meta.json')) | ConvertFrom-Json
$bloques = @()
foreach ($f in (Get-ChildItem $Fuente -Filter 'cap*.json' | Sort-Object Name)) {
    $lote = (Leer $f.FullName) | ConvertFrom-Json
    foreach ($x in $lote) { $bloques += $x }
}
# primera pasada: numerar las figuras en el orden en que aparecen
$numFig = @{}; $n = 0
foreach ($b in $bloques) { if ($b.t -eq 'fig') { $n++; $numFig[$b.id] = $n } }
$totalFig = $n
function Refs([string]$s) {
    return [regex]::Replace($s, '\{(U\d\d[a-z]?)\}', {
            param($m)
            $id = $m.Groups[1].Value
            if ($numFig.ContainsKey($id)) { 'Figura ' + $numFig[$id] } else { '[Figura ' + $id + ' pendiente]' }
        })
}
$faltan = New-Object System.Collections.ArrayList

# ---------- Word ----------
$word = New-Object -ComObject Word.Application
$word.Visible = $false
$word.DisplayAlerts = 0
$doc = $null
try {
    $doc = $word.Documents.Add()
    $sel = $word.Selection

    # pagina carta, margenes de 2,5 cm; la portada no lleva encabezado ni pie
    $pg = $doc.PageSetup
    $pg.PageWidth = 612; $pg.PageHeight = 792
    $pg.TopMargin = 72; $pg.BottomMargin = 68; $pg.LeftMargin = 70.9; $pg.RightMargin = 70.9
    $pg.HeaderDistance = 30; $pg.FooterDistance = 30
    $pg.DifferentFirstPageHeaderFooter = -1

    # ---------- estilos ----------
    $normal = $doc.Styles.Item(-1)
    $normal.Font.Name = 'Calibri'; $normal.Font.Size = 11; $normal.Font.Color = (Rgb $TEXTO)
    $normal.ParagraphFormat.SpaceBefore = 0; $normal.ParagraphFormat.SpaceAfter = 6
    $normal.ParagraphFormat.LineSpacingRule = 5; $normal.ParagraphFormat.LineSpacing = 13.8
    $normal.LanguageID = 9226

    function ConfigurarTitulo($id, $tam, $color, $antes, $despues, $salto) {
        $s = $doc.Styles.Item([int]$id)
        $s.Font.Name = 'Calibri'; $s.Font.Size = $tam; $s.Font.Bold = 1; $s.Font.Italic = 0; $s.Font.Color = (Rgb $color)
        $s.ParagraphFormat.SpaceBefore = $antes; $s.ParagraphFormat.SpaceAfter = $despues
        $s.ParagraphFormat.KeepWithNext = -1; $s.ParagraphFormat.KeepTogether = -1
        $s.ParagraphFormat.LineSpacingRule = 0
        if ($salto) { $s.ParagraphFormat.PageBreakBefore = -1 } else { $s.ParagraphFormat.PageBreakBefore = 0 }
        return $s
    }
    $h1 = ConfigurarTitulo -2 24 $VERDE600 0 12 $true
    $bd = $h1.ParagraphFormat.Borders.Item(-3)
    $bd.LineStyle = 1; $bd.LineWidth = 8; $bd.Color = (Rgb $VERDE600)
    $h1.ParagraphFormat.Borders.DistanceFromBottom = 4
    $null = ConfigurarTitulo -3 16 $VERDE700 16 6 $false
    $null = ConfigurarTitulo -4 13 $VERDE700 12 4 $false

    function NuevoEstilo([string]$nombre) {
        $s = $doc.Styles.Add($nombre, 1)
        $s.BaseStyle = $normal.NameLocal
        return $s
    }
    $stNota = NuevoEstilo 'AM Nota'
    $stNota.ParagraphFormat.LeftIndent = 8; $stNota.ParagraphFormat.RightIndent = 4
    $stNota.ParagraphFormat.SpaceBefore = 2; $stNota.ParagraphFormat.SpaceAfter = 2
    $stNota.ParagraphFormat.Shading.BackgroundPatternColor = (Rgb $VERDE50)
    $bn = $stNota.ParagraphFormat.Borders.Item(-2)
    $bn.LineStyle = 1; $bn.LineWidth = 24; $bn.Color = (Rgb $VERDE600)
    $stNota.ParagraphFormat.Borders.DistanceFromLeft = 6

    $stAviso = NuevoEstilo 'AM Aviso'
    $stAviso.Font.Color = (Rgb $AMBART)
    $stAviso.ParagraphFormat.LeftIndent = 8; $stAviso.ParagraphFormat.RightIndent = 4
    $stAviso.ParagraphFormat.SpaceBefore = 2; $stAviso.ParagraphFormat.SpaceAfter = 2
    $stAviso.ParagraphFormat.Shading.BackgroundPatternColor = (Rgb $AMBARF)
    $ba = $stAviso.ParagraphFormat.Borders.Item(-2)
    $ba.LineStyle = 1; $ba.LineWidth = 24; $ba.Color = (Rgb $AMBARB)
    $stAviso.ParagraphFormat.Borders.DistanceFromLeft = 6

    $stFigura = NuevoEstilo 'AM Figura'
    $stFigura.ParagraphFormat.Alignment = 1
    $stFigura.ParagraphFormat.SpaceBefore = 8; $stFigura.ParagraphFormat.SpaceAfter = 3
    $stFigura.ParagraphFormat.KeepWithNext = -1; $stFigura.ParagraphFormat.LineSpacingRule = 0

    $stPie = NuevoEstilo 'AM Pie de figura'
    $stPie.Font.Size = 9.5; $stPie.Font.Italic = 1; $stPie.Font.Color = (Rgb $GRIS500)
    $stPie.ParagraphFormat.Alignment = 1; $stPie.ParagraphFormat.SpaceAfter = 14

    $stPaso = NuevoEstilo 'AM Paso'
    $stPaso.ParagraphFormat.SpaceAfter = 4

    $stTabla = NuevoEstilo 'AM Tabla'
    $stTabla.Font.Size = 10; $stTabla.ParagraphFormat.SpaceAfter = 2; $stTabla.ParagraphFormat.SpaceBefore = 2
    $stTabla.ParagraphFormat.LineSpacingRule = 0

    $stIndice = NuevoEstilo 'AM Titulo de indice'
    $stIndice.Font.Size = 24; $stIndice.Font.Bold = 1; $stIndice.Font.Color = (Rgb $VERDE600)
    $stIndice.ParagraphFormat.PageBreakBefore = -1; $stIndice.ParagraphFormat.SpaceAfter = 14

    $stBanda = NuevoEstilo 'AM Banda'
    $stBanda.Font.Color = (Rgb 'FFFFFF'); $stBanda.Font.Bold = 1
    $stBanda.ParagraphFormat.Alignment = 1; $stBanda.ParagraphFormat.SpaceAfter = 0
    $stBanda.ParagraphFormat.LineSpacingRule = 0
    $stBanda.ParagraphFormat.Shading.BackgroundPatternColor = (Rgb $VERDE600)

    $stCentro = NuevoEstilo 'AM Portada'
    $stCentro.ParagraphFormat.Alignment = 1; $stCentro.ParagraphFormat.SpaceAfter = 0

    $stVineta = $doc.Styles.Item(-49)
    $stVineta.ParagraphFormat.SpaceAfter = 3

    # ---------- utilidades de escritura ----------
    $stNormal = $normal
    $stFuerte = $doc.Styles.Item(-88)       # Strong
    $stPorDefecto = $doc.Styles.Item(-66)   # Default Paragraph Font

    function Estilo($s) {
        $sel.Style = $s
        $sel.Font.Reset()
        $sel.ParagraphFormat.Reset()
    }
    function Escribir([string]$texto) {
        $texto = Refs $texto
        $partes = $texto -split '\*\*'
        for ($i = 0; $i -lt $partes.Count; $i++) {
            if ($partes[$i] -eq '') { continue }
            if ($i % 2 -eq 1) { $sel.Style = $stFuerte }
            $sel.TypeText($partes[$i])
            if ($i % 2 -eq 1) { $sel.Style = $stPorDefecto }
        }
    }
    function Parrafo($estilo, [string]$texto) {
        Estilo $estilo
        Escribir $texto
        $sel.TypeParagraph()
    }
    function Titulo($id, [string]$texto) {
        Estilo ($doc.Styles.Item([int]$id))
        $sel.TypeText($texto)
        $sel.TypeParagraph()
    }
    function Pasos($items) {
        $ini = $sel.Start
        foreach ($it in $items) { Parrafo $stPaso $it }
        $fin = $sel.Start
        $rng = $doc.Range($ini, $fin - 1)
        $lt = $doc.ListTemplates.Add($false)
        $lv = $lt.ListLevels.Item(1)
        $lv.NumberFormat = '%1.'; $lv.NumberStyle = 0; $lv.TrailingCharacter = 0
        $lv.NumberPosition = 14; $lv.TextPosition = 32; $lv.TabPosition = 32; $lv.StartAt = 1
        $rng.ListFormat.ApplyListTemplate($lt, $false, 0)
    }
    function Vinetas($items) {
        foreach ($it in $items) { Parrafo $stVineta $it }
    }
    function Cuadro($estilo, [string]$titulo, [string]$texto, $items) {
        if ($titulo) {
            Estilo $estilo
            Escribir ('**' + $titulo + '.** ' + $texto)
            $sel.TypeParagraph()
        } elseif ($texto) {
            Parrafo $estilo $texto
        }
        if ($items -and @($items).Count -gt 0) {
            $ini = $sel.Start
            foreach ($it in @($items)) { Parrafo $estilo $it }
            $fin = $sel.Start
            $rng = $doc.Range($ini, $fin - 1)
            $rng.ListFormat.ApplyBulletDefault()
        }
        # separacion despues del cuadro
        Estilo $stNormal
        $sel.Font.Size = 4
        $sel.TypeParagraph()
        $sel.Font.Reset()
    }
    Add-Type -AssemblyName System.Drawing
    $tmpJpg = Join-Path ([IO.Path]::GetTempPath()) 'admind_manual_jpg'
    if (-not (Test-Path $tmpJpg)) { New-Item -ItemType Directory -Force $tmpJpg | Out-Null }
    $codecJpg = [System.Drawing.Imaging.ImageCodecInfo]::GetImageEncoders() | Where-Object { $_.MimeType -eq 'image/jpeg' }
    function EnJpeg([string]$origen) {
        $dest = Join-Path $tmpJpg (([IO.Path]::GetFileNameWithoutExtension($origen)) + '.jpg')
        $img = [System.Drawing.Image]::FromFile($origen)
        $ep = New-Object System.Drawing.Imaging.EncoderParameters 1
        $ep.Param[0] = New-Object System.Drawing.Imaging.EncoderParameter([System.Drawing.Imaging.Encoder]::Quality, [long]92)
        $img.Save($dest, $codecJpg, $ep)
        $img.Dispose()
        return $dest
    }
    function Figura($b) {
        $ruta = Join-Path $Capturas $b.file
        Estilo $stFigura
        if (Test-Path -LiteralPath $ruta) {
            $ruta = EnJpeg $ruta
            $ish = $sel.InlineShapes.AddPicture($ruta, $false, $true)
            $w = $ish.Width; $h = $ish.Height
            $maxW = $ANCHO; $maxH = 400
            if ($b.ancho) { $maxW = [double]$b.ancho * 28.35 }
            $k = [Math]::Min([Math]::Min($maxW / $w, $maxH / $h), 1.0)
            $ish.LockAspectRatio = -1
            $ish.Width = $w * $k
            $ish.AlternativeText = (Refs $b.pie)
            try { $ish.Line.Visible = -1; $ish.Line.ForeColor.RGB = (Rgb $GRIS200); $ish.Line.Weight = 0.75 } catch { }
            $null = $sel.EndKey(6)
        } else {
            [void]$faltan.Add($b.file)
            Escribir ('[Captura pendiente: ' + $b.file + ']')
        }
        $sel.TypeParagraph()
        Estilo $stPie
        Escribir ('Figura ' + $numFig[$b.id] + '. ' + $b.pie)
        $sel.TypeParagraph()
    }
    function Tabla($b) {
        $cols = @($b.cols); $filas = @($b.filas)
        $pesos = @($b.pesos)
        $suma = 0.0; foreach ($p in $pesos) { $suma += [double]$p }
        Estilo $stNormal
        $t = $doc.Tables.Add($sel.Range, $filas.Count + 1, $cols.Count)
        $t.AllowAutoFit = $false
        $t.Range.Style = $stTabla
        $t.Borders.InsideLineStyle = 1; $t.Borders.OutsideLineStyle = 1
        $t.Borders.InsideColor = (Rgb $GRIS200); $t.Borders.OutsideColor = (Rgb $GRIS200)
        $t.TopPadding = 2; $t.BottomPadding = 2; $t.LeftPadding = 5; $t.RightPadding = 5
        for ($c = 1; $c -le $cols.Count; $c++) {
            $t.Columns.Item($c).Width = $ANCHO * ([double]$pesos[$c - 1] / $suma)
            $t.Cell(1, $c).Range.Text = (Refs ([string]$cols[$c - 1]))
        }
        for ($r = 0; $r -lt $filas.Count; $r++) {
            $fila = @($filas[$r])
            for ($c = 0; $c -lt $cols.Count; $c++) {
                $t.Cell($r + 2, $c + 1).Range.Text = (Refs ([string]$fila[$c]))
                if ($c -eq 0 -and $b.primeraNegrita) { $t.Cell($r + 2, 1).Range.Font.Bold = 1 }
            }
            if ($r % 2 -eq 1) { $t.Rows.Item($r + 2).Shading.BackgroundPatternColor = (Rgb $VERDE50) }
        }
        $hr = $t.Rows.Item(1)
        $hr.Shading.BackgroundPatternColor = (Rgb $VERDE600)
        $hr.Range.Font.Color = (Rgb 'FFFFFF'); $hr.Range.Font.Bold = 1
        $hr.HeadingFormat = -1
        $t.Rows.AllowBreakAcrossPages = 0
        $null = $sel.EndKey(6)
        Estilo $stNormal
        $sel.Font.Size = 4
        $sel.TypeParagraph()
        $sel.Font.Reset()
    }

    # ---------- portada ----------
    $sel.HomeKey(6) | Out-Null
    Estilo $stCentro
    $sel.ParagraphFormat.SpaceBefore = 40
    $ish = $sel.InlineShapes.AddPicture($Logo, $false, $true)
    $ish.LockAspectRatio = -1; $ish.Width = 141.7
    $ish.AlternativeText = 'Logo de AdMind'
    $null = $sel.EndKey(6)
    $sel.TypeParagraph()
    Estilo $stCentro; $sel.ParagraphFormat.SpaceAfter = 8; $sel.TypeParagraph()

    Estilo $stBanda; $sel.Font.Size = 14; $sel.TypeText(' '); $sel.TypeParagraph()
    Estilo $stBanda; $sel.Font.Size = 36; $sel.TypeText($meta.portada.titulo); $sel.TypeParagraph()
    Estilo $stBanda; $sel.Font.Size = 16; $sel.Font.Bold = 0; $sel.TypeText($meta.portada.bajada); $sel.TypeParagraph()
    Estilo $stBanda; $sel.Font.Size = 14; $sel.TypeText(' '); $sel.TypeParagraph()

    Estilo $stCentro; $sel.ParagraphFormat.SpaceBefore = 26
    $sel.Font.Size = 15; $sel.Font.Color = (Rgb $VERDE700); $sel.Font.Bold = 1
    $sel.TypeText($meta.portada.subtitulo); $sel.TypeParagraph()
    Estilo $stCentro; $sel.ParagraphFormat.SpaceAfter = 10; $sel.TypeParagraph()

    foreach ($par in @($meta.portada.lineas)) {
        Estilo $stCentro
        $sel.Font.Size = 9; $sel.Font.Bold = 1; $sel.Font.Color = (Rgb $GRIS500)
        $sel.TypeText(([string]$par.etiqueta).ToUpper()); $sel.TypeParagraph()
        foreach ($v in @($par.valores)) {
            Estilo $stCentro
            $sel.Font.Size = 12.5; $sel.Font.Color = (Rgb $VERDE900)
            $sel.TypeText([string]$v); $sel.TypeParagraph()
        }
        Estilo $stCentro; $sel.ParagraphFormat.SpaceAfter = 10; $sel.Font.Size = 6; $sel.TypeParagraph()
    }

    # ---------- indice ----------
    Estilo $stIndice
    $sel.TypeText('Contenido'); $sel.TypeParagraph()
    Estilo $stNormal
    $null = $doc.TablesOfContents.Add($sel.Range, $true, 1, 2)
    $null = $sel.EndKey(6)

    # ---------- cuerpo ----------
    foreach ($b in $bloques) {
        switch ($b.t) {
            'h1' { Titulo -2 $b.texto }
            'h2' { Titulo -3 $b.texto }
            'h3' { Titulo -4 $b.texto }
            'p' { Parrafo $stNormal $b.texto }
            'ul' { Vinetas @($b.items) }
            'ol' { Pasos @($b.items) }
            'fig' { Figura $b }
            'nota' { Cuadro $stNota ([string]$b.titulo) ([string]$b.texto) $b.items }
            'aviso' { Cuadro $stAviso ([string]$b.titulo) ([string]$b.texto) $b.items }
            'tabla' { Tabla $b }
            default { throw ('Bloque desconocido: ' + $b.t) }
        }
    }

    # ---------- encabezado y pie (desde la pagina 2) ----------
    $secc = $doc.Sections.Item(1)
    $enc = $secc.Headers.Item(1)
    $enc.Range.Text = "`t" + $meta.encabezado
    $enc.Range.Font.Size = 9.5; $enc.Range.Font.Color = (Rgb $GRIS500)
    $enc.Range.ParagraphFormat.TabStops.ClearAll()
    $null = $enc.Range.ParagraphFormat.TabStops.Add($ANCHO, 2)
    $bh = $enc.Range.ParagraphFormat.Borders.Item(-3)
    $bh.LineStyle = 1; $bh.LineWidth = 6; $bh.Color = (Rgb $VERDE600)
    $enc.Range.ParagraphFormat.Borders.DistanceFromBottom = 4
    $rs = $enc.Range; $rs.Collapse(1)
    $lg = $rs.InlineShapes.AddPicture($Logo, $false, $true)
    $lg = $enc.Range.InlineShapes.Item(1)
    $lg.LockAspectRatio = -1
    $esc = [Math]::Round(28.35 / $lg.Height * 100, 1)
    $lg.ScaleHeight = $esc; $lg.ScaleWidth = $esc
    $lg.AlternativeText = 'Logo de AdMind'

    $pie = $secc.Footers.Item(1)
    $pie.Range.Text = [string]$meta.pie + "`tP" + [char]0x00E1 + "gina "
    $pie.Range.Font.Size = 9; $pie.Range.Font.Color = (Rgb $GRIS500)
    $pie.Range.ParagraphFormat.TabStops.ClearAll()
    $null = $pie.Range.ParagraphFormat.TabStops.Add($ANCHO, 2)
    $r1 = $pie.Range; $null = $r1.MoveEnd(1, -1); $r1.Collapse(0)
    $null = $doc.Fields.Add($r1, 33)
    $r2 = $pie.Range; $null = $r2.MoveEnd(1, -1); $r2.Collapse(0)
    $r2.InsertAfter(' de ')
    $r3 = $pie.Range; $null = $r3.MoveEnd(1, -1); $r3.Collapse(0)
    $null = $doc.Fields.Add($r3, 26)
    $pie.Range.Font.Size = 9; $pie.Range.Font.Color = (Rgb $GRIS500)

    # ---------- cierre ----------
    $doc.TablesOfContents.Item(1).Update()
    $est = $doc.TablesOfContents.Item(1).Range
    $doc.Fields.Update() | Out-Null
    $doc.TablesOfContents.Item(1).Update()

    $dir = Split-Path -Parent $Salida
    if (-not (Test-Path $dir)) { New-Item -ItemType Directory -Force $dir | Out-Null }
    $pdf = [IO.Path]::ChangeExtension($Salida, '.pdf')
    $doc.SaveAs([ref]$Salida, [ref]16)
    $doc.SaveAs([ref]$pdf, [ref]17)
    $paginas = $doc.ComputeStatistics(2)
    Write-Output ("Word: {0}" -f $Salida)
    Write-Output ("PDF:  {0}" -f $pdf)
    Write-Output ("Figuras numeradas: {0}; paginas: {1}" -f $totalFig, $paginas)
    if ($faltan.Count -gt 0) { Write-Output ("Capturas que faltan ({0}): {1}" -f $faltan.Count, ($faltan -join ', ')) }
}
catch {
    Write-Output ('ERROR en la linea ' + $_.InvocationInfo.ScriptLineNumber + ': ' + $_.InvocationInfo.Line.Trim())
    Write-Output ($_.Exception.Message)
    throw
}
finally {
    if ($doc -ne $null) { try { $doc.Close([ref]0) } catch { } }
    $word.Quit()
}
