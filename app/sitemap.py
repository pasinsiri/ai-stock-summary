import requests
import xml.etree.ElementTree as ET
from config.settings import USER_AGENT
from typing import List

def get_recent_articles(max_articles: int = 50) -> List[str]:
    """
    Fetch recent article URLs from CNBC's news sitemap.
    Uses headers to avoid 403 errors.
    """
    url = "https://www.cnbc.com/sitemap_news.xml"
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/xml, text/xml",
        "Accept-Encoding": "gzip, deflate",
        "Connection": "keep-alive",
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()  # Raises HTTPError for bad status codes
    except requests.exceptions.HTTPError as e:
        if response.status_code == 403:
            raise ValueError(
                f"403 Forbidden on {url}. Try updating your User-Agent in config/settings.py "
                "to a real browser string (e.g., 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36...'). "
                "If persists, CNBC may be rate-limiting your IP—wait 5-10 min or use a VPN."
            ) from e
        raise
    
    root = ET.fromstring(response.content)
    articles = []
    ns = {'news': 'http://www.google.com/schemas/sitemap-news/0.9', 'sm': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
    
    # CNBC's news sitemap uses <urlset> with <news:news> extensions
    for url_elem in root.findall('.//sm:url', ns):
        loc_elem = url_elem.find('sm:loc', ns)
        if loc_elem is not None and 'cnbc.com' in loc_elem.text:
            articles.append(loc_elem.text)
    
    # Sort by lastmod if available (newest first), then limit
    if articles:
        # Simple reverse to get recent (assuming sitemap is chronological)
        articles = articles[-max_articles:]
    
    print(f"Fetched {len(articles)} recent articles from CNBC sitemap.")
    return articles