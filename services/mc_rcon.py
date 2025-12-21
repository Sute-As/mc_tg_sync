import asyncio
from mcrcon import MCRcon
from config import RCON_HOST, RCON_PORT, RCON_PASSWORD
from utils.db import db_logger


def _send_sync(user: str, text: str):
    text_protect = text.replace('"', '\\"').replace('\\', '\\\\')
    json_payload = (
        f'["",'
        f'{{"text":"[TG] ","color":"aqua","bold":true}},'
        f'{{"text":"{user}","color":"gold"}},'
        f'{{"text":": {text_protect}","color":"white"}}'
        f']'
    )
    command = f'/tellraw @a {json_payload}'
    try:
        with MCRcon(RCON_HOST, RCON_PASSWORD, port=RCON_PORT) as mcr:
            mcr.command(command)
    except Exception as e:
        print(f"❌ RCON Error: {e}")


async def send_message(user: str, text: str):
    await db_logger.log_message(source="telegram", user=user, message=text)
    await asyncio.to_thread(_send_sync, user, text)