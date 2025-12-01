import re
from bs4 import BeautifulSoup
from typing import List

def extract_tickers_from_html(html_content: str) -> List[str]:
    """
    Extract stock tickers from CNBC article HTML.
    Priority 1: Official <meta name="stock_tickers"> tag (most accurate)
    Priority 2: Fallback regex on visible text (title + body)
    """
    soup = BeautifulSoup(html_content, 'html.parser')

    # === PRIORITY 1: Official CNBC meta tag ===
    meta_tag = soup.find("meta", attrs={"name": "stock_tickers"})
    if meta_tag and meta_tag.get("content"):
        raw = meta_tag["content"].strip()
        tickers = [t.strip().upper() for t in raw.split(",") if t.strip()]
        if tickers:
            return tickers

    # # === PRIORITY 2: Fallback – smart regex on text ===
    # text = soup.get_text(separator=" ")
    # return extract_tickers_from_text(text)
    return None


def extract_tickers_from_text(text: str) -> List[str]:
    """
    Fallback: Extract 1–5 letter uppercase tickers using regex + blacklist.
    """
    pattern = r'\b[A-Z]{1,5}\b'
    candidates = re.findall(pattern, text.upper())

    # Common false positives to remove
    blacklist = {
        'THE', 'AND', 'FOR', 'WITH', 'FROM', 'THIS', 'THAT', 'WILL', 'ARE', 'IS',
        'ON', 'IN', 'AT', 'BY', 'AS', 'IT', 'TO', 'OF', 'A', 'AN', 'BE', 'BUT',
        'NOT', 'YOU', 'WE', 'HE', 'SHE', 'THEY', 'NEW', 'OLD', 'BIG', 'GET',
        'ALL', 'CAN', 'HAS', 'HAD', 'MAY', 'NOW', 'JUST', 'SO', 'NO', 'YES',
        'ONE', 'TWO', 'CEO', 'CFO', 'COO', 'PM', 'AM', 'EST', 'PST', 'GMT',
        'MONDAY', 'TUESDAY', 'WEDNESDAY', 'THURSDAY', 'FRIDAY'
    }

    tickers = [t for t in candidates if t not in blacklist and len(t) >= 1]
    return list(dict.fromkeys(tickers))  # Preserve order, remove duplicates


# Convenience alias for backward compatibility
extract_tickers = extract_tickers_from_html