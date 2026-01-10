import gzip
import re
import sys
import os

log_file = "../calt.log.gz"

# Common SQLi patterns
sqli_patterns = [
    r"(?<!\S)UNION", r"(?<!\S)SELECT", r"(?<!\S)INSERT", r"(?<!\S)UPDATE", r"(?<!\S)DELETE", r"(?<!\S)DROP",
    r"(?<!\S)ORDER BY", r"(?<!\S)GROUP BY", r"(?<!\S)SLEEP\(", r"BENCHMARK\(",
    r"OR 1=1", r"AND 1=1", r"'", r"\"", r"--", r"(?<!\S)WAITFOR DELAY"
]

exclusions = [
    r"\.(?:css|js|png|jpg|jpeg|gif|ico|woff|ttf)(?:\?|$)",
    r"application/json",
]

regex_sqli = re.compile("|".join(sqli_patterns), re.IGNORECASE)
regex_exclusions = re.compile("|".join(exclusions), re.IGNORECASE)

def analyze_logs(file_path):
    success_count = 0
    total_sqli = 0
    output_file = "sql_attack_logs.txt"

    try:
        with gzip.open(file_path, 'rt', encoding='utf-8', errors='ignore') as f, \
                open(output_file, 'w', encoding='utf-8') as out:
            for line in f:
                parts = re.split(r'\s(?=(?:[^"]*"[^"]*")*[^"]*$)', line)

                if len(parts) < 9:
                    continue

                ip = parts[0]
                timestamp = parts[3].strip('[]')
                request = parts[5].strip('"')
                status = parts[6]
                size_str = parts[7]

                if regex_sqli.search(request) and "?" in request:
                    if regex_exclusions.search(request):
                        continue
                    total_sqli += 1

                    is_success = status.startswith('2')
                    prefix = "[SUCCESS]" if is_success else "[ATTEMPT]"

                    if is_success:
                        success_count += 1
                        print(f"{prefix:<12} | {timestamp:<22} | {ip:<15} | {status} | {size_str:<5} | {request}", file=out)
                    else:
                        pass

        print(f"Analyse de faille sql terminée.")
        print(f"Total de tentatives détectées : {total_sqli}")
        output_path = os.path.abspath(output_file)
        print(f"Résultats sauvegardés dans : {output_path}")

    except FileNotFoundError:
        print("Erreur : Le fichier est introuvable.")

if __name__ == "__main__":
    file_to_analyze = sys.argv[1] if len(sys.argv) > 1 else log_file
    analyze_logs(file_to_analyze)
