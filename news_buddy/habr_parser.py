from itertools import chain

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
    # FIXME: Occasionally there is troubles with pretty printing titles and links to articles
    today = date.today().strftime("%d.%m.%y")
    message = f"Вечерний дайджест хабр от {today}\n\n\n"
    for key in digest:
        tmp = f"*{HUBS[key]}*\n"
        for item in digest[key]:
            tmp += f"--  [{item[1]}]({item[0]})\n"
        tmp += "\n"
        message += tmp
    return message


def filter_digest(digest: Dict) -> Dict:
    filtered_digest = {}
    for key, value in digest.items():
        filtered_digest[key] = []
        for tup in value:
            if tup not in chain(*filtered_digest.values()):
                filtered_digest[key].append(tup)
    filtered_digest = {
        key: value for key, value in filtered_digest.items() if value != []
    }
    return filtered_digest


if __name__ == "__main__":
    print("Parsing . . .")
    data = parse_habr(top="/top/daily")
    dg = filter_digest(data)
    message = get_md_message_habr(dg)
    print(message)
