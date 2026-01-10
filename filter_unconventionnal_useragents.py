import time
import sys
import os
import gzip
import re

file_name = sys.argv[1] if len(sys.argv) > 1 else 'full-logs.sorted.txt'
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
    output_file = 'unconventional_userAgents_all_logs.txt'

debut = time.perf_counter()
nombre_logs = 0
nombre_logs_positif = 0

with open(file_name, 'r', encoding='utf-8') as file, \
        open(output_file, 'w', encoding='utf-8') as out:
    for line in file:
        log_pattern = re.compile(r'(?P<ip>[\d\.]+) - - \[(?P<date>.*?)\] "(?P<request>.*?)" (?P<status>\d+) (?P<size>\d+|-) "(?P<referer>.*?)" "(?P<ua>.*?)"')
        match = log_pattern.match(line)
        if match :
            parts = match.groupdict()
            # Clean line exemple :
            # Ip address, Date and time, Request, Status code, Size, User agent

            ip = parts['ip']
            timestamp = parts['date']
            request = parts['request']
            status = parts['status']
            size_str = parts['size']
            referer = parts['referer']
            log_useragent = parts['ua']

            # If user agent is not conventionnal and status code is 2xx, 301 or 302
            if not any(useragent.lower() in log_useragent.lower() for useragent in conventionnal_useragent):
                if status.startswith('2') or status in ['301', '302']:
                    nombre_logs += 1
                    nombre_logs_positif += 1
                    print(f"{"[REPONSE SERVEUR POSITIVE]":<20} | {timestamp:<22} | {ip:<15} | {status} | {size_str:<5} | {request} | {log_useragent}", file=out)
                # If the user agent is not conventionnal but the status code is 4xx
                if full_logs:
                    if status.startswith('4'):
                        nombre_logs += 1
                        print(f"{"[REPONSE SERVEUR NEGATIVE]":<20} | {timestamp:<22} | {ip:<15} | {status} | {size_str:<5} | {request} | {log_useragent}", file=out)


fin = time.perf_counter()

duree = fin - debut
nombre_logs = len(result)

print("-" * 30)
print(f"Formatage terminé !")
print(f"Logs écrit   : {nombre_logs}")
print(f"Logs positifs: {nombre_logs_positif}")
print(f"Temps écoulé   : {duree:.4f} secondes")
print(f"Résultats sauvegardés dans : {os.path.abspath(output_file)}")
print("-" * 30)