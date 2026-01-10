import time
import sys
import os
import gzip

file_name = sys.argv[1] if len(sys.argv) > 1 else 'full-logs.sorted.txt'
result = []
print("-" * 30)
print("What IP address do you want to filter by ?")
ip_to_filter = input()
print("-" * 30)

file_to_write = ip_to_filter.replace('.', '_')

script_dir = os.path.dirname(os.path.abspath(__file__))
results_dir = os.path.join(script_dir, 'results')
if not os.path.exists(results_dir):
    os.makedirs(results_dir)

output_file = os.path.join(results_dir, f"{file_to_write}.txt")

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
        parts = line.split()

        if len(parts) < 12:
            continue

        clean_line = [
            parts[0],
            f"{parts[3]} {parts[4]}".strip('[]'),
            f"{parts[5]} {parts[6]} {parts[7]}".strip('"'),
            parts[8],
            parts[9],
            " ".join(parts[11:]).strip('"')
        ]
        if clean_line[0] == ip_to_filter:
            result.append(clean_line)
finally:
    if file_handle:
        file_handle.close()


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