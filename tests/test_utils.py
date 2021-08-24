import sys
import pytest

sys.path.append(".")

from datetime import date

from news_buddy import utils


def test_get_md_message_unified():
    name = "Test"
    res = f'{name} картина дня от {date.today().strftime("%d.%m.%y")}\n\n\n'
    assert utils.get_md_message_unified(name, []) == res

@pytest.mark.parametrize('test_input, expected', \
 [('asdasd', True),  ('Habr', True), ('/abrakadabra', True), ('/rbc', False), ('/Gazeta', False)])
def test_check_invalidity(test_input, expected):
    assert utils.check_invalidity(test_input) == expected
