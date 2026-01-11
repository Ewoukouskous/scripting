import gzip
import re
import sys
import os
import io

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

log_file = "../calt.log.gz"
SEUIL_ALERTE = 5

pending_sequences = {}

# Common login page name
LOGIN_PAGES = r"login|admin|manager|wp-login|author|formLogin|config"

def analyze_bruteforce(file_path):
    total_alerts = 0

    script_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    results_dir = os.path.join(script_root, 'results')
    if not os.path.exists(results_dir):
        os.makedirs(results_dir)

    output_file = os.path.join(results_dir, "bruteforce_logs.txt")

    try:
        if file_path.endswith('.gz'):
            f = gzip.open(file_path, 'rt', encoding='utf-8', errors='ignore')
        else:
            f = open(file_path, 'r', encoding='utf-8', errors='ignore')

        with f, open(output_file, 'w', encoding='utf-8') as out:
            for line in f:
                parts = re.split(r'\s(?=(?:[^"]*"[^"]*")*[^"]*$)', line)
                if len(parts) < 7:
                    continue

                ip = parts[0]
                timestamp = parts[3].strip('[]')
                request = parts[5].strip('"')
                size_str = parts[7]

                status_match = re.search(r'\s(\d{3})\s', line)
                if not status_match:
                    continue
                status = status_match.group(1)

                if re.search(LOGIN_PAGES, request, re.IGNORECASE):

                    if status in ['401', '403', '404', '400']:
                        if ip not in pending_sequences:
                            pending_sequences[ip] = []
                        pending_sequences[ip].append(request)

                    elif status == '200':
                        if ip in pending_sequences and len(pending_sequences[ip]) >= SEUIL_ALERTE:
                            total_alerts += 1
                            print(f"{ip:<15} | {timestamp} | {size_str:<5}  | Succès sur : {request}", file=out)
                            print(f"Tentatives ratés juste avant : {len(pending_sequences[ip])}", file=out)

                            del pending_sequences[ip]

        print(f"Analyse bruteforce terminée. Total détecté : {total_alerts}")
        sys.stdout.flush()
        output_path = os.path.abspath(output_file)
        print(f"Résultats sauvegardés dans : {output_path}")
        sys.stdout.flush()

    except FileNotFoundError:
        print(f"Erreur : Le fichier {file_path} est introuvable.")
        sys.stdout.flush()

if __name__ == "__main__":
    file_to_analyze = sys.argv[1] if len(sys.argv) > 1 else log_file
    analyze_bruteforce(file_to_analyze)
