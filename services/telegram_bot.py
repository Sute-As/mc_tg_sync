import os
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from config import TG_TOKEN
from services import mc_rcon
from typing import Any

bot = Bot(token=TG_TOKEN)
dp = Dispatcher()
grps: set[int] = set()
users: dict[str, dict[Any, Any]] = dict()


@dp.message(Command("start"))
async def start(message: types.Message):
    ans = "Привет! Я бот синхронизирующий чаты группы тг и сервера в майнкрафте\n"
    ans += "Чтобы я начал свою работу добавь меня в группу и напиши !add"
    await message.answer(ans)


@dp.message(F.chat.type.in_({"group", "supergroup"}))
async def group_message(message: types.Message):
    if message.text == "!add":
        if message.chat.id not in grps:
            grps.add(message.chat.id)
            await message.answer(f"Группа {message.chat.title} подключена!")
        return
    if message.chat.id not in grps:
        return
    try:
        username = message.from_user.username
        if not(username is None):
            if (username in users):
                users["username"]["count"] += 1
            else:
                users["username"]["count"] = 1
                users["username"]["mnname"] = " Неизвесетен"
        if username is None:
            username = message.from_user.full_name
        text = message.text or ""
        if text.startswith("/"):
            return
        if text:
            i = 0
            while (i * 256 < len(text)):
                await mc_rcon.send_message(username, text[i * 256: (i + 1) * 256])
                i += 1
    except Exception as e:
        print(f"Ошибка отправки в MC: {e}")


@dp.message(Command("stat"))
async def stat(message: types.Message):
    user = message.from_user.username
    if user is None:
        message.answer(f"Нет информации о данном пользователе")
    if user not in users:
        await message.answer(f"Нет информации о данном пользователе")
    else:
        cntintg = users[user]["count"]
        mnname = users[user]["mnname"]
        await message.answer(f"Ник пользователя в маинкрафте:{mnname}\nКоличество отправленных сообщений на сервер: {cntintg}")


@dp.message(Command("connect"))
async def connect(message: types.Message):
    user = message.from_user.username
    if user is None:
        await message.answer(f"Нет информации о данном пользователе")
    text = message.text[8:]
    users[user]["mnname"] = text
    await message.answer(f"Изменения успешны!")
    