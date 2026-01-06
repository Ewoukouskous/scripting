import time

file_name = 'full-logs.sorted.txt'
result = []
print("-" * 30)
print("What name do you want to give to your writed file ?")
file_to_write = input()
print("-" * 30)

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
        result.append(clean_line)

with open(file_to_write, 'w', encoding='utf-8') as file:
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