# News buddy --> live at [@newsbuddy](https://t.me/mvrck_bot)

Персональный помощник в мире российского новостного потока. Может присылать последние новости по клику, аггрегировать хабр, скоро будут красивые инфо дашборды и суммаризация

## Стек

- `python3.8` - universal glue
- `PostgreSQL` + `psycopg2` - хранение данных
- `Docker` + `docker-compose` - контейнеризация для простоты разработки и деплоя
- `airflow` - Extraction + Load
- `Telegram Bot API` - удобная апишка для бота
- `loguru` - удобное логирование

## Как запустить ?

- `git clone https://github.com/mvrck96/news_buddy.git && cd news_buddy`
- `cp example.env .env`
  - Вставить свой токен
- `sudo docker-compose up`

## `example.env`

- Все переменные которые начинаются с `_` это **НЕ** системные переменные
- Остальные где-то используются, например в докере для поднятия постгри

## TODO:

- Зарефакторить `bot.py`
- Добавить выбор хабов через `.env`
- Добавить более детальный учет действий бота
- Дашборды
- Суммаризация