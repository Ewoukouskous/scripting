import gzip
import re
import urllib.parse
import sys
import os
import io

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

log_file = "../calt.log.gz"

xss_patterns = [
    r"<script", r"iframe", r"onload", r"onerror", r"alert\(",
    r"document\.cookie", r"javascript:", r"String\.fromCharCode"
]
regex_xss = re.compile("|".join(xss_patterns), re.IGNORECASE)

def analyze_xss(file_path):
    print(f"[DEBUG] Démarrage de l'analyse XSS sur {file_path}")
    sys.stdout.flush()
    success_count = 0
    total_xss = 0

    script_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    results_dir = os.path.join(script_root, 'results')
    if not os.path.exists(results_dir):
        os.makedirs(results_dir)

    output_file = os.path.join(results_dir, "xss_detector_logs.txt")

    print(f"[DEBUG] Ouverture du fichier {file_path}")
    sys.stdout.flush()

    try:
        with gzip.open(file_path, 'rt', encoding='utf-8', errors='ignore') as f, \
                open(output_file, 'w', encoding='utf-8') as out:
            for line in f:
                parts = line.split()
                if len(parts) < 9: continue

                ip = parts[0]
                timestamp = parts[3].strip('[]')
                size_str = parts[7]

                raw_request = " ".join(parts[5:8])
                request = urllib.parse.unquote(raw_request)

                status = parts[8] if len(parts) > 8 else "???"

                if regex_xss.search(request):
                    total_xss += 1
                    is_success = status.startswith('2')
                    tag = "[SUCCESS]" if is_success else "[ATTEMPT]"
                    if is_success: success_count += 1

                    print(f"{tag:<12} | {timestamp:<22} | {ip:<15} | {status} | {size_str:<5} | {request}", file=out)

        print(f"Total de faille xss détectée : {total_xss} | faille réussies : {success_count}")
        sys.stdout.flush()
        output_path = os.path.abspath(output_file)
        print(f"Résultats sauvegardés dans : {output_path}")
        sys.stdout.flush()

    except FileNotFoundError:
        print(f"Fichier non trouvé : {file_path}")
        sys.stdout.flush()

if __name__ == "__main__":
    file_to_analyze = sys.argv[1] if len(sys.argv) > 1 else log_file
    analyze_xss(file_to_analyze)
