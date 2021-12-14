from datetime import date
from itertools import chain
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

# Читают сейчас
# https://habr.com/kek/v2/articles/most-reading?fl=ru&hl=ru
#
# Новости
# https://habr.com/kek/v2/news/context?fl=ru&hl=ru&context_hub_alias=itcompanies&extend_context=false&per_page=5&page_num=1
#
# Вклвд в хаб
# https://habr.com/kek/v2/companies/top/by_hub/itcompanies


def get_title_and_link(article: str) -> Tuple:
    if article.find("a", {"class": "tm-article-snippet__title-link"}) == None:
        link_wrapper = article.find(
            "a", {"class": "tm-megapost-snippet__link tm-megapost-snippet__card"}
        )
        title = link_wrapper.find("h2").text
    else:
        link_wrapper = article.find("a", {"class": "tm-article-snippet__title-link"})
        title = link_wrapper.find("span").text

    link = URL[:-8] + link_wrapper["href"]
    return link, title


def parse_habr(top="/top/daily", hubs=HUBS) -> Dict:
    digest = {}
    for hub in HUBS.keys():
        link = URL + hub + top
        page = get(link)
        soup = bs.BeautifulSoup(page.text, "html.parser")
        articles_list = soup.find_all("article", {"class": "tm-articles-list__item"})
        articles_list = [x for x in articles_list if x != None]
        hub_arts = list(map(get_title_and_link, articles_list))
        if hub_arts:
            digest[hub] = hub_arts
    return digest


def get_md_message_habr(digest: dict) -> str:
    # FIXME: Occasionally there is troubles with pretty printing titles and links to articles
    today = date.today().strftime("%d.%m.%y")
    message = f"Дайджест хабр от {today}\n\n\n"
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
