import requests
import bs4 as bs
import sched


URL = "https://habr.com/ru/hub/infosecurity/top/weekly/"


page = requests.get(URL)
soup = bs.BeautifulSoup(page.text, "lxml")
top_articles_wrapper = soup.find("div", {"class": "tm-articles-list"})
articles = top_articles_wrapper.find_all("article")
for art in articles:
    link_wrap = art.find("a", {"class": "tm-article-snippet__title-link"})
    link = link_wrap["href"]
    title = link_wrap.find("span").text
    with open("test_parse.txt", "a") as f:
        f.write(f"https://habr.com{link}\n{title}\n")
