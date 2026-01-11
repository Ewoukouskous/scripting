import os
import sys
import io
import subprocess
import threading
import time

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

class Colors:
    GREEN1 = '\033[38;5;46m'
    GREEN2 = '\033[38;5;40m'
    GREEN3 = '\033[38;5;34m'
    GREEN4 = '\033[38;5;28m'
    GREEN5 = '\033[38;5;22m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

class Spinner:
    def __init__(self, message="Analyse en cours"):
        self.spinner_chars = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
        self.message = message
        self.is_running = False
        self.thread = None

    def spin(self):
        idx = 0
        while self.is_running:
            char = self.spinner_chars[idx % len(self.spinner_chars)]
            sys.stdout.write(f'\r{Colors.GREEN2}{char} {self.message}...{Colors.RESET}')
            sys.stdout.flush()
            time.sleep(0.1)
            idx += 1
        sys.stdout.write('\r' + ' ' * (len(self.message) + 10) + '\r')
        sys.stdout.flush()

    def start(self):
        self.is_running = True
        self.thread = threading.Thread(target=self.spin)
        self.thread.start()

    def stop(self):
        self.is_running = False
        if self.thread:
            self.thread.join()

def print_ascii_art():
    art = rf"""
{Colors.GREEN1}            /^\/^\
{Colors.GREEN1}          _|__|  O|
{Colors.GREEN2} \/     /~     \_/ \
{Colors.GREEN2}  \____|__________/  \
{Colors.GREEN3}         \_______      \
{Colors.GREEN3}                 `\     \                 \
{Colors.GREEN3}                   |     |                  \
{Colors.GREEN4}                  /      /                    \
{Colors.GREEN4}                 /     /                       \
{Colors.GREEN5}               /      /                         \ \
{Colors.GREEN5}              /     /                            \  \
{Colors.GREEN5}            /     /             _----_            \   \
{Colors.GREEN5}           /     /           _-~      ~-_         |   |
{Colors.GREEN5}          (      (        _-~    _--_    ~-_     _/   |
{Colors.GREEN5}           \      ~-____-~    _-~    ~-_    ~-_-~    /
{Colors.GREEN5}             ~-_           _-~          ~-_       _-~
{Colors.GREEN5}                ~--______-~                ~-___-~

{Colors.BOLD}{Colors.GREEN1}  ╦  ╔═╗╔═╗  {Colors.GREEN2}╔═╗╔═╗╦═╗╔═╗╔╗╔{Colors.GREEN3}╔═╗╔╗╔╔═╗╦╔═╔═╗
{Colors.BOLD}{Colors.GREEN1}  ║  ║ ║║ ╦  {Colors.GREEN2}╠╣ ║ ║╠╦╝║╣ ║║║{Colors.GREEN3}╚═╗║║║╠═╣╠╩╗║╣ 
{Colors.BOLD}{Colors.GREEN1}  ╩═╝╚═╝╚═╝  {Colors.GREEN2}╚  ╚═╝╩╚═╚═╝╝╚╝{Colors.GREEN3}╚═╝╝╚╝╩ ╩╩ ╩╚═╝
{Colors.RESET}
{Colors.GREEN3}═══════════════════════════════════════════════════════════════
{Colors.GREEN4}        Outil de Forensic pour l'Analyse de Logs Apache
{Colors.GREEN3}═══════════════════════════════════════════════════════════════
{Colors.RESET}
"""
    print(art)

def get_log_file():
    print(f"{Colors.GREEN2}[?] Veuillez entrer le nom du fichier de logs à analyser:{Colors.RESET}")
    print(f"{Colors.GREEN4}    (Exemple: full-logs.sorted.txt){Colors.RESET}")

    script_dir = os.path.dirname(os.path.abspath(__file__))

    while True:
        log_file = input(f"{Colors.GREEN3}>>> {Colors.RESET}").strip()

        if not log_file:
            print(f"{Colors.GREEN5}[!] Veuillez entrer un nom de fichier valide.{Colors.RESET}")
            continue

        if not os.path.isabs(log_file):
            full_path = os.path.join(script_dir, log_file)
            if os.path.exists(full_path):
                print(f"{Colors.GREEN2}[✓] Fichier trouvé: {log_file}{Colors.RESET}\n")
                return full_path

        if os.path.exists(log_file):
            print(f"{Colors.GREEN2}[✓] Fichier trouvé: {log_file}{Colors.RESET}\n")
            return log_file

        print(f"{Colors.GREEN5}[!] Fichier non trouvé: {log_file}{Colors.RESET}")
        print(f"{Colors.GREEN4}    Recherche effectuée dans: {script_dir}{Colors.RESET}")
        retry = input(f"{Colors.GREEN4}    Voulez-vous réessayer? (o/n): {Colors.RESET}").strip().lower()
        if retry != 'o':
            print(f"{Colors.GREEN5}[!] Arrêt du programme.{Colors.RESET}")
            sys.exit(0)

