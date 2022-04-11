import requests
import re
import random

class news:
    def __init__(self):
        self.news = []
        self.update_news()
        self.i = 0

    def update_news(self):
        r = requests.get("http://nrk.no").text
        x = re.findall('data-ec-name="((?:\w|\d|\s|-)*)"', r)
        x.remove("Se siste nytt")
        self.news = x

    def __str__(self):
        self.i = (self.i + 1) % len(self.news)
        return self.news[self.i]

nyheter = news()
for i in range(20):
    print(nyheter)
