from typing import Dict
from requests import get
import bs4 as bs
from unicodedata import normalize
from datetime import date
from pprint import pprint

URL = "https://www.rbc.ru/"


def parse_rbc() -> Dict:
    digest = {}
    page = get(URL)
    soup = bs.BeautifulSoup(page.text, "html.parser")
    wrapper = soup.find("div", {"class": "main js-main-reload"})

    big_link = wrapper.find("a", {"class": "main__big__link js-yandex-counter"})
    digest[big_link["href"]] = big_link.span.text.strip()

    small_news = soup.find_all("a", {"class": "main__feed__link js-yandex-counter"})
    for block in small_news:
        digest[block["href"]] = block.span.text.strip()
    return digest


def get_md_message(digest: dict) -> str:
    today = date.today().strftime("%d.%m.%y")
    message = f"Дайджест РБК от {today}\n\n\n"
    for key in digest:
        tmp = f"--  [{digest[key]}]({key})\n\n"
        message += tmp
    return message


if __name__ == "__main__":
    digest = parse_rbc()
    print(get_md_message(digest))
