import re
import json
import asyncio
import os
import aiofiles

CHAT_REGEX = re.compile(
    r"\[(?P<time>\d{2}:\d{2}:\d{2})\] \[.*?/INFO\]: <(?P<player>[^>]+)> (?P<message>.*)"
)

log_path = "logs/latest.log"


async def watch_logs():
    last_size = 0
    f = await aiofiles.open(log_path, "r", encoding="utf-8")
    await f.seek(0, 2)
    while True:
        if not os.path.exists(log_path):
            await asyncio.sleep(0.1)
            continue
        size = os.path.getsize(log_path)
        if size < last_size:
            await f.close()
            f = await aiofiles.open(log_path, "r", encoding="utf-8")
            last_size = 0
        line = await f.readline()
        if not line:
            last_size = size
            await asyncio.sleep(0.1)
            continue
        m = CHAT_REGEX.search(line)
        if m:
            event = {
                "time": m.group("time"),
                "player": m.group("player"),
                "message": m.group("message")
            }
            print(json.dumps(event, ensure_ascii=False))
