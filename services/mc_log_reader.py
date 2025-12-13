import subprocess
import re
import json
import sys
import telegram_bot

CHAT_REGEX = re.compile(
    r"\[(?P<time>\d{2}:\d{2}:\d{2}) INFO]: <(?P<player>[^>]+)> (?P<message>.*)"
)

process = subprocess.Popen(
    ["java", "-Xms2G", "-Xmx2G", "-jar", "paper-1.21.10-115.jar", "--nogui"],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True,
    bufsize=1
)

print("Сервер запущен. Читаю чат...\n")
sys.stdout.flush()

for line in process.stdout:
    line = line.strip()
    m = CHAT_REGEX.search(line)
    if m:
        event = {
            "time": m.group("time"),
            "player": m.group("player"),
            "message": m.group("message")
        }
        telegram_bot.get_message_form_rcon(m.group("player"), m.group("message"))
        print(json.dumps(event, ensure_ascii=False))