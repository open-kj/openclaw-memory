import subprocess
import sys
import os

# Check if Chrome is running with remote debugging port
result = subprocess.run(['powershell', '-Command', 
    'Get-Process chrome -ErrorAction SilentlyContinue | Select-Object Id, ProcessName, StartTime'],
    capture_output=True, text=True)
print("Chrome processes:")
print(result.stdout)
print(result.stderr)

# Try to find chrome with debugging port
result2 = subprocess.run(['powershell', '-Command',
    'netstat -ano | Select-String "127.0.0.1:9222"'],
    capture_output=True, text=True)
print("\nRemote debugging port 9222:")
print(result2.stdout)
print(result2.stderr)
