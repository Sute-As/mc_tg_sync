from mcrcon import MCRcon
from config import RCON_HOST, RCON_PORT, RCON_PASSWORD
import asyncio


def send_to_minecraft(user: str, text: str):
    text_protect = text.replace('"', '\\"').replace('\\', '\\\\')
    user_protect = user.replace('"', '\\"').replace('\\', '\\\\')
    json_payload = (
        f'["",' 
        f'{{"text":"[TG] ","color":"aqua","bold":true}},' 
        f'{{"text":"{user_protect}","color":"gold"}},' 
        f'{{"text":": {text_protect}","color":"white"}}' 
        f']'
    )
    command = f'/tellraw @a {json_payload}'
    try:
        with MCRcon(host=RCON_HOST, port=RCON_PORT, password=RCON_PASSWORD) as mcr:
            response = mcr.command(command)
    except ConnectionRefusedError:
        print('ConnectionRefusedError')
    except Exception as e:
        print(f"RCON error: {e}")


async def send_message(user: str, text: str):
    await asyncio.to_thread(send_to_minecraft, user, text)