def ask_display_mode():
    print(f"\n{Colors.GREEN2}╔═══════════════════════════════════════════════════════════════╗{Colors.RESET}")
    print(f"{Colors.GREEN2}║           {Colors.BOLD}TYPE D'AFFICHAGE DES RÉSULTATS{Colors.RESET}{Colors.GREEN2}                      ║{Colors.RESET}")
    print(f"{Colors.GREEN2}╠═══════════════════════════════════════════════════════════════╣{Colors.RESET}")
    print(f"{Colors.GREEN2}║                                                               ║{Colors.RESET}")
    print(f"{Colors.GREEN2}║  {Colors.GREEN1}[1]{Colors.GREEN3} Afficher tous les logs (tentatives + réussites)          ║{Colors.RESET}")
    print(f"{Colors.GREEN2}║  {Colors.GREEN1}[2]{Colors.GREEN3} Afficher uniquement les réussites                        ║{Colors.RESET}")
    print(f"{Colors.GREEN2}║                                                               ║{Colors.RESET}")
    print(f"{Colors.GREEN2}╚═══════════════════════════════════════════════════════════════╝{Colors.RESET}")

    while True:
        choice = input(f"{Colors.GREEN2}[>] Votre choix: {Colors.RESET}").strip()
        if choice in ['1', '2']:
            return 'all' if choice == '1' else 'success'
        print(f"{Colors.GREEN5}[!] Choix invalide. Veuillez entrer 1 ou 2.{Colors.RESET}")

def display_menu():
    menu = f"""
{Colors.GREEN2}╔═══════════════════════════════════════════════════════════════╗
║                      {Colors.BOLD}MENU PRINCIPAL{Colors.RESET}{Colors.GREEN2}                           ║
╠═══════════════════════════════════════════════════════════════╣
║                                                               ║
║  {Colors.GREEN1}[1]{Colors.GREEN3} Détection de Bruteforce                                  ║
║  {Colors.GREEN1}[2]{Colors.GREEN3} Détection d'Injection SQL                                ║
║  {Colors.GREEN1}[3]{Colors.GREEN3} Détection de Path Traversal                              ║
║  {Colors.GREEN1}[4]{Colors.GREEN3} Détection de XSS (Cross-Site Scripting)                  ║
║  {Colors.GREEN1}[5]{Colors.GREEN3} Détection de RCE (Remote Code Execution)                 ║
║  {Colors.GREEN1}[6]{Colors.GREEN3} Détection d'Exfiltration de Données                      ║
║                                                               ║
║  {Colors.GREEN1}[7]{Colors.GREEN3} Filtrer par IP                                           ║
║  {Colors.GREEN1}[8]{Colors.GREEN3} Trier les IPs par occurrence                             ║
║  {Colors.GREEN1}[9]{Colors.GREEN3} Filtrer les User-Agents non conventionnels               ║
║                                                               ║
║  {Colors.GREEN1}[A]{Colors.GREEN3} Analyse complète (tous les tests)                        ║
║                                                               ║
║  {Colors.GREEN5}[0]{Colors.GREEN4} Quitter                                                  ║
║                                                               ║
{Colors.GREEN2}╚═══════════════════════════════════════════════════════════════╝{Colors.RESET}
"""
    print(menu)

def run_script(script_name, log_file, display_mode=None):
    print(f"\n{Colors.GREEN3}[*] Exécution de {script_name}...{Colors.RESET}\n")

    needs_mode = 'path_traversal/' in script_name or 'rce_checker/' in script_name

    if display_mode is None and needs_mode:
        display_mode = ask_display_mode()

    script_dir = os.path.dirname(os.path.abspath(__file__))
    full_script_path = os.path.join(script_dir, script_name)

    if os.path.exists(full_script_path):
        spinner = Spinner("Analyse en cours")
        spinner.start()

        try:
            cmd = ["python", full_script_path, log_file]
            if display_mode:
                cmd.append(display_mode)

            env = os.environ.copy()
            env['PYTHONIOENCODING'] = 'utf-8'

            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                encoding='utf-8',
                errors='replace',
                env=env
            )

            spinner.stop()

            if result.stdout:
                for line in result.stdout.strip().split('\n'):
                    if line:
                        print(line)

            if result.stderr and result.returncode != 0:
                print(f"{Colors.GREEN5}{result.stderr}{Colors.RESET}")

        except Exception as e:
            spinner.stop()
            print(f"{Colors.GREEN5}[!] Erreur lors de l'exécution: {e}{Colors.RESET}")
    else:
        print(f"{Colors.GREEN5}[!] Script non trouvé: {script_name}{Colors.RESET}")

    input(f"\n{Colors.GREEN4}Appuyez sur Entrée pour continuer...{Colors.RESET}")

def run_interactive_script(script_name, log_file):
    print(f"\n{Colors.GREEN3}[*] Exécution de {script_name}...{Colors.RESET}\n")

    script_dir = os.path.dirname(os.path.abspath(__file__))
    full_script_path = os.path.join(script_dir, script_name)

    if os.path.exists(full_script_path):
        command = f'python "{full_script_path}" "{log_file}"'
        os.system(command)
    else:
        print(f"{Colors.GREEN5}[!] Script non trouvé: {script_name}{Colors.RESET}")

    input(f"\n{Colors.GREEN4}Appuyez sur Entrée pour continuer...{Colors.RESET}")

