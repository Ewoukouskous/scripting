import time

file_name = 'full-logs.sorted.txt'
result = []

debut = time.perf_counter()

with open(file_name, 'r', encoding='utf-8') as file:
    for line in file:
        parts = line.split()

        clean_line = [
            parts[0],
            f"{parts[3]} {parts[4]}".strip('[]'),
            f"{parts[5]} {parts[6]} {parts[7]}".strip('"'),
            parts[8],
            parts[9],
            " ".join(parts[11:]).strip('"')
        ]

        if clean_line[3] == '404':
            result.append(clean_line)

fin = time.perf_counter()

for log_tab in result:
     print(log_tab)

duree = fin - debut
nombre_logs = len(result)

print("-" * 30)
print(f"Analyse terminée !")
print(f"Logs trouvés   : {nombre_logs}")
print(f"Temps écoulé   : {duree:.4f} secondes")
print("-" * 30)