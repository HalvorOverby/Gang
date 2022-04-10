from datetime import datetime
from webbrowser import Elinks
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
        hour=datetime.now().hour
        if datetime.now().minute>30:
            hour+=1
        currentTime=f"{datetime.now().date()}T{hour}:00:00Z"    
        for WeatherAtTime in WeatherForDay:
            if WeatherAtTime['time'] == currentTime:
                return WeatherAtTime
    
    def weatherstatus(self):#Tanken er å rangsjere været fra og med 1 til og med 6. 1 er skyfri himmel ,ingen regn og vind og 20 deg. 2 er
        #rain
        if self.rainAmount==0:
            rain=0
        elif 0<self.rainAmount<0.2:
            rain=1
        elif 0.2<=self.rainAmount<1.8:
            rain=2
        elif 1.8<=self.rainAmount:
            rain=3
        
        #wind
        if self.windSpeed<4:
            wind=0
        elif 4<=self.windSpeed<10:
            wind=1
        elif 10<=self.windSpeed<22:
            wind=2
        elif 22<=self.windSpeed:
            wind=3
        
        #cloud
        if self.cloudFraction<40:
            cloud=0
        else:
            cloud=1
        
        #Calculation
        if rain==wind==cloud==0:
            return "Det er nydelig vær"
        if rain==wind==0 and cloud==1:
            return "Det er fint vær"
        if rain==0 and wind<2:
            return "Det er greit vær"
        if rain==1 and wind<2:
            return "På med regnjakka!"
        if rain==2 or wind==2:
            return "Det er ganske dårlig vær"
        if wind==3 or rain==3:
            return "ALARM! Revurder å gå ut!"
        
        
    
    def __str__(self):
        return f"Tid\t\t{self.time}\nTemp\t\t{self.temp}\nSkydekke\t{self.cloudFraction}\nVindVinkel\t{self.windDirection}\nVindHastighet\t{self.windSpeed}\nSymbol\t\t{self.symbol}\nRegnmengde\t{self.rainAmount}\nSymbol6\t\t{self.next6hoursSymbol}\nRegnmengde6\t{self.next6hoursRainAmount}"

