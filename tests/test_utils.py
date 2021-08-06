import sys

sys.path.append(".")

from datetime import date

from news_buddy import utils


def test_get_md_message_unified():
    name = "Test"
    res = f'{name} картина дня от {date.today().strftime("%d.%m.%y")}\n\n\n'
    assert utils.get_md_message_unified(name, []) == res

