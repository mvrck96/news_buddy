from datetime import date
from typing import Dict, Tuple

import bs4 as bs
from requests import get

# from telegram.utils.helpers import escape_markdown


URL = "https://habr.com/ru/hub/"
HUBS = {
    "startuprise": "Развитие стартапа",
    "python": "Python",
    "finance": "Финансы в IT",
    "machine_learning": "Машинное обучение",
    "data_mining": "Data Mining",
    "bidata": "Big Data",
    "venturecap": "Венчурные ивестиции",
    "statistics": "Статистика в ИТ",
    "infosecurity": "Информационная безопасность",
    "health": "Здоровье",
    "read": "Читальный зал",
}


def get_title_and_link(article: str) -> Tuple:
    link_wrapper = article.find("a", {"class": "tm-article-snippet__title-link"})
    link = URL[:-8] + link_wrapper["href"]
    title = link_wrapper.find("span").text
    return link, title


def parse_habr(top="/top/daily", hubs=HUBS) -> Dict:
    # TODO: Добавить фильтрацию статей
    #       Например, если статья попадается в Python, то её не надо    показывать в ML
    digest = {}
    for hub in hubs.keys():
        link = URL + hub + top
        page = get(link)
        soup = bs.BeautifulSoup(page.text, "html.parser")
        articles_list = soup.find_all("article", {"class": "tm-articles-list__item"})
        hub_arts = list(map(get_title_and_link, articles_list))
        if hub_arts:
            digest[hub] = hub_arts
    return digest


def get_md_message_habr(digest: dict) -> str:
    # FIXME: Иногда, ссылка на статью выводится не корректно вместе со скобками
    today = date.today().strftime("%d.%m.%y")
    message = f"Вечерний дайджест хабр от {today}\n\n\n"
    for key in digest:
        tmp = f"*{HUBS[key]}*\n"
        for item in digest[key]:
            tmp += f"--  [{item[1]}]({item[0]})\n"
        tmp += "\n"
        message += tmp
    return message


if __name__ == "__main__":
    print("Parsing . . .")
    data = parse_habr(top="/top/daily")
    message = get_md_message_habr(data)
    print(message)
