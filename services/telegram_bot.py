import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from config import TG_TOKEN
from services import mc_rcon
from utils.db import db_logger

bot = Bot(token=TG_TOKEN)
dp = Dispatcher()
grps: set[int] = set()
users: dict[str, str] = {}


async def broadcast_logs(bot: Bot, queue: asyncio.Queue):
    while True:
        player, message_text = await queue.get()
        formatted_text = f"👤 <b>{player}</b>: {message_text}"
        active_groups = grps.copy()
        for chat_id in active_groups:
            try:
                await bot.send_message(chat_id, formatted_text, parse_mode="HTML")
            except Exception as e:
                print(f"Ошибка отправки в группу {chat_id}: {e}")


@dp.message(Command("start"))
async def start(message: types.Message):
    ans = (
        "👋 <b>Привет! Я синхронизатор чата</b>\n\n"
        "🤖 Я соединяю чат Telegram и сервер Minecraft.\n\n"
        "<b>Инструкция:</b>\n"
        "1️⃣ Добавь меня в группу\n"
        "2️⃣ Напиши <code>!add</code> в чате группы\n"
        "3️⃣ Привяжи ник командой <code>/connect ник</code>\n\n"
        "<i>Удачной игры!</i>"
    )
    await message.answer(ans, parse_mode="HTML")


@dp.message(Command("stat"))
async def stat(message: types.Message):
    username = message.from_user.username
    if (username is None):
        username = message.from_user.full_name
    inf = users.get(username)
    if not inf:
        await message.answer("❓ <b>Упс!</b> Статистика не найдена. Начни общаться!")
    else:
        res = (
            f"📊 <b>КАРТОЧКА ИГРОКА</b>\n"
            f"━━━━━━━━━━━━━━━━━━\n"
            f"👤 <b>Профиль:</b> @{username}\n"
            f"🎮 <b>Ник в MC:</b> <code>{inf['mnname']}</code>\n"
            f"✉️ <b>Сообщений:</b> <code>{inf['count']}</code>\n"
            f"━━━━━━━━━━━━━━━━━━"
        )
        await message.answer(res, parse_mode="HTML")

@dp.message(Command("connect"))
async def con(message: types.Message):
    username = message.from_user.username
    if username is None:
        username = message.from_user.full_name
    inf = users.get(username)
    if not inf:
        await message.answer(f"Нет информации о данном пользователе")
    else:
        txt = message.text[8:].strip()
        if not txt:
            await message.answer("⚠️ <b>Ошибка:</b> укажите ник!\nПример: <code>/connect Steve</code>", parse_mode="HTML")
        else:
            inf["mnname"] = txt
            await db_logger.update_user(username, txt, inf["count"])
            await message.answer(f"✅ <b>Успешно!</b>\nВы играете под ником: <code>{txt}</code>", parse_mode="HTML")


@dp.message(F.chat.type.in_({"group", "supergroup"}))
async def group_message(message: types.Message):
    if message.text == "!add":
        if message.chat.id not in grps:
            grps.add(message.chat.id)
            await db_logger.save_group(message.chat.id)
            await message.answer(f"🌐 <b>Группа подключена!</b>\nЧат сервера синхронизирован с <b>{message.chat.title}</b>", parse_mode="HTML")
        return
    if message.chat.id not in grps:
        return
    try:
        username = message.from_user.username
        if username not in users:
            users[username] = {"mnname": "Неизвестен", "count": 1}
        else:
            users[username]["count"] += 1
        asyncio.create_task(db_logger.update_user(username, users[username]["mnname"], users[username]["count"]))
        text = message.text
        for i in range(0, len(text), 256):
            part = text[i:i + 256]
            await mc_rcon.send_message(username, part)

    except Exception as e:
        print(f"Ошибка в обработке сообщения: {e}")