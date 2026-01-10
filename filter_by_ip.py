import time
import sys
import os
import gzip
import re

file_name = sys.argv[1] if len(sys.argv) > 1 else 'full-logs.sorted.txt'
result = []
print("-" * 30)
print("What IP address do you want to filter by ?")
ip_to_filter = input()
print("-" * 30)

output_file = ip_to_filter.replace('.', '_')+".txt"

script_dir = os.path.dirname(os.path.abspath(__file__))
results_dir = os.path.join(script_dir, 'results')
if not os.path.exists(results_dir):
    os.makedirs(results_dir)

output_file = os.path.join(results_dir, f"{file_to_write}.txt")

debut = time.perf_counter()

with open(file_name, 'r', encoding='utf-8') as file, \
        open(output_file, 'w', encoding='utf-8') as out:
    for line in file:
        log_pattern = re.compile(
            r'(?P<ip>[\d\.]+) - - \[(?P<date>.*?)\] "(?P<request>.*?)" (?P<status>\d+) (?P<size>\d+|-) "(?P<referer>.*?)" "(?P<ua>.*?)"')
        match = log_pattern.match(line)
        if match:
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

            if ip == ip_to_filter:
                nombre_logs += 1
                print(f"{timestamp:<22} | {ip:<15} | {status} | {size_str:<5} | {request} | {log_useragent}", file=out)


fin = time.perf_counter()

duree = fin - debut
nombre_logs = len(result)

print("-" * 30)
print(f"Formatage terminé !")
print(f"Logs écrit   : {nombre_logs}")
print(f"Temps écoulé   : {duree:.4f} secondes")
print(f"Résultats sauvegardés dans : {os.path.abspath(output_file)}")
print("-" * 30)