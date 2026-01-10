import time
import re
import sys
import os
import gzip
import io

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

file_name = sys.argv[1] if len(sys.argv) > 1 else 'calt.log'
result = []
print("-" * 30)
print("What name do you want to give to your writed file ?")
file_to_write = input()
print("-" * 30)

script_dir = os.path.dirname(os.path.abspath(__file__))
results_dir = os.path.join(script_dir, 'results')
if not os.path.exists(results_dir):
    os.makedirs(results_dir)

output_file = os.path.join(results_dir, f"{file_to_write}.txt")

ips = {}

debut = time.perf_counter()

log_pattern = re.compile(
    r'(?P<ip>[\d\.]+) - - \[(?P<date>.*?)\] "(?P<request>.*?)" (?P<status>\d+) (?P<size>\d+|-) "(?P<referer>.*?)" "(?P<ua>.*?)"')

if file_name.endswith('.gz'):
    file_handle = gzip.open(file_name, 'rt', encoding='utf-8', errors='ignore')
else:
    file_handle = open(file_name, 'r', encoding='utf-8', errors='ignore')

try:
    for line in file_handle:
        match = log_pattern.match(line)
        if match:
            parts = match.groupdict()
            ip = parts['ip']

            if ip in ips:
                ips[ip] += 1
            else:
                ips[ip] = 1
finally:
    file_handle.close()

for ip, count in ips.items():
    if count > 2 :
        result.append((ip, count))

result.sort(key=lambda x: x[1], reverse=True)


with open(output_file, 'w', encoding='utf-8') as file:
    for line in result:
        file.write(str(line) + '\n')

fin = time.perf_counter()

duree = fin - debut
nombre_logs = len(result)

print("-" * 30)
print(f"Formatage terminé !")
print(f"Logs écrit   : {nombre_logs}")
print(f"Temps écoulé   : {duree:.4f} secondes")
print(f"Résultats sauvegardés dans : {os.path.abspath(output_file)}")
print("-" * 30)