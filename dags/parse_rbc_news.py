from datetime import datetime

import bs4 as bs
from airflow import DAG
from airflow.operators.python import PythonOperator
from requests import get

import utils

RBC_API_LINK = "https://www.rbc.ru/v10/ajax/main/region/world/publicher/main_main"
TABLE = "news_rbc"


def get_news() -> dict:
    digest = {}
    news = get(RBC_API_LINK).json()
    for n in news["items"]:
        s = bs.BeautifulSoup(n["html"], "html.parser")
        digest[s.a["href"].split("?")[0]] = s.span.text.strip()
    return digest


with DAG(
    "parse_rbc_news",
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
