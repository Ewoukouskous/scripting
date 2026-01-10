import gzip
import re
import sys
import os
import io

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

log_file = "../calt.log.gz"

traversal_patterns = [
    r"\.\./", r"\.\.%2f", r"%2e%2e%2f", r"\.\.%5c",
    r"/etc/passwd", r"windows/win\.ini", r"\.env",
    r"wp-config\.php", r"php://filter", r"/proc/self/environ"
]

regex_traversal = re.compile("|".join(traversal_patterns), re.IGNORECASE)

def analyze_traversal(file_path, full_logs=False):
    print(f"[DEBUG] Démarrage de l'analyse path traversal sur {file_path} (mode: {'all' if full_logs else 'success only'})")
    sys.stdout.flush()
    total_found = 0
    critical_hits = 0

    script_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    results_dir = os.path.join(script_root, 'results')
    if not os.path.exists(results_dir):
        os.makedirs(results_dir)

    output_file = os.path.join(results_dir, "path_traversal_logs.txt")

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
                    prefix = "[REUSSIE]" if is_success else "[SUSPECT/TENTATIVE]"

                    if is_success:
                        critical_hits += 1
                        print(f"{prefix:<20} | {timestamp:<22} | {ip:<15} | {status} | {size_str:<5} | {request}", file=out)
                    elif full_logs:
                        print(f"{prefix:<20} | {timestamp:<22} | {ip:<15} | {status} | {size_str:<5} | {request}", file=out)

        print(f"Analyse de path traversal terminée")
        sys.stdout.flush()
        print(f"Total de tentatives détectées : {total_found}")
        sys.stdout.flush()
        print(f"Accès réussis                 : {critical_hits}")
        sys.stdout.flush()
        output_path = os.path.abspath(output_file)
        print(f"Résultats sauvegardés dans : {output_path}")
        sys.stdout.flush()

    except FileNotFoundError:
        print(f"Erreur : Le fichier {file_path} est introuvable.")
        sys.stdout.flush()

if __name__ == "__main__":
    file_to_analyze = sys.argv[1] if len(sys.argv) > 1 else log_file
    full_logs_mode = sys.argv[2].lower() == 'all' if len(sys.argv) > 2 else False
    analyze_traversal(file_to_analyze, full_logs_mode)
