import requests
import json
import datetime as dt

class Serper():
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.serpstack.com/search"