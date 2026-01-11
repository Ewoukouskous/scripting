import gzip
import re
import sys
import os
import io

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

log_file = "../calt.log.gz"


def analyze_exfiltration(file_path, limite_exfil=None):
    if limite_exfil is None:
        limite_exfil = 3000000

    threshold_label = f"{limite_exfil / 1000000} Mo"

    print(f"\n[*] Analyse avec seuil : {threshold_label}")
    sys.stdout.flush()

    total_suspicious = 0

    script_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    results_dir = os.path.join(script_root, 'results')
    if not os.path.exists(results_dir):
        os.makedirs(results_dir)

    output_file = os.path.join(results_dir, "data_exfiltration_logs.txt")

    try:
        if file_path.endswith('.gz'):
            f = gzip.open(file_path, 'rt', encoding='utf-8', errors='ignore')
        else:
            f = open(file_path, 'r', encoding='utf-8', errors='ignore')

        with f, open(output_file, 'w', encoding='utf-8') as out:
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

                if status == '200' and size > limite_exfil:
                    total_suspicious += 1
                    size_kb = round(size / 1024, 2)

                    print(f"[EXFIL] | {timestamp:<22} | {ip:<15} | {status} | {size_kb:<12} | {request}", file=out)

        print(f"Analyse d'exfiltration terminée")
        sys.stdout.flush()
        print(f"Nombre de transferts lourds détectés (> {threshold_label}) : {total_suspicious}")
        sys.stdout.flush()
        output_path = os.path.abspath(output_file)
        print(f"Résultats sauvegardés dans : {output_path}")
        sys.stdout.flush()

    except FileNotFoundError:
        print(f"Erreur : Le fichier {file_path} est introuvable.")
        sys.stdout.flush()

if __name__ == "__main__":
    file_to_analyze = sys.argv[1] if len(sys.argv) > 1 else log_file
    threshold = int(sys.argv[2]) if len(sys.argv) > 2 else None
    analyze_exfiltration(file_to_analyze, threshold)
