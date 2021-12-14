import time
from os import getenv
from loguru import logger
from telebot import TeleBot
from telegram import ParseMode


import habr_parser
import utils


TOKEN = getenv("_BOT_TOKEN")

bot = TeleBot(TOKEN)
utils.log_create_file()
logger.info("Bot is up !")

time.sleep(
    3
)  # wait a litle just not to recieve coonection errors, while db is initialising
conn = utils.db_connect()


# @bot.message_handler(commands=["habr"])
# def habr_digest(message) -> None:
#     source = "Habr.com"
#     user = utils.get_user(message)
#     logger.debug(f"Starting parsing {source}")
#     bot.send_message(chat_id=message.chat.id, text="Gathering news for you !")
#     data = habr_parser.parse_habr(top="/top/daily")
#     digest = habr_parser.filter_digest(data)
#     post = habr_parser.get_md_message_habr(digest)
#     bot.send_message(
#         chat_id=message.chat.id,
#         text=post,
#         parse_mode=ParseMode.MARKDOWN,
#         disable_web_page_preview=True,
#     )
#     utils.log_digest(source, user)


@bot.message_handler(commands=["help", "start"])
def helping_greeting(message) -> None:
    user = utils.get_user(message)
    help_message = """
    Hi, this is *news buddy*. I can send you news from:\n habr.com, gazeta.ru and rbc.ru\n\n -  To check top daily posts from selected hubs of habr.com \nsend me `/habr`\n-  If you want hot news from rbc.ru send `/rbc`\n-  For top news from gazeta.ru type `/gazeta`
    """
    bot.send_message(
        chat_id=message.chat.id, parse_mode=ParseMode.MARKDOWN, text=help_message
    )
    utils.log_help(user)


@bot.message_handler(func=utils.check_invalidity)
def unsupported_reply(message) -> None:
    user = utils.get_user(message)
    bot.send_message(
        chat_id=message.chat.id,
        text="Sorry, no supported comands except:\n`/help`, `/habr`, `/rbc`, `/gazeta`",
        parse_mode=ParseMode.MARKDOWN,
    )
    utils.log_unsupported(user)


bot.polling()

logger.critical("! ! ! Bot is down ! ! !")

utils.db_close(conn)
