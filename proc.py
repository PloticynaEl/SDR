import subprocess

proc = subprocess.Popen('sleep 50', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
for line in proc.stdout:
 print(line, end='', flush=True)