import gzip
import re
import urllib.parse
import sys

log_file = "../calt.log.gz"

xss_patterns = [
    r"<script", r"iframe", r"onload", r"onerror", r"alert\(",
    r"document\.cookie", r"javascript:", r"String\.fromCharCode"
]
regex_xss = re.compile("|".join(xss_patterns), re.IGNORECASE)

def analyze_xss(file_path):
    success_count = 0
    total_xss = 0

    try:
        with gzip.open(file_path, 'rt', encoding='utf-8', errors='ignore') as f, \
                open("xss_detector_logs.txt", 'w', encoding='utf-8') as out:
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

    except FileNotFoundError:
        print(f"Fichier non trouvé : {file_path}")

if __name__ == "__main__":
    file_to_analyze = sys.argv[1] if len(sys.argv) > 1 else log_file
    analyze_xss(file_to_analyze)
