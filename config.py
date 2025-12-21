import os
from dotenv import load_dotenv
import sys

load_dotenv()

TG_TOKEN = os.getenv("TG_TOKEN")

RCON_HOST = os.getenv("RCON_HOST", "localhost")
RCON_PORT = int(os.getenv("RCON_PORT", 25575))
RCON_PASSWORD = os.getenv("RCON_PASSWORD")

if not RCON_PASSWORD:
    raise ValueError("RCON_PASSWORD must be set")

CH_HOST = os.getenv("CH_HOST", "localhost")
CH_PORT = int(os.getenv("CH_PORT", 8123))
CH_USER = os.getenv("CH_USER", "default")
CH_PASSWORD = os.getenv("CH_PASSWORD", "")
CH_DB = os.getenv("CH_DB", "minecraft_chat")

missing_vars = []
if not TG_TOKEN:
    missing_vars.append("TG_TOKEN")
if not RCON_PASSWORD:
    missing_vars.append("RCON_PASSWORD")

if missing_vars:
    print(f"В файле .env нет: {', '.join(missing_vars)}")
    sys.exit(1)