def run_all_analysis(log_file):
    scripts = [
        ("bruteforce/bruteforce_checker.py", "Bruteforce"),
        ("faille_sql/sql_checker.py", "Injection SQL"),
        ("path_traversal/path_traversal_checker.py", "Path Traversal"),
        ("xss_checker/xss_checker.py", "XSS"),
        ("rce_checker/rce_checker.py", "RCE"),
        ("data_exfiltration/data_exfiltration.py", "Exfiltration de données")
    ]

    print(f"\n{Colors.GREEN2}[*] Démarrage de l'analyse complète...{Colors.RESET}\n")

    print(f"{Colors.GREEN3}[i] Mode d'affichage pour Path Traversal et RCE :{Colors.RESET}")
    display_mode = ask_display_mode()

    script_dir = os.path.dirname(os.path.abspath(__file__))

    for script, name in scripts:
        print(f"{Colors.GREEN3}{'='*63}{Colors.RESET}")
        print(f"{Colors.GREEN2}[*] Analyse: {name}{Colors.RESET}")
        print(f"{Colors.GREEN3}{'='*63}{Colors.RESET}")

        full_script_path = os.path.join(script_dir, script)
        if os.path.exists(full_script_path):
            spinner = Spinner(f"Analyse {name}")
            spinner.start()

            try:
                cmd = ["python", full_script_path, log_file]

                if 'path_traversal/' in script or 'rce_checker/' in script:
                    cmd.append(display_mode)

                env = os.environ.copy()
                env['PYTHONIOENCODING'] = 'utf-8'

                result = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                    encoding='utf-8',
                    errors='replace',
                    env=env
                )

                spinner.stop()

                if result.stdout:
                    for line in result.stdout.strip().split('\n'):
                        if line:
                            print(line)

                if result.stderr and result.returncode != 0:
                    print(f"{Colors.GREEN5}{result.stderr}{Colors.RESET}")

            except Exception as e:
                spinner.stop()
                print(f"{Colors.GREEN5}[!] Erreur lors de l'exécution: {e}{Colors.RESET}")
        else:
            print(f"{Colors.GREEN5}[!] Script non trouvé: {script}{Colors.RESET}")

        print()

    print(f"{Colors.GREEN2}[✓] Analyse complète terminée!{Colors.RESET}")
    input(f"\n{Colors.GREEN4}Appuyez sur Entrée pour continuer...{Colors.RESET}")

def main():
    if os.name == 'nt':
        os.system('')

    script_dir = os.path.dirname(os.path.abspath(__file__))
    results_dir = os.path.join(script_dir, 'results')
    if not os.path.exists(results_dir):
        os.makedirs(results_dir)
        print(f"{Colors.GREEN2}[✓] Dossier 'results' créé pour les fichiers de sortie{Colors.RESET}\n")

    clear_screen()
    print_ascii_art()

    log_file = get_log_file()

    while True:
        clear_screen()
        print_ascii_art()
        print(f"{Colors.GREEN3}[*] Fichier en cours d'analyse: {Colors.GREEN2}{log_file}{Colors.RESET}\n")
        display_menu()

        choice = input(f"{Colors.GREEN2}[>] Votre choix: {Colors.RESET}").strip().upper()

        if choice == '1':
            run_script("bruteforce/bruteforce_checker.py", log_file)
        elif choice == '2':
            run_script("faille_sql/sql_checker.py", log_file)
        elif choice == '3':
            run_script("path_traversal/path_traversal_checker.py", log_file)
        elif choice == '4':
            run_script("xss_checker/xss_checker.py", log_file)
        elif choice == '5':
            run_script("rce_checker/rce_checker.py", log_file)
        elif choice == '6':
            run_script("data_exfiltration/data_exfiltration.py", log_file)
        elif choice == '7':
            run_interactive_script("filter_by_ip.py", log_file)
        elif choice == '8':
            run_interactive_script("sort_ip_by_occurence.py", log_file)
        elif choice == '9':
            run_interactive_script("filter_unconventionnal_useragents.py", log_file)
        elif choice == 'A':
            run_all_analysis(log_file)
        elif choice == '0':
            print(f"\n{Colors.GREEN2}[*] Merci d'avoir utilisé Log Forensnake!{Colors.RESET}")
            print(f"{Colors.GREEN3}[*] À bientôt! 🐍{Colors.RESET}\n")
            sys.exit(0)
        else:
            print(f"{Colors.GREEN5}[!] Choix invalide. Veuillez réessayer.{Colors.RESET}")
            input(f"{Colors.GREEN4}Appuyez sur Entrée pour continuer...{Colors.RESET}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.GREEN5}[!] Interruption détectée.{Colors.RESET}")
        print(f"{Colors.GREEN3}[*] Arrêt de Log Forensnake. À bientôt! 🐍{Colors.RESET}\n")
        sys.exit(0)