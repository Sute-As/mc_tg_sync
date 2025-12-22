import asyncio
from rcon.source import rcon
from config import RCON_HOST, RCON_PORT, RCON_PASSWORD
from utils.db import db_logger


async def send_message(user: str, text: str):
    await db_logger.log_message(source="telegram", user=user, message=text)
    text_protect = text.replace('"', '\\"').replace('\\', '\\\\')
    json_payload = (
        f'["",'
        f'{{"text":"[TG] ","color":"aqua","bold":true}},'
        f'{{"text":"{user}","color":"gold"}},'
        f'{{"text":": {text_protect}","color":"white"}}'
        f']'
    )
    command = f'tellraw @a {json_payload}'

    try:
        await rcon(
            command,
            host=RCON_HOST,
            port=int(RCON_PORT),
            passwd=RCON_PASSWORD,
            timeout=5
        )
    except Exception as e:
        print(f"RCON Error: {e}")