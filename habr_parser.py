from requests import get
import bs4 as bs
from datetime import date

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
    "gtd": "GTD",
    "infosecurity": "Информационная безопасность",
    "health": "Здоровье",
    "read": "Читальный зал",
}


def get_title_and_link(article: str) -> list:
    link_wrapper = article.find("a", {"class": "tm-article-snippet__title-link"})
    link = URL[:-8] + link_wrapper["href"]
    title = link_wrapper.find("span").text
    return link, title


def pretty_digest(digest: dict) -> str:
    today = date.today().strftime("%d%m%y")
    pass


def parse_habr(top="/top/daily") -> dict:
    digest = {}
    for hub in HUBS.keys():
        link = URL + hub + top
        page = get(link)
        soup = bs.BeautifulSoup(page.text, "lxml")
        articles_list = soup.find_all("article", {"class": "tm-articles-list__item"})
        hub_arts = list(map(get_title_and_link, articles_list))
        if hub_arts:
            digest[hub] = hub_arts
    return digest


def get_md_message(digest: dict) -> str:
    today = date.today().strftime("%d.%m.%y")
    message = f"Вечерний дайджест хабр от _{today}_\n\n\n"
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
    message = get_md_message(data)
    print(message)
