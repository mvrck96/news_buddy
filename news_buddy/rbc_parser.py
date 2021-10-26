from typing import Dict
import bs4 as bs
from requests import get
import utils

RBC_API_LINK = "https://www.rbc.ru/v10/ajax/main/region/world/publicher/main_main"


def get_main_news() -> Dict:
    digest = {}
    news = get(RBC_API_LINK).json()
    for n in news["items"]:
        s = bs.BeautifulSoup(n["html"], "html.parser")
        digest[s.a["href"].split("?")[0]] = s.span.text.strip()
    return digest


if __name__ == "__main__":
    name = "RBC.ru"
    digest = get_main_news()
    print(utils.get_md_message_unified(name, digest))
