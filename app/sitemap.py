# app/sitemap.py
import requests
import xml.etree.ElementTree as ET
from config.settings import USER_AGENT
from typing import List, Dict, Optional

def get_recent_articles_with_tickers(max_articles: int = 50) -> List[Dict]:
    """
    Fetch recent CNBC articles + their OFFICIAL stock tickers from sitemap.
    Returns list of dicts: {"url": ..., "tickers": [...], "title": ...}
    """
    url = "https://www.cnbc.com/sitemap_news.xml"
    headers = {"User-Agent": USER_AGENT}

    response = requests.get(url, headers=headers, timeout=15)
    response.raise_for_status()

    root = ET.fromstring(response.content)

    # Namespaces
    ns = {
        'sm': 'http://www.sitemaps.org/schemas/sitemap/0.9',
        'news': 'http://www.google.com/schemas/sitemap-news/0.9'
    }

    articles = []

    for url_elem in root.findall('sm:url', ns):
        loc = url_elem.find('sm:loc', ns)
        if loc is None or loc.text is None:
            continue

        article_url = loc.text.strip()

        # Extract news block
        news_elem = url_elem.find('news:news', ns)
        if news_elem is None:
            continue

        title_elem = news_elem.find('news:title', ns)
        title = title_elem.text.strip() if title_elem is not None else "No title"

        tickers_elem = news_elem.find('news:stock_tickers', ns)
        raw_tickers = tickers_elem.text if tickers_elem is not None and tickers_elem.text else ""
        tickers = [t.strip().upper() for t in raw_tickers.split(",") if t.strip()]

        # Only include if has tickers (optional: remove this filter if you want all)
        if tickers:
            articles.append({
                "url": article_url,
                "title": title,
                "tickers": tickers
            })

    # Sort by recency (sitemap is usually chronological)
    recent_articles = articles[-max_articles:]
    print(f"Fetched {len(recent_articles)} articles with official tickers from sitemap.")
<<<<<<< Updated upstream
<<<<<<< Updated upstream
    return recent_articles
=======
    return recent_articles
>>>>>>> Stashed changes
=======
    return recent_articles
>>>>>>> Stashed changes
