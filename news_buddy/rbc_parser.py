from datetime import date
from typing import Dict

import bs4 as bs
from requests import get

import utils

URL = "https://www.rbc.ru/"


def parse_rbc(url=URL) -> Dict:
    digest = {}
    page = get(url)
    soup = bs.BeautifulSoup(page.text, "html.parser")
    wrapper = soup.find("div", {"class": "main js-main-reload"})
    big_link = wrapper.find("a", {"class": "main__big__link js-yandex-counter"})
    digest[big_link["href"]] = big_link.span.text.strip()
    small_news = soup.find_all("a", {"class": "main__feed__link js-yandex-counter"})
    for block in small_news:
        digest[block["href"]] = block.span.text.strip()
    return digest


if __name__ == "__main__":
    name = 'RBC.ru'
    digest = parse_rbc()
    print(utils.get_md_message_unified(name, digest))
