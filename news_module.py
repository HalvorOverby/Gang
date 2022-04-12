import requests
import re
import random

class news:
    def __init__(self):
        self.news = []
        self.update_news()
        self.i = 0

    def update_news(self):
        r = requests.get("http://nrk.no/nyheter/").text
        x = re.findall('"bulletin-title">((?:\w|\d|\s|-)*)</h', r)
        self.news = x

    def __str__(self):
        self.i = (self.i + 1) % len(self.news)
        return "NRK: " + self.news[self.i]