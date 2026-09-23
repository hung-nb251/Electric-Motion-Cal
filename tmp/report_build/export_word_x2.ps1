$ErrorActionPreference = 'Stop'
$taskRoot = (Resolve-Path -LiteralPath '.').Path
$docPath = Join-Path $taskRoot 'outputs\bao_cao_xe_con\Bao_cao_xe_con_x2_theo_mau.docx'
$pdfPath = Join-Path $taskRoot 'outputs\bao_cao_xe_con\Bao_cao_xe_con_x2_theo_mau.pdf'
$wordApp = New-Object -ComObject Word.Application
$wordApp.Visible = $false
$wordApp.DisplayAlerts = 0
try {
    $taskDoc = $wordApp.Documents.Open($docPath, $false, $true)
    $taskDoc.Repaginate()
    $taskDoc.ExportAsFixedFormat($pdfPath, 17)
    Write-Output ('Pages: ' + $taskDoc.ComputeStatistics(2))
    $taskDoc.Close(0)
} finally {
    $wordApp.Quit()
    [System.Runtime.InteropServices.Marshal]::ReleaseComObject($wordApp) | Out-Null
}

