from bs4 import BeautifulSoup
import requests
from .utils import extract_tickers_from_html
from config.settings import USER_AGENT

def scrape_article(url):
    headers = {"User-Agent": USER_AGENT}
    r = requests.get(url, headers=headers, timeout=10)
    r.raise_for_status()
    soup = BeautifulSoup(r.content, 'html.parser')

    title = (soup.find("h1") or soup.find("title")).get_text(strip=True)
    content = soup.select_one('[data-module="ArticleBody"]')
    if content:
        text = " ".join(p.get_text() for p in content.find_all("p"))
    else:
        text = soup.get_text(separator=" ")[:8000]

    return title, text[:8000]  # ← tickers now come from sitemap