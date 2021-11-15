import time
from typing import Dict

from requests import post

TASS_API_LINK = "https://tass.ru/userApi/getNewsFeed"


def get_live_news() -> Dict:
    digest = {}
    news = post(
        TASS_API_LINK, json={"limit": 15, 'timestamp': round(time.time())}
    ).json()  # Есть варик регулировать кол-во новостей через параметр limit
    for n in news["newsList"]:
        digest["https://tass.ru" + n["link"]] = n["title"]
    return digest


if __name__ == "__main__":
    name = "Tass.ru"
    digest = get_live_news()
    print(digest)
    # print(utils.get_md_message_unified(name, digest))
