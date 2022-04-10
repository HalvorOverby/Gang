from datetime import datetime
import requests
import json

class weather():
    url="https://api.met.no/weatherapi/locationforecast/2.0/compact?altitude=30&lat=63.4185&lon=10.4028"
    headers={'User-Agent': 'Raspberry pi 3a+ gang prodject https://github.com/HalvorOverby/Gang'}
    time=""
    temp=0.0
    cloudFraction=0.0;
    windDirection=0
    windSpeed=0
    symbol=""
    rainAmount=""
    next6hoursSymbol=""
    next6hoursRainAmount=""

    def __init__(self):
        self.updateWeather()
    def updateWeather(self):
        rawtext= requests.get(self.url,headers=self.headers).content
        self.setParameters(rawtext)
    def setParameters(self,rawtext):
        dictionary=json.loads(rawtext)
        
        dictionary=self.getCurrentWeatherDict(dictionary['properties']['timeseries'])

        self.time=dictionary["time"]
        self.temp=dictionary["data"]["instant"]["details"]["air_temperature"]
        self.cloudFraction=dictionary["data"]["instant"]["details"]["cloud_area_fraction"]
        self.windDirection=dictionary["data"]["instant"]["details"]['wind_from_direction']
        self.windSpeed=dictionary["data"]["instant"]["details"]["wind_speed"]
        self.symbol=dictionary["data"]["next_1_hours"]["summary"]["symbol_code"]
        self.rainAmount=dictionary["data"]["next_1_hours"]["details"]['precipitation_amount']
        self.next6hoursSymbol=dictionary["data"]["next_6_hours"]["summary"]["symbol_code"]
        self.next6hoursRainAmount=dictionary["data"]["next_6_hours"]["details"]['precipitation_amount']

    def getCurrentWeatherDict(self, WeatherForDay: list):
        currentTime=f"{datetime.now().date()}T{datetime.now().hour}:00:00Z"    
        for WeatherAtTime in WeatherForDay:
            if WeatherAtTime['time'] == currentTime:
                return WeatherAtTime
    def toString(self):
        return f"Tid=\t\t{self.time}\nTemp=\t\t{self.temp}\nSkydekke=\t{self.cloudFraction}\nVindVinkel=\t{self.windDirection}\nVindHastighet=\t{self.windSpeed}\nSymbol=\t\t{self.symbol}\nRegnmengde=\t{self.rainAmount}\nSymbol6=\t{self.next6hoursSymbol}\nRegnmengde6=\t{self.next6hoursRainAmount}"

vear= weather()
print(vear.toString())