from requests import get
import bs4 as bs
from datetime import date

URL = "https://habr.com/ru/hub/"
HUBS = [
    "data_mining",
    "machine_learning",
    "startuprise",
    "read",
    "python",
    "finance",
    "infosecurity",
    "bidata",
    "gtd",
    "venturecap",
    "health",
    "statistics",
]


def get_title_and_link(article: str) -> list:
    link_wrapper = article.find("a", {"class": "tm-article-snippet__title-link"})
    link = URL[:-8] + link_wrapper["href"]
    title = link_wrapper.find("span").text
    return link, title


def pretty_digest(digest: dict) -> str:
    today = date.today().strftime("%d%m%y")
    pass


def parse():
    digest = {}
    for hub in HUBS:
        link = URL + hub + "/top/daily"
        page = get(link)
        soup = bs.BeautifulSoup(page.text, "lxml")
        articles_list = soup.find_all("article", {"class": "tm-articles-list__item"})
        hub_arts = list(map(get_title_and_link, articles_list))
        if hub_arts:
            digest[hub] = hub_arts
    return digest


if __name__ == "__main__":
    print(parse())
