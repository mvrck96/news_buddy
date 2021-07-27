from telebot import TeleBot
import habr_parser
from telegram import ParseMode

with open("token.txt", "r") as f:
    TOKEN = f.readline().strip()

bot = TeleBot(TOKEN)


@bot.message_handler(commands=["habr"])
def start(message):
    data = habr_parser.parse_habr(top="/top/daily")
    post = habr_parser.get_md_message(data)
    bot.send_message(
        # chat_id="@mvrck_hood",
        chat_id=message.chat.id,
        text=post,
        parse_mode=ParseMode.MARKDOWN,
        disable_web_page_preview=True,
    )


bot.polling()
