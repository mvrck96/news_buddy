from datetime import datetime

from loguru import logger
from telebot import TeleBot
from telegram import ParseMode, chat, parsemode

import gazeta_parser
import habr_parser
import rbc_parser
import utils

with open("token.txt", "r") as f:
    TOKEN = f.readline().strip()

bot = TeleBot(TOKEN)
logger.info("Bot is up !")


@bot.message_handler(commands=["habr"])
def habr_digest(message) -> None:
    logger.debug("Starting parsing habr.com")
    bot.send_message(chat_id=message.chat.id, text="Gathering news for you !")
    data = habr_parser.parse_habr(top="/top/daily")
    post = habr_parser.get_md_message_habr(data)
    bot.send_message(
        chat_id=message.chat.id,
        text=post,
        parse_mode=ParseMode.MARKDOWN,
        disable_web_page_preview=True,
    )
    logger.info("Habr digest shipped")


@bot.message_handler(commands=["rbc"])
def rbc_digest(message) -> None:
    digest = rbc_parser.parse_rbc()
    post = utils.get_md_message_unified('Rbc.ru', digest)
    bot.send_message(
        chat_id=message.chat.id,
        text=post,
        parse_mode=ParseMode.MARKDOWN,
        disable_web_page_preview=True,
    )
    name = message.from_user.first_name
    logger.info("Rbc digest shipped", name)


@bot.message_handler(commands=["gazeta"])
def gazeta_digest(message) -> None:
    digest = gazeta_parser.parse_gazeta()
    post = utils.get_md_message_unified('Gazeta.ru', digest)
    bot.send_message(
        chat_id=message.chat.id,
        text=post,
        parse_mode=ParseMode.MARKDOWN,
        disable_web_page_preview=True,
    )
    logger.info("Gazeta digest shipped")


@bot.message_handler(func=utils.not_habr)
def base_reply(message) -> None:
    bot.send_message(
        chat_id=message.chat.id,
        text="Sorry, no supported comands except `/help`, `/habr`, `/rbc`, `/gazeta`",
        parse_mode=ParseMode.MARKDOWN,
    )
    logger.info("No suitable command found")


@bot.message_handler(commands=["start", "help"])
def helping_greeting(message) -> None:
    help_message = """
    Hi, this is *News buddy*. I can send you news from:\n habr.com, gazeta.ru and rbc.ru\n\n -  To check top daily posts from selected hubs of habr.com send me `/habr`\n-  If you want hot news from rbc.ru send `/rbc`\n-  For top news from gazeta.ru type `/gazeta`
    """
    bot.send_message(
        chat_id=message.chat.id, parse_mode=ParseMode.MARKDOWN, text=help_message
    )
    logger.info("Help message shipped")


bot.polling()
