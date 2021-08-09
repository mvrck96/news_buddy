from datetime import date
from typing import Dict
from loguru import logger


def get_md_message_unified(name: str, digest: dict) -> str:
    today = date.today().strftime("%d.%m.%y")
    message = f"{name} картина дня от {today}\n\n\n"
    for key in digest:
        tmp = f"--  [{digest[key]}]({key})\n\n"
        message += tmp
    return message


def not_habr(message: str) -> bool:
    return (
        True
        if str(message).strip().lower() in ["habr", "start", "help", "rbc", "gazeta"]
        else False
    )

def get_user(message: object) -> Dict:
    id_ = message.from_user.id
    username = message.from_user.username
    fname = message.from_user.first_name
    lname = message.from_user.last_name
    return {'id': id_, 'username': username, 'first_name': fname, 'last_name': lname}

def log_digest(source: str, user:dict) -> None:
    logger.info(f"{source} digest shipped for {user['username']}, id:{user['id']}")


if __name__ == "__main__":
    print(__file__)
