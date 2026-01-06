import ast
import time

file_name = 'logs.txt'
output_file = 'succesfull_bruteforce.txt'
pending_sequences = {}

SEUIL_ALERTE = 5

print(f"Analyse en cours...")
debut = time.perf_counter()

with open(file_name, 'r', encoding='utf-8') as file:
    for line in file:
        try:
            clean_line = line.strip()
            log_list = ast.literal_eval(clean_line)
            ip = log_list[0]
            status = log_list[3]

            if status == '401':
                if ip not in pending_sequences:
                    pending_sequences[ip] = []
                pending_sequences[ip].append(clean_line)

            elif status == '200':
                if ip in pending_sequences and len(pending_sequences[ip]) >= SEUIL_ALERTE:
                    with open(output_file, 'a', encoding='utf-8') as f_out:
                        f_out.write(f"--- Bruteforce réussi avec : {ip} ---\n")
                        for s_line in pending_sequences[ip]:
                            f_out.write('❌ ' + s_line + "\n")
                        f_out.write(f"✔️ {clean_line} \n")
                        f_out.write("-" * 50 + "\n\n")

                    print(f"[!] Alerte : Brute force réussi pour l'IP {ip}")

                if ip in pending_sequences:
                    del pending_sequences[ip]

            else:
                if ip in pending_sequences:
                    del pending_sequences[ip]

        except (SyntaxError, ValueError, IndexError):
            continue

fin = time.perf_counter()
print(f"\nAnalyse terminée en {fin - debut:.4f}s. Vérifiez '{output_file}'.")