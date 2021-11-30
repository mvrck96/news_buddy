import nltk

nltk.download("stopwords")

from string import punctuation
from nltk.corpus import stopwords
from pymystem3 import Mystem
import utils as ut
import yake

import psycopg2 as ps


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


def get_keywords(conn, table: str) -> list:
    res = []
    titles_24hours = ut.get_24hour_news(conn, table)
    text_24hours = [x[0] for x in titles_24hours]
    pp_text_24hours = [preprocess_text(x) for x in text_24hours]

    extractor = yake.KeywordExtractor(lan="ru", n=1, top=5)
    kw = extractor.extract_keywords(". ".join(pp_text_24hours))
    for k in kw:
        res.append(k[0])
    return res


def db_connect():
    connection = ps.connect(
        # dbname=getenv("POSTGRES_DB"),
        # user=getenv("POSTGRES_USER"),
        # password=getenv("POSTGRES_PASSWORD"),
        # port=getenv("_POSTGRES_PORT"),
        # host="postgres_database",  # container name for postgres db, specified in docker-compose
        dbname="maverick",
        user="maverick",
        password="maverick",
        port=5432,
        host="localhost",
    )
    connection.autocommit = True
    return connection


if __name__ == "__main__":
    conn = db_connect()
    print(get_keywords(conn, "news_tass"))
