from telebot import TeleBot
import habr_parser
from telegram import ParseMode, chat

with open("token.txt", "r") as f:
    TOKEN = f.readline().strip()

bot = TeleBot(TOKEN)
print("Bot is live !!!")


@bot.message_handler(commands=["habr"])
def habr_digest(message):
    data = habr_parser.parse_habr(top="/top/daily")
    post = habr_parser.get_md_message(data)
    bot.send_message(
        chat_id=message.chat.id,
        text=post,
        parse_mode=ParseMode.MARKDOWN,
        disable_web_page_preview=True,
    )
    print("Habr digest shipped !")


def not_habr(message: str) -> bool:
    return False if message == "/habr" else True


@bot.message_handler(func=not_habr)
def base_reply(message):
    bot.send_message(
        chat_id=message.chat.id,
        text="Sorry, no supported comands except `/habr`",
        parse_mode=ParseMode.MARKDOWN,
    )


bot.polling()
