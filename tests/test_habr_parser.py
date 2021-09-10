import sys

sys.path.append(".")

import bs4 as bs
from news_buddy import habr_parser 
from requests import get
import pytest

URL = "https://habr.com/ru/"


def test_get_title_and_link():
    link = URL + "company/ruvds/blog/top/"
    page = get(link)
    soup = bs.BeautifulSoup(page.text, "html.parser")
    to_test = soup.find("div", {"class": "tm-article-snippet"})
    assert type(habr_parser.get_title_and_link(to_test)) == tuple, "Not a tuple returned"


def test_parse_habr():
    # Тест не корректный !
    # Потому что не корректно написана функция. Надо перписывать модули парсинга :(
    assert habr_parser.parse_habr(top='/top/daily', hubs={}) == {}, "I don't know how to write test !"

@pytest.mark.parametrize('test_input, expected', [
    ({1: [(1, 1), (1, 2)], 2: [(1, 2), (2, 6)]}, {1: [(1, 1), (1, 2)], 2: [(2, 6)]}),
    ({1: [(1, 1), (1, 1), (1, 1)], 2: [(1, 1), (1, 1)]}, {1: [(1, 1)]}), 
    ({1: [(1, 2), (4, 2), (1, 3)]}, {1: [(1, 2), (4, 2), (1, 3)]}), 
    ({1: [], 2: [(2, 2)]}, {2: [(2, 2)]})])
def test_filter_digest(test_input, expected):
    assert habr_parser.filter_digest(test_input) == expected