import time
import psutil
import os
import schedule

total_time = 0  # in seconds

def check_vs_code():
    global total_time
    
    found = False

    for process in psutil.process_iter(['name']):
        if process.info['name'] == "code":
            found = True
            break

    if found:
        total_time += 5  # because we check every 5 seconds
        print(f"Coding... Total time: {total_time} seconds")

        with open("logs/data.txt", "a") as log_file:
            log_file.write(f"{total_time} seconds\n")
    else:
        print("VS Code not running")

# create logs folder if not exists
if not os.path.exists("logs"):
    os.mkdir("logs")

schedule.every(5).seconds.do(check_vs_code)

while True:
    schedule.run_pending()
    time.sleep(1)