Start-Sleep -Seconds 300
$ErrorActionPreference = 'Stop'
try {
    $output = & node 'C:\Users\Administrator\AppData\Roaming\npm\node_modules\clawdhub\bin\clawdhub.js' install stock-price-query 2>&1
    $result = "SUCCESS: $output"
} catch {
    $result = "ERROR: $($_.Exception.Message)"
}
$result | Out-File -FilePath 'C:\Users\Administrator\.openclaw\workspace\tmp\result.txt' -Encoding UTF8