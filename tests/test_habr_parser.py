# import sys
# sys.path.append("../")

from requests import get
import bs4 as bs

import habr_parser as parser


def test_get_title_and_link():
    url = "https://habr.com/ru/company/ruvds/blog/top/"
    page = get(url)
    soup = bs.BeautifulSoup(page.text, "html.parser")
    to_test = soup.find("div", {"class": "tm-article-snippet"})
    assert (
        type(parser.get_title_and_link(to_test)) == tuple
    ), "Not a tuple returned"


test_get_title_and_link()
