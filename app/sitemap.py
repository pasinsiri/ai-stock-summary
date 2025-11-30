import requests
import xml.etree.ElementTree as ET

def get_recent_articles(max_articles=50):
    url = "https://www.cnbc.com/sitemap_news.xml"
    resp = requests.get(url)
    resp.raise_for_status()
    
    root = ET.fromstring(resp.content)
    articles = []
    ns = {'sm': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
    
    for sitemap in root.findall('sm:sitemap', ns):
        loc = sitemap.find('sm:loc', ns).text
        if "article" in loc:
            sub = requests.get(loc).text
            subroot = ET.fromstring(sub)
            for url in subroot.findall('sm:url', ns):
                loc_elem = url.find('sm:loc', ns)
                if loc_elem is not None:
                    articles.append(loc_elem.text)
    return articles[-max_articles:]