import os
from datetime import date
from datetime import datetime
from typing import Dict

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
    return {"id": id_, "username": username, "first_name": fname, "last_name": lname}


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
    connection = ps.connect(
        dbname="newsbuddy_db",
        user="postgres",
        password="postgres",
        host="postgres",
        port=5432,
    )
    connection.autocommit = True
    logger.info(f"Connection to localhost:newsbuddy_db opened")
    return connection


def db_get_news(conn, table: str) -> Dict:
    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT link, title FROM {table_name};
        """.format(
                table_name=table
            )
        )
        return dict(cur.fetchall())


def db_write_news(conn, table: str, news: dict) -> None:
    olds = db_get_news(conn, table)
    fresh = [n for n in news.items() if n[0] not in olds.keys()]
    for f in fresh:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO {table_name} (title, link, time) 
                VALUES ('{title}', '{link}', '{time}')
                """.format(
                    table_name=table, title=f[1], link=f[0], time=datetime.today()
                )
            )
    logger.info(f"{len(fresh)} items added to {table}")


def db_close(conn):
    conn.close()
    logger.info("Connection closed ! ! !")


if __name__ == "__main__":
    print(__file__)
