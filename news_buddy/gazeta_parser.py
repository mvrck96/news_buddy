from typing import Dict
from unicodedata import normalize

import bs4 as bs
from requests import get

import utils

URL = "https://www.gazeta.ru/"


def parse_gazeta(url=URL) -> Dict:
    digest = {}
    page = get(url)
    soup = bs.BeautifulSoup(page.text, "html.parser")
    main_wrapper = soup.find("div", {"class": "b_main"})
    news_wrappers = main_wrapper.find_all("div", {"class": "b_ear-title"})
    for block in news_wrappers:
        digest[url[:-1] + block.a["href"]] = normalize("NFKD", block.a.text).strip()
    return digest


if __name__ == "__main__":
    name = "Gazeta.ru"
    digest = parse_gazeta()
    print(utils.get_md_message_unified(name, digest))
