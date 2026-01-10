import time
import sys
import os
import gzip
import re
import io

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

file_name = sys.argv[1] if len(sys.argv) > 1 else 'calt.log'
print("-" * 30)
print("Sur qu'elle IP souhaites-tu filtrer ?")
ip_to_filter = input()
print("-" * 30)

file_to_write = ip_to_filter.replace('.', '_')

script_dir = os.path.dirname(os.path.abspath(__file__))
results_dir = os.path.join(script_dir, 'results')
if not os.path.exists(results_dir):
    os.makedirs(results_dir)

start = time.perf_counter()
output_file = os.path.join(results_dir, f"{file_to_write}.txt")
number_logs = 0


log_pattern = re.compile(
    r'(?P<ip>[\d\.]+) - - \[(?P<date>.*?)\] "(?P<request>.*?)" (?P<status>\d+) (?P<size>\d+|-) "(?P<referer>.*?)" "(?P<ua>.*?)"')

if file_name.endswith('.gz'):
    file_handle = gzip.open(file_name, 'rt', encoding='utf-8', errors='ignore')
else:
    file_handle = open(file_name, 'r', encoding='utf-8', errors='ignore')

with file_handle, open(output_file, 'w', encoding='utf-8') as out:
    for line in file_handle:
        match = log_pattern.match(line)
        if match:
            parts = match.groupdict()
            # Clean line exemple :
            # Ip address, Date and time, Request, Status code, Size, User agent

            ip = parts['ip']

            if ip == ip_to_filter:
                timestamp = parts['date']
                request = parts['request']
                status = parts['status']
                size_str = parts['size']
                log_useragent = parts['ua']

                number_logs += 1
                print(f"{timestamp:<22} | {ip:<15} | {status} | {size_str:<5} | {request} | {log_useragent}", file=out)


end = time.perf_counter()

duration = end - start

print("-" * 30)
print(f"Formatage terminé !")
print(f"Logs écrit   : {number_logs}")
print(f"Temps écoulé   : {duration:.4f} secondes")
print(f"Résultats sauvegardés dans : {os.path.abspath(output_file)}")
print("-" * 30)
sys.stdout.flush()
