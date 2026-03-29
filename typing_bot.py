import os
import sys
import subprocess
import time
import random
import string
import threading
import webbrowser
import json

# ==========================================
# 1. AUTO DEPENDENCY INSTALLER
# ==========================================
REQUIRED_PACKAGES = {
    'pyautogui': 'pyautogui',
    'pynput': 'pynput',
    'colorama': 'colorama'
}

def setup_dependencies():
    install_all = False
    for module_name, package_name in REQUIRED_PACKAGES.items():
        try:
            __import__(module_name)
        except ImportError:
            if not install_all:
                print(f"\n[!] Required package '{package_name}' is not installed.")
                print("Options:")
                print("  [Y]   - Install this package")
                print("  [All] - Install ALL missing packages automatically")
                print("  [N]   - Cancel and Exit")
                ans = input(f"Select an option for '{package_name}': ").strip().lower()
                
                if ans == 'all':
                    install_all = True
                elif ans != 'y':
                    print("[-] Setup cancelled. Exiting program.")
                    sys.exit()
            
            print(f"[*] Downloading and Installing {package_name}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package_name, "--quiet"])
            print(f"[+] {package_name} installed successfully!\n")

setup_dependencies()

# ==========================================
# 2. IMPORTS & GLOBAL CONFIGURATION
# ==========================================
import pyautogui
from pynput import mouse
from colorama import init, Fore, Style

init(autoreset=True)
pyautogui.FAILSAFE = True

typing_active = False
pause_event = threading.Event()
pause_event.set()

REPO_URL = "https://github.com/Rehmanalidevpro/Auto_typing_bot_Real"
ISSUES_URL = "https://github.com/Rehmanalidevpro/Auto_typing_bot_Real/issues"

# Default Configuration
DEFAULT_CONFIG = {
    "speed_min": 0.04,
    "speed_max": 0.15,
    "typo_chance": 0.05,
    "pause_chance": 0.03,
    "lower_case_chance": 0.30
}

DEFAULT_WORDS = {
    "i am": "I'm", "I am": "I'm", "do not": "don't", "Do not": "Don't",
    "cannot": "can't", "Cannot": "Can't", "you are": "you're", "You are": "You're"
}

def load_json(filename, default_data):
    if not os.path.exists(filename):
        with open(filename, 'w') as f:
            json.dump(default_data, f, indent=4)
        return default_data
    with open(filename, 'r') as f:
        return json.load(f)

def save_json(filename, data):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

config = load_json('config.json', DEFAULT_CONFIG)
words_dict = load_json('words.json', DEFAULT_WORDS)

# ==========================================
# 3. UI & BRANDING
# ==========================================
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def display_banner():
    clear_screen()
    print(f"{Fore.CYAN}{Style.BRIGHT}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}{Style.BRIGHT}                        A U T O   T Y P I N G   B O T   R E A L                           {Style.RESET_ALL}")
    print(f"{Fore.CYAN}{Style.BRIGHT}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Style.RESET_ALL}")
    print(f"{Fore.GREEN} [+] Developer    : {Fore.WHITE}Rehman Ali")
    print(f"{Fore.GREEN} [+] GitHub Repo  : {Fore.WHITE}{REPO_URL}")
    print(f"{Fore.GREEN} [+] Bug Report   : {Fore.WHITE}{ISSUES_URL}")
    print(f"{Fore.CYAN}{Style.BRIGHT}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Style.RESET_ALL}")
    
    print(f"{Fore.MAGENTA}{Style.BRIGHT} [ ABOUT THIS TOOL ]{Style.RESET_ALL}")
    print(f"{Fore.WHITE} A highly advanced, easy-to-use AI typing simulator. It bypasses bot-detection by")
    print(f"{Fore.WHITE} simulating 100% real human keystrokes. Fully customizable speed and human errors.\n")
    
    print(f"{Fore.YELLOW} Main Features:{Style.RESET_ALL}")
    print(f"{Fore.WHITE}   • {Fore.CYAN}Smart Pause/Resume{Fore.WHITE} : Click anywhere else to PAUSE. Click back to RESUME.")
    print(f"{Fore.WHITE}   • {Fore.CYAN}Human Typing{Fore.WHITE}       : Natural delays, random mistakes, and auto-corrections.")
    print(f"{Fore.WHITE}   • {Fore.CYAN}Custom Word List{Fore.WHITE}   : Edit 'words.json' to auto-replace common words.")
    print(f"{Fore.CYAN}{Style.BRIGHT}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Style.RESET_ALL}\n")

# ==========================================
# 4. SETTINGS & CONFIGURATION WIZARD
# ==========================================
def configuration_menu():
    global config
    while True:
        clear_screen()
        print(f"{Fore.CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}{Style.BRIGHT}                           S E T T I N G S   M E N U                                      {Style.RESET_ALL}")
        print(f"{Fore.CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Style.RESET_ALL}")
        print(f"{Fore.WHITE} Current Typing Speed  : {config['speed_min']}s to {config['speed_max']}s per key")
        print(f"{Fore.WHITE} Making Mistakes Chance: {int(config['typo_chance']*100)}%")
        print(f"{Fore.WHITE} Thinking Pause Chance : {int(config['pause_chance']*100)}%")
        print(f"{Fore.CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Style.RESET_ALL}\n")
        
        print(f"  {Fore.GREEN}[1]{Fore.WHITE} Setup Typing Speed")
        print(f"  {Fore.GREEN}[2]{Fore.WHITE} Setup Mistakes & Errors (Typos)")
        print(f"  {Fore.GREEN}[3]{Fore.WHITE} Reset All Settings to Default")
        print(f"  {Fore.GREEN}[4]{Fore.WHITE} Go Back to Main Menu")
        
        choice = input(f"\n{Fore.CYAN}[>] Enter your choice (1-4): {Style.RESET_ALL}").strip()
        
        if choice == '4':
            break
        elif choice == '3':
            config = DEFAULT_CONFIG.copy()
            save_json('config.json', config)
            print(f"{Fore.GREEN}[+] Settings restored to Default!{Style.RESET_ALL}")
            time.sleep(1.5)
        elif choice == '1':
            print(f"\n{Fore.YELLOW}Select Typing Speed:{Style.RESET_ALL}")
            print(" 1. Slow   (Good for long articles, very safe)")
            print(" 2. Normal (Recommended default, human speed)")
            print(" 3. Fast   (Fast typing, for quick copy-paste)")
            print(" 4. Custom (Set your own delay in seconds)")
            s_choice = input("Select speed (1-4): ").strip()
            if s_choice == '1':
                config['speed_min'], config['speed_max'] = 0.08, 0.25
            elif s_choice == '2':
                config['speed_min'], config['speed_max'] = 0.04, 0.15
            elif s_choice == '3':
                config['speed_min'], config['speed_max'] = 0.01, 0.06
            elif s_choice == '4':
                try:
                    config['speed_min'] = float(input("Enter minimum delay (e.g., 0.02): "))
                    config['speed_max'] = float(input("Enter maximum delay (e.g., 0.10): "))
                except ValueError:
                    print(f"{Fore.RED}[!] Invalid input. Speed not changed.{Style.RESET_ALL}")
            save_json('config.json', config)
            print(f"{Fore.GREEN}[+] Speed settings saved!{Style.RESET_ALL}")
            time.sleep(1.5)
        elif choice == '2':
            try:
                print(f"\n{Fore.YELLOW}Setup Errors (Typos):{Style.RESET_ALL}")
                val = int(input("Enter chance of making mistakes (0 to 100, Default is 5): "))
                config['typo_chance'] = min(max(val, 0), 100) / 100.0
                save_json('config.json', config)
                print(f"{Fore.GREEN}[+] Error settings saved!{Style.RESET_ALL}")
            except ValueError:
                print(f"{Fore.RED}[!] Invalid input.{Style.RESET_ALL}")
            time.sleep(1.5)

# ==========================================
# 5. MOUSE LISTENER (SMART PAUSE/RESUME)
# ==========================================
def on_click(x, y, button, pressed):
    global typing_active
    if typing_active and pressed:
        if pause_event.is_set():
            pause_event.clear()
            print(f"\n{Fore.RED}[!] SYSTEM PAUSED: {Fore.WHITE}You clicked somewhere else.")
            print(f"{Fore.YELLOW}[*] ACTION REQUIRED: Click inside the typing box again to RESUME.{Style.RESET_ALL}")
        else:
            pause_event.set()
            print(f"\n{Fore.GREEN}[+] SYSTEM RESUMED: {Fore.WHITE}Continuing typing...{Style.RESET_ALL}")

# ==========================================
# 6. CORE TYPING ENGINE
# ==========================================
def modify_text(text):
    text = text.replace('\n', ' ').replace('\r', ' ')
    while '  ' in text:
        text = text.replace('  ', ' ')

    # Use words from words.json
    for old, new in words_dict.items():
        text = text.replace(old, new)
    return text

def advanced_human_typing(text):
    global typing_active
    text = modify_text(text)
    
    listener = mouse.Listener(on_click=on_click)
    listener.start()
    
    typing_active = True
    after_period = False 
    was_paused = False
    
    for char in text:
        if not pause_event.is_set():
            was_paused = True
            pause_event.wait() 
            
        if was_paused:
            time.sleep(0.5) 
            was_paused = False

        # Formatting occasionally
        if after_period and char.isalpha():
            if random.random() < config['lower_case_chance']: 
                char = char.lower()
                print(f"{Fore.CYAN}[*] Human Effect: {Fore.WHITE}Did not capitalize '{char}'")
            after_period = False
            
        if char == '.':
            after_period = True

        # Typo Injection
        if char.isalpha() and random.random() < config['typo_chance']:
            wrong_char = random.choice(string.ascii_lowercase)
            pyautogui.write(wrong_char)
            print(f"{Fore.RED}[-] Human Effect: {Fore.WHITE}Made a typo -> '{wrong_char}'")
            time.sleep(random.uniform(0.1, 0.3)) 
            
            # Correction
            if random.random() < 0.85:
                pyautogui.press('backspace')
                print(f"{Fore.GREEN}[+] Human Effect: {Fore.WHITE}Corrected the typo.")
                time.sleep(random.uniform(0.1, 0.4))
                pyautogui.write(char) 
        else:
            pyautogui.write(char)
        
        # Speed mapping from config
        time.sleep(random.uniform(config['speed_min'], config['speed_max']))
        
        # Pause mapping from config
        if char == ' ' and random.random() < config['pause_chance']:
            pause_time = random.uniform(1.0, 5.0)
            print(f"{Fore.YELLOW}[*] Human Effect: {Fore.WHITE}Taking a short break for {round(pause_time, 1)} seconds...")
            time.sleep(pause_time)

    typing_active = False
    listener.stop()
    print(f"\n{Fore.GREEN}[+] TASK COMPLETED: {Fore.WHITE}All text typed successfully.{Style.RESET_ALL}")

# ==========================================
# 7. MAIN MENU & WORKFLOW
# ==========================================
def uninstall_dependencies():
    print(f"\n{Fore.YELLOW}[*] Preparing to remove all installed libraries...{Style.RESET_ALL}")
    for package_name in REQUIRED_PACKAGES.values():
        subprocess.check_call([sys.executable, "-m", "pip", "uninstall", "-y", package_name, "--quiet"])
    print(f"{Fore.GREEN}[+] Success: All packages have been removed.{Style.RESET_ALL}")
    sys.exit()

def main():
    while True:
        display_banner()
        print(f"{Fore.CYAN}:: MAIN MENU ::{Style.RESET_ALL}")
        print(f"  {Fore.GREEN}[1]{Fore.WHITE} Start Auto Typing Bot")
        print(f"  {Fore.GREEN}[2]{Fore.WHITE} Settings & Configuration {Fore.YELLOW}(Speed, Typos, Setup){Style.RESET_ALL}")
        print(f"  {Fore.GREEN}[3]{Fore.WHITE} Open GitHub Repository {Fore.YELLOW}(Browser){Style.RESET_ALL}")
        print(f"  {Fore.GREEN}[4]{Fore.WHITE} Report an Issue or Bug {Fore.YELLOW}(Browser){Style.RESET_ALL}")
        print(f"  {Fore.GREEN}[5]{Fore.WHITE} Uninstall Dependencies")
        print(f"  {Fore.GREEN}[6]{Fore.WHITE} Exit System")
        
        choice = input(f"\n{Fore.CYAN}[>] Enter your choice (1-6): {Style.RESET_ALL}").strip()
        
        if choice == '6':
            print(f"\n{Fore.GREEN}[+] Thank you for using! Goodbye.{Style.RESET_ALL}")
            sys.exit()
            
        elif choice == '5':
            confirm = input(f"{Fore.RED}[!] WARNING: Do you want to remove all installed libraries? [y/N]: {Style.RESET_ALL}").strip().lower()
            if confirm == 'y':
                uninstall_dependencies()
                
        elif choice == '3':
            print(f"\n{Fore.YELLOW}[*] Opening GitHub in browser...{Style.RESET_ALL}")
            webbrowser.open(REPO_URL)
            time.sleep(2)
            
        elif choice == '4':
            print(f"\n{Fore.YELLOW}[*] Opening Issue Tracker in browser...{Style.RESET_ALL}")
            webbrowser.open(ISSUES_URL)
            time.sleep(2)

        elif choice == '2':
            configuration_menu()
            
        elif choice == '1':
            print(f"\n{Fore.CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Style.RESET_ALL}")
            print(f"{Fore.GREEN} [ INSTRUCTION ]{Style.RESET_ALL}")
            print(f"{Fore.WHITE} 1. Paste your large text below (Ctrl+V or Right-Click).")
            print(f"{Fore.WHITE} 2. When you are done pasting, type {Fore.RED}DONE{Fore.WHITE} on a new line.")
            print(f"{Fore.WHITE} 3. Press Enter to confirm.")
            print(f"{Fore.CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Style.RESET_ALL}\n")

            user_lines =[]
            while True:
                try:
                    line = input()
                except EOFError:
                    break
                    
                if line.strip().upper() == 'DONE':
                    break
                user_lines.append(line)
                
            full_text = ' '.join(user_lines)

            if full_text.strip() == "":
                print(f"\n{Fore.RED}[!] Error: No text pasted. Returning to main menu.{Style.RESET_ALL}")
                time.sleep(2)
                continue

            print(f"\n{Fore.CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Style.RESET_ALL}")
            confirm_start = input(f"{Fore.WHITE}[?] Are you ready? Press {Fore.GREEN}[ENTER]{Fore.WHITE} to start or {Fore.RED}[N]{Fore.WHITE} to cancel: {Style.RESET_ALL}").strip().lower()
            
            if confirm_start != 'n':
                wait_time = random.randint(4, 10)
                print(f"\n{Fore.YELLOW}[*] The bot will start typing in {wait_time} seconds...{Style.RESET_ALL}")
                print(f"{Fore.RED}[!] URGENT: Click inside the target typing box immediately!{Style.RESET_ALL}")
                
                time.sleep(wait_time)
                print(f"\n{Fore.GREEN}[+] SYSTEM STARTED. Typing text now...{Style.RESET_ALL}\n")
                
                advanced_human_typing(full_text)
                
                input(f"\n{Fore.CYAN}[>] Press [ENTER] to return to the Main Menu...{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}[!] Typing cancelled.{Style.RESET_ALL}")
                time.sleep(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Fore.RED}[!] Forced closed by user. Goodbye.{Style.RESET_ALL}")
        sys.exit()