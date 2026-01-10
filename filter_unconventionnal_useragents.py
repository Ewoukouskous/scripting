import time
import sys
import os
import gzip
import re
import io

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

file_name = sys.argv[1] if len(sys.argv) > 1 else 'full-logs.sorted.txt'
print("-" * 30)
print("What name do you want to give to your writed file ?")
file_to_write = input()
print("-" * 30)

script_dir = os.path.dirname(os.path.abspath(__file__))
results_dir = os.path.join(script_dir, 'results')
if not os.path.exists(results_dir):
    os.makedirs(results_dir)

output_file = os.path.join(results_dir, f"{file_to_write}.txt")

conventionnal_useragent = [
    "Safari",
    "Chrome",
    "Firefox",
    "Mozilla",
    "Edge",
    "Opera",
    "AppleWebKit",
    "Dart"
]

full_logs = False
print("Souhaitez vous l'intégralité des logs avec user agents non conventionnels ? (REPONSE SERVEUR POSITIVE et NEGATIVE) [o/N] :")
choice = input().strip().lower()
if choice == 'o':
    full_logs = True

debut = time.perf_counter()
nombre_logs = 0
nombre_logs_positif = 0

log_pattern = re.compile(r'(?P<ip>[\d\.]+) - - \[(?P<date>.*?)\] "(?P<request>.*?)" (?P<status>\d+) (?P<size>\d+|-) "(?P<referer>.*?)" "(?P<ua>.*?)"')

if file_name.endswith('.gz'):
    file_handle = gzip.open(file_name, 'rt', encoding='utf-8', errors='ignore')
else:
    file_handle = open(file_name, 'r', encoding='utf-8', errors='ignore')

with file_handle, open(output_file, 'w', encoding='utf-8') as out:
    for line in file_handle:
        match = log_pattern.match(line)
        if match:
            parts = match.groupdict()

            ip = parts['ip']
            timestamp = parts['date']
            request = parts['request']
            status = parts['status']
            size_str = parts['size']
            log_useragent = parts['ua']

            if not any(useragent.lower() in log_useragent.lower() for useragent in conventionnal_useragent):
                if status.startswith('2') or status in ['301', '302']:
                    nombre_logs += 1
                    nombre_logs_positif += 1
                    print(f"{"[REPONSE SERVEUR POSITIVE]":<30} | {timestamp:<22} | {ip:<15} | {status} | {size_str:<5} | {request} | {log_useragent}", file=out)
                elif full_logs and status.startswith('4'):
                    nombre_logs += 1
                    print(f"{"[REPONSE SERVEUR NEGATIVE]":<30} | {timestamp:<22} | {ip:<15} | {status} | {size_str:<5} | {request} | {log_useragent}", file=out)


fin = time.perf_counter()

duree = fin - debut

print("-" * 30)
print(f"Formatage terminé !")
print(f"Logs écrit   : {nombre_logs}")
print(f"Logs positifs: {nombre_logs_positif}")
print(f"Temps écoulé   : {duree:.4f} secondes")
print(f"Résultats sauvegardés dans : {os.path.abspath(output_file)}")
print("-" * 30)
sys.stdout.flush()
