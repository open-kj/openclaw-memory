$ErrorActionPreference = 'Continue'
Start-Sleep -Seconds 300
$scriptPath = 'C:\Users\Administrator\AppData\Roaming\npm\node_modules\clawdhub\bin\clawdhub.js'
$output = & node $scriptPath install stock-price-query 2>&1 | Out-String
$output | Out-File -FilePath 'C:\Users\Administrator\.openclaw\workspace\tmp\install_result.txt' -Encoding UTF8
Write-Host "Done"