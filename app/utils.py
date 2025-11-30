import re

def extract_tickers(text: str):
    pattern = r'\b[A-Z]{1,5}\b'
    candidates = re.findall(pattern, text.upper())
    blacklist = {'THE', 'AND', 'FOR', 'WITH', 'FROM', 'THIS', 'THAT', 'WILL', 'ARE', 'IS', 'ON', 'IN', 'AT', 'BY', 'AS', 'IT', 'TO', 'OF', 'A', 'AN'}
    return [t for t in candidates if t not in blacklist]