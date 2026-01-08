import gzip
import re

log_file = "full-logs.sorted.txt.gz"

SEUIL_EXFILTRATION = 1000000

def analyze_exfiltration(file_path):
    total_suspicious = 0

    try:
        with gzip.open(file_path, 'rt', encoding='utf-8', errors='ignore') as f:
            for line in f:
                parts = re.split(r'\s(?=(?:[^"]*"[^"]*")*[^"]*$)', line)

                if len(parts) < 8:
                    continue

                ip = parts[0]
                request = parts[5].strip('"')
                status = parts[6]
                size_str = parts[7]

                try:
                    size = int(size_str)
                except ValueError:
                    size = 0

                if status == '200' and size > SEUIL_EXFILTRATION:
                    total_suspicious += 1
                    size_kb = round(size / 1024, 2)

                    print(f"\033[92m[EXFIL]      | {ip:<15} | {size_kb:<12} | {request}\033[0m")
                else:
                    pass

        print("-" * 110)
        print(f"ANALYSE D'EXFILTRATION TERMINÉE")
        print(f"Nombre de transferts volumineux détectés (> {SEUIL_EXFILTRATION / 1000000} Mo) : {total_suspicious}")

    except FileNotFoundError:
        print(f"Erreur : Le fichier {file_path} est introuvable.")

if __name__ == "__main__":
    analyze_exfiltration(log_file)