from typing import Dict
from requests import get
import bs4 as bs
from unicodedata import normalize
from datetime import date

URL = "https://www.gazeta.ru/"


def parse_gazeta() -> Dict:
    digest = {}
    page = get(URL)
    soup = bs.BeautifulSoup(page.text, "html.parser")
    main_wrapper = soup.find("div", {"class": "b_main"})
    news_wrappers = main_wrapper.find_all("div", {"class": "b_ear-title"})
    for block in news_wrappers:
        digest[URL[:-1] + block.a["href"]] = normalize("NFKD", block.a.text).strip()
    return digest


def get_md_message(digest: dict) -> str:
    today = date.today().strftime("%d.%m.%y")
    message = f"Gazeta.ru картина дня от {today}\n\n\n"
    for key in digest:
        tmp = f"--  [{digest[key]}]({key})\n\n"
        message += tmp
    return message


if __name__ == "__main__":
    digest = parse_gazeta()
    print(get_md_message(digest))
