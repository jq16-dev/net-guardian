import requests
import time
import winsound
import subprocess
from plyer import notification
from datetime import datetime
import os
import socket

# ---------- CONFIG ----------
CHECK_INTERVAL = 3
CONFIRM_COUNT = 2
TEST_URL = "https://mail.google.com/"
MAX_SPEED_KB = 16

# Make log file absolute path
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_FILE = os.path.join(SCRIPT_DIR, "internet_log.txt")

# ---------- STATE ----------
last_status = None
last_wifi = None
success_streak = 0
fail_streak = 0


# ---------- FUNCTIONS ----------

def get_wifi_name():
    try:
        output = subprocess.check_output(
            "netsh wlan show interfaces", shell=True, encoding="utf-8", errors="ignore"
        )
        for line in output.splitlines():
            if "SSID" in line and "BSSID" not in line:
                return line.split(":")[1].strip()
        return "No Wi-Fi"
    except:
        return "Unknown"


def measure_speed_kb():
    try:
        start = time.time()
        r = requests.get(TEST_URL, timeout=6)
        r.raise_for_status()
        end = time.time()
        size_kb = len(r.content) / 1024
        duration = end - start
        if duration == 0:
            return MAX_SPEED_KB
        speed = round(size_kb / duration, 2)
        return speed if speed > 0 else MAX_SPEED_KB
    except:
        return 0


def format_speed(speed_kbps):
    if speed_kbps >= 1024:
        return f"{round(speed_kbps / 1024, 2)} MB/s"
    return f"{round(speed_kbps, 2)} KB/s"


def notify(status, speed_kbps, wifi_name):
    now = datetime.now().strftime("%d %b %Y, %I:%M:%S %p")
    speed_str = format_speed(speed_kbps)
    title = f"Internet Status: {'UP ✅' if status else 'DOWN ❌'}"
    message = f"Checked at: {now}\nSpeed: {speed_str}\nWi-Fi: {wifi_name}"

    # Plyer notification
    notification.notify(
        title=title,
        message=message,
        timeout=5
    )

    # Optional beep when online
    if status:
        winsound.Beep(1000, 400)

    print(f"{title} | {message}")  # Console log
    log_status(now, wifi_name, status, speed_str)


def log_status(timestamp, wifi_name, status, speed_str):
    log_entry = f"{timestamp} | Wi-Fi: {wifi_name} | {'UP' if status else 'DOWN'} | {speed_str}\n"
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(log_entry)


# ---------- MAIN LOOP ----------
while True:
    current_wifi = get_wifi_name()

    # Reset streaks if Wi-Fi changes
    if current_wifi != last_wifi:
        success_streak = 0
        fail_streak = 0
        last_status = None
        last_wifi = current_wifi

    speed = measure_speed_kb()
    is_online = speed > 0

    # Update streaks
    if is_online:
        success_streak += 1
        fail_streak = 0
    else:
        fail_streak += 1
        success_streak = 0

    # Confirm status based on streak
    confirmed_status = last_status
    if success_streak >= CONFIRM_COUNT:
        confirmed_status = True
    if fail_streak >= CONFIRM_COUNT:
        confirmed_status = False

    # Notify only on status change
    if confirmed_status != last_status:
        notify(confirmed_status, speed, current_wifi)
        last_status = confirmed_status

    time.sleep(CHECK_INTERVAL)