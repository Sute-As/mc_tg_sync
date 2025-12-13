import telebot
import mc_rcon

TOKEN = "8153960157:AAG_Dbls0LPpZUO2pPbLnVdvDYXycUmv5nI"

bot = telebot.TeleBot(TOKEN)
grps = set()

@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id, "Привет! Я бот синхронизирующий чаты группы тг и сервера в маинкрафте\n Чтобы я начал свою работу добавь меня в группу и напиши !add")

@bot.message_handler(func=lambda message: message.chat.type in ['group', 'supergroup'])
def new_message(message):
    if (message.chat.id not in grps and message.text == "!add"):
        bot.send_message(message.chat.id, "Группа добавлена в отслеживаемые группы")
        grps.add(message.chat.id)
    if (message.chat.id not in grps):
        return
    try:
        mc_rcon.send_message(message.from_user.username, message.text)         
    except Exception:
        bot.send_message(message.chat.id, "Возникла ошибка при попытке отправить сообщение в чат маинкрафта")

@bot.message_handler(func=lambda message: True)
def read_all_messages(message):
    bot.reply_to(message, f"Ты сказал: {message.text}")

def get_message_form_rcon(user: str, text: str):
    if not text:
        return
    for grp in grps:
        bot.send_message(grp, f"{user} said {text}")

bot.polling(non_stop=True)