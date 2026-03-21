@echo off
cd /d C:\Users\Administrator\AppData\Roaming\npm
echo Starting install > C:\Users\Administrator\.openclaw\workspace\tmp\log.txt
node node_modules\clawdhub\bin\clawdhub.js install stock-price-query >> C:\Users\Administrator\.openclaw\workspace\tmp\log.txt 2>&1
echo Done >> C:\Users\Administrator\.openclaw\workspace\tmp\log.txt
echo EXIT_CODE=%ERRORLEVEL% >> C:\Users\Administrator\.openclaw\workspace\tmp\log.txt