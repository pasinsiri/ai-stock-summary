from bs4 import BeautifulSoup
import requests
from .utils import extract_tickers
from config.settings import USER_AGENT

def scrape_article(url):
    headers = {"User-Agent": USER_AGENT}
    r = requests.get(url, headers=headers, timeout=10)
    r.raise_for_status()
    soup = BeautifulSoup(r.content, 'html.parser')

    title = soup.find("h1") or soup.find("title")
    title = title.get_text(strip=True) if title else "No title"

    content = ""
    for sel in ['[data-module="ArticleBody"]', 'div.group', 'article']:
        container = soup.select_one(sel)
        if container:
            content = " ".join(p.get_text() for p in container.find_all("p"))
            break
    if not content:
        content = soup.get_text(separator=" ")[:8000]

    tickers = extract_tickers(title + " " + content)
    return title, content[:8000], list(set(tickers))