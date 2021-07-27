from telebot import TeleBot
import habr_parser

with open("token.txt", "r") as f:
    TOKEN = f.readline()

bot = TeleBot(TOKEN)


@bot.message_handler(commands=["digest"])
def start(message):
    data = habr_parser.parse()
    print(data)
    bot.send_message(message.chat.id, str(data))


bot.polling()
