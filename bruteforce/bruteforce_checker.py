import gzip
import re

log_file = "../calt.log.gz"
SEUIL_ALERTE = 5

pending_sequences = {}

# Common login page name
LOGIN_PAGES = r"login|admin|manager|wp-login|author|formLogin|config"

def analyze_bruteforce(file_path):
    total_alerts = 0

    try:
        with gzip.open(file_path, 'rt', encoding='utf-8', errors='ignore') as f, \
                open("bruteforce_logs.txt", 'w', encoding='utf-8') as out:
            for line in f:
                parts = re.split(r'\s(?=(?:[^"]*"[^"]*")*[^"]*$)', line)
                if len(parts) < 7:
                    continue

                ip = parts[0]
                timestamp = parts[3].strip('[]')
                request = parts[5].strip('"')

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
                            print(f"{ip:<15} | {timestamp} | Succès sur : {request}", file=out)
                            print(f"Tentatives infructueuses juste avant : {len(pending_sequences[ip])}", file=out)

                            del pending_sequences[ip]

        print(f"{'=' * 100}")
        print(f"ANALYSE TERMINÉE. Total détecté : {total_alerts}")

    except FileNotFoundError:
        print(f"Erreur : Le fichier {file_path} est introuvable.")

if __name__ == "__main__":
    analyze_bruteforce(log_file)