import time
from datetime import datetime

import pandas as pd
from airflow import DAG
from airflow.hooks.postgres_hook import PostgresHook
from airflow.operators.python import PythonOperator
from requests import post, get
import bs4 as bs

TASS_API_LINK = "https://tass.ru/userApi/getNewsFeed"


def get_live_news() -> dict:
    digest = {}
    news = post(
        TASS_API_LINK, json={"limit": 15, "timestamp": round(time.time())}
    ).json()  # Есть варик регулировать кол-во новостей через параметр limit
    for n in news["newsList"]:
        digest["https://tass.ru" + n["link"]] = n["title"]
    return digest


def saver(ti):
    digest = ti.xcom_pull(task_ids="tass_parser")

    query = """
        INSERT INTO news_tass(title, link, time) 
        VALUES (%s, %s, %s);
    """
    for i in digest.items():
        pg_hook = PostgresHook(postgres_conn_id="my_postgres_connection")
        pg_hook.run(query, parameters=(i[0], i[1], str(datetime.today())))


with DAG(
    "parse_news",
    start_date=datetime(2021, 11, 19),
    schedule_interval="*/10 * * * *",
    catchup=False,
) as dag:

    get_tass_news = PythonOperator(task_id="tass_parser", python_callable=get_live_news)


    save_news = PythonOperator(task_id="save_news_postgres", python_callable=saver)

get_tass_news >> save_news
