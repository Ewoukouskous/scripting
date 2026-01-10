import gzip
import re
import sys
import os
import io

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

log_file = "../calt.log.gz"

# Common rce attacks
rce_patterns = [
    r"wget", r"curl", r"chmod\+777", r"rm\+-rf", r"sh\+",
    r"eval-stdin\.php",
    r"invokefunction", r"call_user_func_array", r"die\(@md5",
    r"shell\?cd", r"/bin/sh", r"whoami",
    r"&&", r"\|", r";", r"`"
]

regex_rce = re.compile("|".join(rce_patterns), re.IGNORECASE)

def analyze_rce(file_path, full_logs=False):
    success_count = 0
    total_rce = 0

    script_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    results_dir = os.path.join(script_root, 'results')
    if not os.path.exists(results_dir):
        os.makedirs(results_dir)

    output_file = os.path.join(results_dir, "rce_detector_logs.txt")

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
                status = parts[6]
                size_str = parts[7]

                if regex_rce.search(request):
                    total_rce += 1

                    is_success = status.startswith('2')
                    prefix = "[REUSSIE]" if is_success else "[SUSPECT/TENTATIVE]"

                    if is_success:
                        success_count += 1
                        print(f"{prefix:<20} | {timestamp:<22} | {ip:<15} | {status} | {size_str:<5} | {request}", file=out)
                    elif full_logs:
                        print(f"{prefix:<20} | {timestamp:<22} | {ip:<15} | {status} | {size_str:<5} | {request}", file=out)

        print(f"Analyse d'attaque rce terminée")
        sys.stdout.flush()
        print(f"Total de tentatives RCE détectées : {total_rce}")
        sys.stdout.flush()
        print(f"Tentatives réussies               : {success_count}")
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
    analyze_rce(file_to_analyze, full_logs_mode)
