import os
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from config import TG_TOKEN
from services import mc_rcon
from utils.db import db_logger

bot = Bot(token=TG_TOKEN)
dp = Dispatcher()
grps: set[int] = set()
users: dict[str, str] = {}


@dp.message(Command("start"))
async def start(message: types.Message):
    ans = "Привет! Я бот синхронизирующий чаты группы тг и сервера в майнкрафте\n"
    ans += "Чтобы я начал свою работу добавь меня в группу и напиши !add"
    await message.answer(ans)

@dp.message(Command("stat"))
async def stat(message: types.Message):
    username = message.from_user.username
    if (username is None):
        username = message.from_user.full_name
    inf = users.get(username)
    if not inf:
        await message.answer(f"Нет информации о данном пользователе")
    else:
        cntintg = inf["count"]
        mnname = inf["mnname"]
        await message.answer(f"Ник пользователя в маинкрафте:{mnname}\nКоличество отправленных сообщений на сервер: {cntintg}")

@dp.message(Command("connect"))
async def con(message: types.Message):
    username = message.from_user.username
    if (username is None):
        username = message.from_user.full_name
    inf = users.get(username)
    if not inf:
        await message.answer(f"Нет информации о данном пользователе")
    else:
        txt = message.text[8:].strip()
        if not txt:
            await message.answer(f"Имя не должно быть пустым")
        else:
            inf["mnname"] = txt
            await db_logger.update(username, txt, inf["count"])
            await message.answer(f"Информация успешно обновлена")


@dp.message(F.chat.type.in_({"group", "supergroup"}))
async def group_message(message: types.Message):
    if message.text == "!add":
        if message.chat.id not in grps:
            grps.add(message.chat.id)
            await db_logger.save_group(message.chat.id)
            await message.answer(f"Группа {message.chat.title} подключена!")
        return
    if message.chat.id not in grps:
        return
    try:
        username = message.from_user.username
        if username is None:
            username = message.from_user.full_name
        inf = users.get(username)
        if (not inf):
            await db_logger.update_user(username, "Неизвесетен", 1)
        else:
            await db_logger.update_user(username, inf["mnname"], inf["count"] + 1)
        text = message.text or ""
        if text.startswith("/"):
            return
        if text:
            i = 0
            while (i * 256 < len(text)):
                await mc_rcon.send_message(username, text[i * 256: min((i + 1) * 256, len(text))])
                i += 1
    except Exception as e:
        print(f"Ошибка отправки в MC: {e}")