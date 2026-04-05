from datetime import datetime, timedelta
import time
import psutil
import os
import schedule
import json
import requests

LOG_FILE = "logs/data.json"
CHECK_INTERVAL = 5
TARGET_TIME = 3600
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

if not os.path.exists("logs"):
    os.mkdir("logs")

def send_telegram(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": CHAT_ID,
        "text": message
    }
    try:
        response = requests.post(url, data=data)
        print("Telegram sent:", response.status_code)
    except Exception as e:
        print("Telegram error:", e)

def load_data():
    if not os.path.exists(LOG_FILE):
        return {}
    with open(LOG_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(LOG_FILE, "w") as f:
        json.dump(data, f, indent=4)

data = load_data()

def check_vs_code():
    global data

    today = datetime.now().strftime("%Y-%m-%d")
    
    if today not in data:
        data[today] = {"time": 0, "streak": 0, "notified": False}
    
    found = False
    for process in psutil.process_iter(['name']):
        if process.info['name'] and "code" in process.info['name']:
            found = True
            break

    if found:
        data[today]["time"] += CHECK_INTERVAL
        print(f"Coding... {data[today]['time']} seconds")

    save_data(data)

def update_streak():
    global data
    
    today = datetime.now().strftime("%Y-%m-%d")
    yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")

    if today not in data:
        return

    if data[today]["time"] >= TARGET_TIME:
        if yesterday in data and data[yesterday]["time"] >= TARGET_TIME:
            data[today]["streak"] = data[yesterday]["streak"] + 1
        else:
            data[today]["streak"] = 1
    else:
        data[today]["streak"] = 0

    save_data(data)

def send_message():
    global data

    today = datetime.now().strftime("%Y-%m-%d")

    if today not in data:
        return

    minutes = data[today]["time"] // 60

    msg1 = f"Today you have coded for {minutes} minutes. Keep it up!🔥"
    msg2 = f"Today you have coded for {minutes} minutes! Try to increase it tomorrow!💪"    

    if data[today]["time"] >= TARGET_TIME and not data[today].get("notified", False):
        send_telegram(msg1)
        data[today]["notified"] = True
    else:
        send_telegram(msg2)
        data[today]["notified"] = True
    
    save_data(data)

schedule.every(CHECK_INTERVAL).seconds.do(check_vs_code)

schedule.every(1).minutes.do(update_streak)

schedule.every().day.at("23:00").do(send_message)

while True:
    schedule.run_pending()
    time.sleep(1)
