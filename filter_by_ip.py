import time
import re

file_name = 'calt.log'
number_logs = 0
print("-" * 30)
print("Sur qu'elle IP souhaites-tu filtrer ?")
ip_to_filter = input()
print("-" * 30)

output_file = ip_to_filter.replace('.', '_')+".txt"

start = time.perf_counter()

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
                number_logs += 1
                print(f"{timestamp:<22} | {ip:<15} | {status} | {size_str:<5} | {request} | {log_useragent}", file=out)


end = time.perf_counter()

duration = end - start

print("-" * 30)
print(f"Formatage terminé !")
print(f"Logs écrit   : {number_logs}")
print(f"Temps écoulé   : {duration:.4f} secondes")
print("-" * 30)