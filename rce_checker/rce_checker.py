import gzip
import re
import sys
import os

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

def analyze_rce(file_path):
    success_count = 0
    total_rce = 0
    output_file = "rce_detector_logs.txt"

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

                if regex_rce.search(request):
                    total_rce += 1

                    is_success = status.startswith('2')
                    prefix = "[SUCCESS]" if is_success else "[ATTEMPT]"

                    if is_success:
                        success_count += 1
                        print(f"{prefix:<12} | {timestamp:<22} | {ip:<15} | {status} | {size_str:<5} | {request}", file=out)
                    else:
                        pass

        print(f"Analyse d'attaque rce terminée")
        print(f"Total de tentatives RCE détectées : {total_rce}")
        print(f"Tentatives réussies               : {success_count}")
        output_path = os.path.abspath(output_file)
        print(f"Résultats sauvegardés dans : {output_path}")

    except FileNotFoundError:
        print(f"Erreur : Le fichier {file_path} est introuvable.")

if __name__ == "__main__":
    file_to_analyze = sys.argv[1] if len(sys.argv) > 1 else log_file
    analyze_rce(file_to_analyze)
