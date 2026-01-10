import gzip
import re
import sys
import os

log_file = "../calt.log.gz"

traversal_patterns = [
    r"\.\./", r"\.\.%2f", r"%2e%2e%2f", r"\.\.%5c",
    r"/etc/passwd", r"windows/win\.ini", r"\.env",
    r"wp-config\.php", r"php://filter", r"/proc/self/environ"
]

regex_traversal = re.compile("|".join(traversal_patterns), re.IGNORECASE)

def analyze_traversal(file_path):
    total_found = 0
    critical_hits = 0
    output_file = "path_traversal_logs.txt"

    try:
        with gzip.open(file_path, 'rt', encoding='utf-8', errors='ignore') as f, \
                open(output_file, 'w', encoding='utf-8') as out:
            for line in f:
                parts = re.split(r'\s(?=(?:[^"]*"[^"]*")*[^"]*$)', line)
                if len(parts) < 7:
                    continue

                ip = parts[0]
                timestamp = parts[3].strip('[]')
                request = parts[5].strip('"')
                status = parts[6]
                size_str = parts[7]

                if regex_traversal.search(request):
                    total_found += 1
                    is_success = status.startswith('2')

                    if is_success:
                        critical_hits += 1
                        print(f"[CRITIQUE]   | {timestamp:<22} | {ip:<15} | {status} | {size_str:<5} | {request}", file=out)
                    else:
                        print(f"[TENTATIVE]  | {timestamp:<22} | {ip:<15} | {status} | {size_str:<5} | {request}", file=out)

        print(f"Analyse de path traversal terminée")
        print(f"Total de tentatives détectées : {total_found}")
        print(f"Accès réussis                 : {critical_hits}")
        output_path = os.path.abspath(output_file)
        print(f"Résultats sauvegardés dans : {output_path}")

    except FileNotFoundError:
        print(f"Erreur : Le fichier {file_path} est introuvable.")

if __name__ == "__main__":
    file_to_analyze = sys.argv[1] if len(sys.argv) > 1 else log_file
    analyze_traversal(file_to_analyze)
