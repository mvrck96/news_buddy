import sys

sys.path.append(".")

import bs4 as bs
from requests import get

from news_buddy.habr_parser import get_title_and_link, parse_habr

URL = "https://habr.com/ru/"


def test_get_title_and_link():
    link = URL + "company/ruvds/blog/top/"
    page = get(link)
    soup = bs.BeautifulSoup(page.text, "html.parser")
    to_test = soup.find("div", {"class": "tm-article-snippet"})
    assert type(get_title_and_link(to_test)) == tuple, "Not a tuple returned"


def test_parse_habr():
    # Тест не корректный !
    # Потому что не корректно написана функция. Надо перписывать модули парсинга :(
    assert parse_habr() == None, "I don't know how to write test !"
