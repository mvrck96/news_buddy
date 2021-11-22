from datetime import datetime
from unicodedata import normalize

import bs4 as bs
from airflow import DAG
from airflow.operators.python import PythonOperator
from requests import get

import utils

GAZETA_API_LINK = "https://www.gazeta.ru/"
TABLE = "news_gazeta"


def get_news() -> dict:
    digest = {}
    page = get(GAZETA_API_LINK)
    soup = bs.BeautifulSoup(page.text, "html.parser")
    main_wrapper = soup.find("div", {"class": "b_main"})
    news_wrappers = main_wrapper.find_all("div", {"class": "b_ear-title"})
    for block in news_wrappers:
        digest[GAZETA_API_LINK[:-1] + block.a["href"]] = normalize(
            "NFKD", block.a.text
        ).strip()
    return digest


with DAG(
    "parse_gazeta_news",
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
