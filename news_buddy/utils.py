from datetime import date
from typing import Dict, Text
from loguru import logger
import psycopg2 as ps

COMMANDS = ["/start", "/help", "/habr", "/gazeta", "/rbc"]


def get_md_message_unified(name: str, digest: dict) -> str:
    today = date.today().strftime("%d.%m.%y")
    message = f"{name} картина дня от {today}\n\n\n"
    for key in digest:
        tmp = f"--  [{digest[key]}]({key})\n\n"
        message += tmp
    return message


def check_invalidity(message) -> bool:
    if str(message).lower() not in COMMANDS:
        return True
    else:
        return False


def get_user(message: object) -> Dict:
    id_ = message.from_user.id
    username = message.from_user.username
    fname = message.from_user.first_name
    lname = message.from_user.last_name
    return {"id": id_, "username": username, "first_name": fname, "last_name": lname}


def log_digest(source: str, user: dict) -> None:
    logger.info(f"{source} digest shipped for {user['username']}, id:{user['id']}")


def db_connect():
    pass


def db_insert():
    pass


if __name__ == "__main__":
    print(__file__)