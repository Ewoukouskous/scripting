import time
import re
import sys
import os
import gzip

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

file_handle = None
is_gzip = False

try:
    file_handle = gzip.open(file_name, 'rt', encoding='utf-8', errors='ignore')
    file_handle.readline()
    file_handle.seek(0)
    is_gzip = True
except (gzip.BadGzipFile, OSError):
    pass

if not is_gzip:
    file_handle = open(file_name, 'r', encoding='utf-8', errors='ignore')

try:
    for line in file_handle:
        parts = re.split(r'\s(?=(?:[^"]*"[^"]*")*[^"]*$)', line)

        if len(parts) < 1:
            continue

        ip = parts[0]

        if ip in ips:
            ips[ip] += 1
        else:
            ips[ip] = 1
finally:
    if file_handle:
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