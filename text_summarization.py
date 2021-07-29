import requests
import bs4 as bs
import summa.summarizer
from summa.keywords import keywords
import gensim.summarization.summarizer
import gensim.summarization.keywords
from rbc_parser import parse_rbc
from unicodedata import normalize


def parse_article(url: str) -> str:
    text = ""
    page = requests.get(url)
    soup = bs.BeautifulSoup(page.text, "html.parser")
    wrapper = soup.find("div", {"class": "article"})
    text = list(map(lambda x: normalize("NFKD", x.text).strip(), wrapper.find_all("p")))
    return text


if __name__ == "__main__":
    news = parse_rbc()
    title = news[list(news.keys())[0]]
    link = list(news.keys())[0]
    text = " ".join(parse_article(link))
    summary_gensim = gensim.summarization.summarizer.summarize(
        text, ratio=0.3, split=True
    )
    summary_summa = summa.summarizer.summarize(text, ratio=0.3, split=True)
    print(summary_gensim)
    print(summary_summa)

    kw_gensim = gensim.summarization.keywords(text, words=10, split=True)
    kw_summa = keywords(text, words=10, split=True)

    print(kw_gensim)
    print(kw_summa)
