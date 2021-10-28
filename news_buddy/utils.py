import os
from datetime import date
from typing import Dict, Text

import psycopg2 as ps
from loguru import logger

COMMANDS = ["/start", "/help", "/habr", "/gazeta", "/rbc"]


def get_md_message_unified(name: str, digest: dict) -> str:
    today = date.today().strftime("%d.%m.%y")
    message = f"Новости к {today} от {name}\n\n\n"
    for key in digest:
        tmp = f"--  [{digest[key]}]({key})\n\n"
        message += tmp
    return message


def check_invalidity(message) -> bool:
    if str(message) not in COMMANDS:
        return True
    else:
        return False


def get_user(message: object) -> Dict:
    id_ = message.from_user.id
    username = message.from_user.username
    fname = message.from_user.first_name
    lname = message.from_user.last_name
    # is_scam = message.from_user.scam
    # phone = message.from_user.phone
    # status = message.from_user.status
    # lang_code = message.from_user.lang_code
    return {
        "id": id_,
        "username": username,
        "first_name": fname,
        "last_name": lname,
        # "is_scam": is_scam,
        # "phone": phone,
        # "status": status,
        # "lang_code": lang_code,
    }


def log_create_file() -> None:
    logger.add(
        "data/logs/log.json",
        format="{time} {level} {message}",
        level="TRACE",
        rotation="1 week",
        compression="tar.gz",
        serialize=True,
    )


def log_digest(source: str, user: dict) -> None:
    logger.info(f"{source} digest shipped for id:{user['id']}, {user['username']}")


def log_unsupported(user: dict) -> None:
    logger.info(
        f"Unsupported message recieved from id:{user['id']}, {user['username']}"
    )


def log_help(user: dict) -> None:
    logger.info(f"Help message send to id:{user['id']}, {user['username']}")


def db_connect():
    pass


def db_insert():
    pass


def db_connect():
    connection = ps.connect(dbname='newsbuddy_db',
                            user='postgres',
                            password='postgres', 
                            host='postgres', 
                            port=5432)
    connection.autocommit = True
    logger.info(f"Connection to localhost:newsbuddy_db opened")


if __name__ == "__main__":
    print(__file__)