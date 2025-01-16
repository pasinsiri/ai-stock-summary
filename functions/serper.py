import requests
import json
import datetime as dt

class Serper():
    def __init__(self, api_key):
        self.api_key = api_key
        self.search_url = "https://google.serper.dev/search"
        self.scrape_url = "https://scrape.serper.dev"
        self.scrape_headers = {
            'X-API-KEY': self.api_key,
            'Content-Type': 'application/json'
        }

    def search_google(self, query: str, n_day_lag: int = 1, location: str = "Thailand", language: str = "en"):

        payload = json.dumps({
            "q": query,
            "location": location,
            "gl": language
        })

        response = requests.request("POST", self.search_url, headers=self.scrape_headers, data=payload)
        assert response.status_code == 200, f"Error: {response.status_code}"
        return response
    
    def scrape(self, url: str):
        response = requests.request("POST", self.scrape_url, headers=self.scrape_headers, data=json.dumps({url}))
        assert response.status_code == 200, f"Error: {response.status_code}"