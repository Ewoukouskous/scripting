import time
import re

file_name = 'calt.log'
output_file = 'unconventional_userAgents_positive_logs.txt'

conventional_useragent = [
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

start = time.perf_counter()
number_logs = 0
number_positive_logs = 0

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

            # If user agent is not conventional and status code is 2xx, 301 or 302
            if not any(useragent.lower() in log_useragent.lower() for useragent in conventional_useragent):
                if status.startswith('2') or status in ['301', '302']:
                    number_logs += 1
                    number_positive_logs += 1
                    print(f"{"[REPONSE SERVEUR POSITIVE]":<20} | {timestamp:<22} | {ip:<15} | {status} | {size_str:<5} | {request} | {log_useragent}", file=out)
                # If the user agent is not conventional but the status code is 4xx
                if full_logs:
                    if status.startswith('4'):
                        number_logs += 1
                        print(f"{"[REPONSE SERVEUR NEGATIVE]":<20} | {timestamp:<22} | {ip:<15} | {status} | {size_str:<5} | {request} | {log_useragent}", file=out)


end = time.perf_counter()

duration = end - start

print("-" * 30)
print(f"Formatage terminé !")
print(f"Logs écrit   : {number_logs}")
print(f"Logs positifs: {number_positive_logs}")
print(f"Temps écoulé   : {duration:.4f} secondes")
print("-" * 30)