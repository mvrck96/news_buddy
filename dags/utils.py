import os
from datetime import datetime

import psycopg2 as ps
from airflow.hooks.postgres_hook import PostgresHook
from dotenv import find_dotenv, load_dotenv


def get_old_news(table: str) -> dict:
    load_dotenv(find_dotenv())
    connection = ps.connect(
        dbname=os.environ.get("DB__DATABASE"),
        user=os.environ.get("DB__USER"),
        password=os.environ.get("DB__PASS"),
        host=os.environ.get("DB__HOST"),
        port=os.environ.get("DB__PORT"),
    )
    connection.autocommit = True
    with connection.cursor() as cur:
        cur.execute(
            f"""
            select title, link from {table};
            """
        )
        return dict(cur.fetchall())


def db_write_only_new(ti, table: str) -> None:
    pg_hook = PostgresHook(postgres_conn_id="my_local_postgres")
    olds = ti.xcom_pull(task_ids="fetch_old_news")
    news = ti.xcom_pull(task_ids="parse_news")

    fresh = [n for n in news.items() if n[1] not in olds.keys()]
    for f in fresh:
        pg_hook.run(
            "insert into " + table + " (title, link, time) values (%s, %s, %s)",
            parameters=(f[1], f[0], datetime.now()),
        )
