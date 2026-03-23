import subprocess
result = subprocess.run(['pip', 'install', 'playwright', '-q'], capture_output=True, text=True)
print(result.stdout)
print(result.stderr)
