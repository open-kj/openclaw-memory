$skills = @(
    "mx-finance-search",
    "mx-stocks-screener",
    "polymarket-trade",
    "finance-report-analyzer",
    "finance-radar"
)

$results = @()

foreach ($skill in $skills) {
    $attempt = 0
    $success = $false
    while (-not $success -and $attempt -lt 10) {
        $attempt++
        Write-Host "[$(Get-Date -Format 'HH:mm:ss')] Attempting to install: $skill (attempt $attempt)"
        $output = npx clawdhub install $skill 2>&1
        $exitCode = $LASTEXITCODE
        Write-Host $output
        
        if ($exitCode -eq 0) {
            $results += "$skill : SUCCESS"
            $success = $true
        } elseif ($output -match "Rate limit exceeded" -or $output -match "rate.limit") {
            Write-Host "[$(Get-Date -Format 'HH:mm:ss')] Rate limited. Waiting 180 seconds..."
            Start-Sleep -Seconds 180
        } else {
            $results += "$skill : FAILED (exit $exitCode)"
            break
        }
    }
    if (-not $success -and $attempt -ge 10) {
        $results += "$skill : ABANDONED after $attempt attempts"
    }
}

Write-Host ""
Write-Host "=== RESULTS ==="
foreach ($r in $results) {
    Write-Host $r
}
