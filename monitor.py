import subprocess
import requests
import time

# isi token dan chat id lo di sini
TELEGRAM_TOKEN = "8871724584:AAEvTYKSiwgMc6mzTgPUelmGEDmuvPoexjg"
TELEGRAM_CHAT_ID = "6208876002"

# daftar IP yang mau dimonitor
HOSTS = [
    "192.168.12.1",  # R1
    "192.168.12.2",  # R2
    "192.168.23.2",  # R3
    "8.8.8.8",       # Google DNS
]

def send_telegram(message):
    url = "https://api.telegram.org/bot" + TELEGRAM_TOKEN + "/sendMessage"
    requests.post(url, data={"chat_id": TELEGRAM_CHAT_ID, "text": message})

def ping(host):
    result = subprocess.run(
        ["ping", "-n", "1", "-w", "1000", host],
        stdout=subprocess.DEVNULL
    )
    return result.returncode == 0

def monitor():
    print("Network Monitor started...")
    while True:
        for host in HOSTS:
            status = ping(host)
            if not status:
                msg = f"⚠️ ALERT: {host} is DOWN!"
                print(msg)
                send_telegram(msg)
            else:
                print(f"✅ {host} is UP")
        print("--- cek ulang dalam 30 detik ---")
        time.sleep(30)

if __name__ == "__main__":
    monitor()