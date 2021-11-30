import psycopg2 as ps
from os import getenv
import streamlit as st
import models

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


def get_top_news(conn, table, count=5):
    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT link, title, to_char(time, 'HH24:MI') FROM {table_name}
            ORDER BY time DESC
            LIMIT {count};
            """.format(
                table_name=table, count=count
            )
        )
        return cur.fetchall()

def get_24hour_news(conn, table):
    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT title FROM {table_name}
            WHERE time >= NOW() - INTERVAL '24 HOURS';
            """.format(
                table_name=table
            )
        )
        return cur.fetchall()

def print_news(conn, source, counter):
    news = get_top_news(conn, source, counter)
    for n in news:
        st.markdown(f"- [{n[1]}]({n[0]}) @ {n[2]}")


def get_24h_keywords(conn, table):
    kw = models.get_keywords(conn, table)
    for k in kw:
        st.markdown(f"- {k}")