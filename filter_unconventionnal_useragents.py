import time
import sys

file_name = sys.argv[1] if len(sys.argv) > 1 else 'full-logs.sorted.txt'
result = []
print("-" * 30)
print("What name do you want to give to your writed file ?")
file_to_write = input()
print("-" * 30)


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
        if not any(useragent.lower() in clean_line[5].lower() for useragent in conventionnal_useragent):
            result.append(clean_line)

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