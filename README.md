# News buddy --> live at [@newsbuddy](https://t.me/mvrck_bot)

Персональный помощник в мире российского новостного потока. Может присылать последние новости по клику, аггрегировать хабр, скоро будут красивые инфо дашборды и суммаризация

## Стек

- `python3.8` - universal glue
- `Docker` + `docker-compose` - контейнеризация для простоты разработки и деплоя
- `PostgreSQL` + `psycopg2` - хранение данных
- `Telegram Bot API` - удобная апишка для бота
- `loguru` - удобное логирование
- `airflow` - Extraction + Load

## Как запустить ?

- `git clone https://github.com/mvrck96/news_buddy.git && cd news_buddy`
- `cp example.env .env`
  - Вставить свой токен
- `sudo docker-compose up`

## `example.env`

- Все переменные которые начинаются с `_` это **НЕ** системные переменные
- Остальные где-то используются, например в докере для поднятия постгри
