import gzip
import re

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

    try:
        with gzip.open(file_path, 'rt', encoding='utf-8', errors='ignore') as f, \
                open("sql_attack_logs.txt", 'w', encoding='utf-8') as out:
            for line in f:
                parts = re.split(r'\s(?=(?:[^"]*"[^"]*")*[^"]*$)', line)

                if len(parts) < 9:
                    continue

                ip = parts[0]
                timestamp = parts[3].strip('[]')
                request = parts[5].strip('"')
                status = parts[6]

                if regex_sqli.search(request) and "?" in request:
                    if regex_exclusions.search(request):
                        continue
                    total_sqli += 1

                    is_success = status.startswith('2')
                    prefix = "[SUCCESS]" if is_success else "[ATTEMPT]"

                    if is_success:
                        success_count += 1
                        print(f"{prefix} {timestamp:<20} | {ip:<15} | {status} | {request}", file=out)
                    else:
                        pass

        print(f"{'=' * 80}")
        print(f"Analyse terminée.")
        print(f"Total de tentatives SQLi détectées : {total_sqli}")

    except FileNotFoundError:
        print("Erreur : Le fichier est introuvable.")

if __name__ == "__main__":
    analyze_logs(log_file)