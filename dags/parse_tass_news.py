import time
from datetime import datetime

from airflow import DAG
from airflow.operators.python import PythonOperator
from requests import post

import utils


TASS_API_LINK = "https://tass.ru/userApi/getNewsFeed"
TABLE = "news_tass"


def get_news():
    digest = {}
    news = post(
        TASS_API_LINK, json={"limit": 15, "timestamp": round(time.time())}
    ).json()
    for n in news["newsList"]:
        digest["https://tass.ru" + n["link"]] = " ".join([n["title"], n["subtitle"]])
    return digest


with DAG(
    "parse_tass_news",
    start_date=datetime(2021, 11, 20),
    catchup=False,
    schedule_interval="*/10 * * * *",
) as dag:

    parse_news = PythonOperator(task_id="parse_news", python_callable=get_news)

    fetch_old_news = PythonOperator(
        task_id="fetch_old_news",
        python_callable=utils.get_old_news,
        op_kwargs={"table": TABLE},
    )

    return_fresh = PythonOperator(
        task_id="return_fresh_news",
        python_callable=utils.db_write_only_new,
        op_kwargs={"table": TABLE},
    )

    [parse_news, fetch_old_news] >> return_fresh
