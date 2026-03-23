$md = "C:\Users\Administrator\.openclaw\workspace\技术方案_深户团购.md"
$doc = "C:\Users\Administrator\Desktop\ceshi\深户社区公共广播系统技术方案.docx"
pandoc $md -o $doc
if (Test-Path $doc) {
    Write-Host "SUCCESS: $doc"
    Get-Item $doc | Select-Object Name, Length
}
