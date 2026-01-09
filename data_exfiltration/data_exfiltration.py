import gzip
import re

log_file = "../calt.log.gz"

LIMITE_EXFIL = 3000000

def analyze_exfiltration(file_path):
    total_suspicious = 0

    try:
        with gzip.open(file_path, 'rt', encoding='utf-8', errors='ignore') as f, \
                open("data_exfiltration_logs.txt", 'w', encoding='utf-8') as out:
            for line in f:
                parts = re.split(r'\s(?=(?:[^"]*"[^"]*")*[^"]*$)', line)

                if len(parts) < 8:
                    continue

                ip = parts[0]
                timestamp = parts[3].strip('[]')
                request = parts[5].strip('"')
                status = parts[6]
                size_str = parts[7]

                try:
                    size = int(size_str)
                except ValueError:
                    size = 0

                if status == '200' and size > LIMITE_EXFIL:
                    total_suspicious += 1
                    size_kb = round(size / 1024, 2)

                    print(f"[EXFIL] | {timestamp:<22} | {ip:<15} | {status} | {size_kb:<12} | {request}", file=out)
                else:
                    pass

        print(f"Analyse d'exfiltration terminée")
        print(f"Nombre de transferts lourds détectés (> {LIMITE_EXFIL / 1000000} Mo) : {total_suspicious}")

    except FileNotFoundError:
        print(f"Erreur : Le fichier {file_path} est introuvable.")

if __name__ == "__main__":
    analyze_exfiltration(log_file)