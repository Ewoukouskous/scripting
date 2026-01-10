import time
import re
import sys

file_name = sys.argv[1] if len(sys.argv) > 1 else 'calt.log'
result = []
print("-" * 30)
print("What name do you want to give to your writed file ?")
file_to_write = input()
print("-" * 30)

ips = {}

debut = time.perf_counter()

with open(file_name, 'r', encoding='utf-8') as file:
    for line in file:
        parts = re.split(r'\s(?=(?:[^"]*"[^"]*")*[^"]*$)', line)

        # Clean line exemple :
        # Ip address [0], Date and time [1], Request [2], Status code [3], Size [4], User agent [5]
        ip = parts[0]
        date = parts[1]
        request = parts[2]
        status_code = parts[3]
        size = parts[4]
        user_agent = " ".join(parts[5:])

        clean_line = [
            ip,
            date,
            request,
            status_code,
            size,
            user_agent
        ]

        if ip in ips:
            ips[ip] += 1
        else:
            ips[ip] = 1

for ip, count in ips.items():
    if count > 2 :
        result.append((ip, count))

result.sort(key=lambda x: x[1], reverse=True)


with open(file_to_write+".txt", 'w', encoding='utf-8') as file:
    for line in result:
        file.write(str(line) + '\n')

fin = time.perf_counter()

duree = fin - debut
nombre_logs = len(result)

print("-" * 30)
print(f"Formatage terminé !")
print(f"Logs écrit   : {nombre_logs}")
print(f"Temps écoulé   : {duree:.4f} secondes")
print("-" * 30)