import os
from datetime import datetime
from string import punctuation

import nltk
import psycopg2 as ps
import yake
from airflow import DAG
from airflow.hooks.postgres_hook import PostgresHook
from airflow.operators.python import PythonOperator

nltk.download("stopwords")
from nltk.corpus import stopwords
from pymystem3 import Mystem

table = "news_tass"

def get_titles(table: str):
    connection = ps.connect(
        dbname="maverick",
        user="maverick",
        password="maverick",
        port=5432,
        host="localhost",
    )
    connection.autocommit = True
    with connection.cursor() as cur:
        cur.execute(
            f"""
            SELECT title FROM {table}
            WHERE time >= NOW() - INTERVAL '24 HOURS';
            """
        )
        return cur.fetchall()


def preprocess_text(text: str) -> str:
    mystem = Mystem()
    russian_stopwords = stopwords.words("russian")
    tokens = mystem.lemmatize(text.lower())
    tokens = [
        token
        for token in tokens
        if token not in russian_stopwords
        and token != " "
        and token.strip() not in punctuation
    ]
    text = " ".join(tokens)
    return text


def generate_24h_keywords(ti):
    res = []
    sql_res = ti.xcom_pull(task_ids="get_titles")  # list [(a,), (b,), ...]

    titles = [x[0] for x in sql_res]
    pp_titles = [preprocess_text(x) for x in titles]

    extractor = yake.KeywordExtractor(lan="ru", n=1, top=5)
    kw = extractor.extract_keywords(". ".join(pp_titles))
    for k in kw:
         res.append(k[0])
    return res


def write_kw(ti, table: str):
    keywords = ti.xcom_pull(task_ids="genearet_kw")
    pg_hook = PostgresHook(postgres_conn_id="my_postgres_connection")
    for kw in keywords:
        pg_hook.run(
            """
            INSERT INTO keywords (word, table_name, time) VALUES (%s, %s, %s)
            """,
            parameters=(kw, table, datetime.now()),
        )


with DAG(
    "generate_24h_keywoards",
    start_date=datetime(2021, 12, 1),
    catchup=False,
    schedule_interval="*/30 * * * *"
) as dag:

    fetch_titles = PythonOperator(
        task_id="get_titles",
        python_callable=get_titles,
        op_kwargs={"table": table},
    )   
    generate_keywords = PythonOperator(
        task_id="genearet_kw", python_callable=generate_24h_keywords
    )   
    write_keywords = PythonOperator(
        task_id="write_kw_to_db", python_callable=write_kw, op_kwargs={"table": table}
    )   
    fetch_titles >> generate_keywords >> write_keywords