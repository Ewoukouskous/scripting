import gzip
import re

log_file = "full-logs.sorted.txt.gz"

# Common SQLi patterns
sqli_patterns = [
    r"UNION", r"SELECT", r"INSERT", r"UPDATE", r"DELETE", r"DROP",
    r"ORDER BY", r"GROUP BY", r"SLEEP\(", r"BENCHMARK\(",
    r"OR 1=1", r"AND 1=1", r"'", r"\"", r"--", r"WAITFOR DELAY"
]

regex_sqli = re.compile("|".join(sqli_patterns), re.IGNORECASE)

def analyze_logs(file_path):
    success_count = 0
    total_sqli = 0

    try:
        with gzip.open(file_path, 'rt', encoding='utf-8', errors='ignore') as f:
            for line in f:
                parts = re.split(r'\s(?=(?:[^"]*"[^"]*")*[^"]*$)', line)

                if len(parts) < 9:
                    continue

                ip = parts[0]
                timestamp = parts[3].strip('[]')
                request = parts[5].strip('"')
                status = parts[6]

                if regex_sqli.search(request):
                    total_sqli += 1

                    is_success = status.startswith('2')
                    prefix = "[SUCCESS]" if is_success else "[ATTEMPT]"

                    if is_success:
                        success_count += 1
                        print(f"{prefix} {timestamp:<20} | {ip:<15} | {status} | {request}\033[0m")
                    else:
                        pass

        print(f"{'=' * 80}")
        print(f"Analyse terminée.")
        print(f"Total de tentatives SQLi détectées : {total_sqli}")

    except FileNotFoundError:
        print("Erreur : Le fichier est introuvable.")

if __name__ == "__main__":
    analyze_logs(log_file)