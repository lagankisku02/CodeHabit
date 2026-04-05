CodeHabit – Coding Activity Tracker

A simple Python-based automation tool that tracks how much time you spend coding in VS Code and motivates you with daily reports via Telegram.

---

Features

- Tracks VS Code usage in real-time
- Stores daily coding time in JSON format
- Maintains a daily streak system
- Sends Telegram notifications:
  - When daily goal is achieved
  - Daily report at a fixed time
- Runs automatically using a scheduler

---

How It Works

- The script checks running processes every few seconds
- If VS Code is detected, it increments your coding time
- Data is stored locally in a JSON file (`logs/data.json`)
- At the end of the day:
  - If goal is achieved → motivational message
  - Else → improvement message
- Streak is updated based on consecutive days meeting the goal

---

Tech Stack

- **Python**
- `psutil` → process tracking
- `schedule` → task scheduling
- `requests` → Telegram API
- `json` → data storage

---

Setup & Installation

1.Clone the repository

git clone https://github.com/lagankisku02/codehabit.git
cd codehabit

2.Install dependencies

pip install psutil schedule requests

3.Set up Telegram Bot

Create a bot using BotFather
Get your BOT_TOKEN
Get your CHAT_ID

4.Set environment variables

export BOT_TOKEN="your_token"
export CHAT_ID="your_chat_id"

5.Run the script

python vscode_tracker.py

---

Purpose -

This project was built as a Python automation practice project and a personal productivity tool to stay consistent with coding habits.

Author - Lagan Kisku
