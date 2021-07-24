import requests
import bs4 as bs
import pandas as pd

URL = "https://habr.com/ru/hubs/page"
DF = pd.DataFrame(
    columns=["Title", "Link", "Description", "Raiting", "Subscriptions"])


def make_nice_subs(subs: str) -> int:
    if '.' in subs:
        subs = subs.replace('K', '00').replace('.', '')
    else:
        subs = subs.replace('K', '00')
    return int(subs)


for i in range(1, 12):
    current_url = URL + str(i)
    page = requests.get(current_url)
    soup = bs.BeautifulSoup(page.text, "lxml")
    hubs_wrapper = soup.find("div", {"class", "tm-hubs-list"})
    hubs = hubs_wrapper.find_all(
        "div", {"class", "tm-hubs-list__category-wrapper"})
    for hub in hubs:
        title = hub.find("span").text
        link = "https://habr.com" + \
            hub.find("a", {"class": "tm-hub__title"})["href"]
        desc = hub.find("div", {"class": "tm-hub__description"}).text
        raiting = hub.find(
            "div", {"class", "tm-hubs-list__hub-rating"}).text.strip()
        subs = hub.find(
            "div", {"class", "tm-hubs-list__hub-subscribers"}).text.strip()
        DF = DF.append(
            dict(zip(DF.columns, [title, link, desc, raiting, subs])), ignore_index=True)

DF['Subscriptions'] = DF['Subscriptions'].apply(make_nice_subs)
DF['Date'] = pd.to_datetime('today')
DF.to_csv('hubs.csv', index=False)
