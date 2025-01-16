import requests
import json
import datetime as dt

class Serper():
    def __init__(self, api_key):
        self.api_key = api_key
        self.search_url = "https://google.serper.dev/search"
        self.scrape_url = "https://scrape.serper.dev"

    def scrape(query: str, n_day_lag: int = 1):
        pass