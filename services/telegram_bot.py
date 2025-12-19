import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
import mc_rcon

bot = Bot(token=TOKEN)
dp = Dispatcher()
grps: set[int] = set()


@dp.message(Command("start"))
async def start(message: types.Message):
    ans = "Привет! Я бот синхронизирующий чаты группы тг и сервера в маинкрафте\n"
    ans += "Чтобы я начал свою работу добавь меня в группу и напиши !add"
    await message.answer(ans)


@dp.message(F.chat.type.in_({"group", "supergroup"}))
async def group_message(message: types.Message):
    if message.chat.id not in grps and message.text == "!add":
        grps.add(message.chat.id)
        await message.answer("Группа добавлена в отслеживаемые группы")
        return
    if message.chat.id not in grps:
        return
    try:
        username = message.from_user.username
        if (username is None):
            username = message.from_user.ful_name
        text = message.text or ""
        if text:
            mc_rcon.send_message(username, text)
    except Exception:
        await message.answer("Возникла ошибка при попытке отправить сообщение в чат Minecraft")


@dp.message()
async def read_all_messages(message: types.Message):
    await message.reply(f"Ты сказал: {message.text}")


async def get_message_from_rcon(user: str, text: str):
    if not text:
        return
    for grp in grps:
        await bot.send_message(grp, f"{user} сказал {text}")


async def main():
    await dp.start_polling(bot)


asyncio.run(main())