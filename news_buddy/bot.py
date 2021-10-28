from loguru import logger
from telebot import TeleBot
from telegram import ParseMode

import gazeta_parser
import habr_parser
import rbc_parser
import tass_parser
import utils

with open("token.txt", "r") as f:
    TOKEN = f.readline().strip()

bot = TeleBot(TOKEN)
utils.log_create_file()
logger.info("Bot is up !")
utils.db_connect()

@bot.message_handler(commands=["habr"])
def habr_digest(message) -> None:
    source = "Habr.com"
    user = utils.get_user(message)
    logger.debug(f"Starting parsing {source}")
    bot.send_message(chat_id=message.chat.id, text="Gathering news for you !")
    data = habr_parser.parse_habr(top="/top/daily")
    digest = habr_parser.filter_digest(data)
    post = habr_parser.get_md_message_habr(digest)
    bot.send_message(
        chat_id=message.chat.id,
        text=post,
        parse_mode=ParseMode.MARKDOWN,
        disable_web_page_preview=True,
    )
    utils.log_digest(source, user)


@bot.message_handler(commands=["rbc"])
def rbc_digest(message) -> None:
    source = "Rbc.ru"
    user = utils.get_user(message)
    digest = rbc_parser.get_main_news()
    post = utils.get_md_message_unified(source, digest)
    bot.send_message(
        chat_id=message.chat.id,
        text=post,
        parse_mode=ParseMode.MARKDOWN,
        disable_web_page_preview=True,
    )
    utils.log_digest(source, user)


@bot.message_handler(commands=["gazeta"])
def gazeta_digest(message) -> None:
    source = "Gazeta.ru"
    user = utils.get_user(message)
    digest = gazeta_parser.parse_gazeta()
    post = utils.get_md_message_unified(source, digest)
    bot.send_message(
        chat_id=message.chat.id,
        text=post,
        parse_mode=ParseMode.MARKDOWN,
        disable_web_page_preview=True,
    )
    utils.log_digest(source, user)

@bot.message_handler(commands=["tass"])
def tass_live_digest(message) -> None:
    source = "Tass.ru"
    user = utils.get_user(message)
    digest = tass_parser.get_live_news()
    post = utils.get_md_message_unified(source, digest)
    bot.send_message(
        chat_id=message.chat.id,
        text=post,
        parse_mode=ParseMode.MARKDOWN,
        disable_web_page_preview=True,
    )
    utils.log_digest(source, user)


@bot.message_handler(func=utils.check_invalidity)
def unsupported_reply(message) -> None:
    user = utils.get_user(message)
    bot.send_message(
        chat_id=message.chat.id,
        text="Sorry, no supported comands except:\n`/help`, `/habr`, `/rbc`, `/gazeta`",
        parse_mode=ParseMode.MARKDOWN,
    )
    utils.log_unsupported(user)


@bot.message_handler(commands=["start", "help"])
def helping_greeting(message) -> None:
    user = utils.get_user(message)
    help_message = """
    Hi, this is *News buddy*. I can send you news from:\n habr.com, gazeta.ru and rbc.ru\n\n -  To check top daily posts from selected hubs of habr.com \nsend me `/habr`\n-  If you want hot news from rbc.ru send `/rbc`\n-  For top news from gazeta.ru type `/gazeta`
    """
    bot.send_message(
        chat_id=message.chat.id, parse_mode=ParseMode.MARKDOWN, text=help_message
    )
    utils.log_help(user)


bot.polling()

logger.critical("! ! ! Bot is down ! ! !")
