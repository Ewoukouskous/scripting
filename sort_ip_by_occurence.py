import time

file_name = 'full-logs.sorted.txt'
result = []
print("-" * 30)
print("What name do you want to give to your writed file ?")
file_to_write = input()
print("-" * 30)

ips = {}

debut = time.perf_counter()

with open(file_name, 'r', encoding='utf-8') as file:
    for line in file:
        parts = line.split()

        # Clean line exemple :
        # Ip address [0], Date and time [1], Request [2], Status code [3], Size [4], User agent [5]
        clean_line = [
            parts[0],
            f"{parts[3]} {parts[4]}".strip('[]'),
            f"{parts[5]} {parts[6]} {parts[7]}".strip('"'),
            parts[8],
            parts[9],
            " ".join(parts[11:]).strip('"')
        ]

        ip = clean_line[0]
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