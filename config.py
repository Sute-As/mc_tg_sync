import os
from dotenv import load_dotenv

load_dotenv()

RCON_HOST = os.getenv("RCON_HOST", "localhost")
RCON_PORT = int(os.getenv("RCON_PORT", 25575))
RCON_PASSWORD = os.getenv("RCON_PASSWORD")

if not RCON_PASSWORD:
    raise ValueError("RCON_PASSWORD must be set")