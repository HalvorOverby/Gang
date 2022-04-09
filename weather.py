import urllib.request
url="https://api.met.no/weatherapi/locationforecast/2.0/compact?altitude=30&lat=63.4185&lon=10.4028"

text= urllib.request.urlopen(url) #må identifye deg selv
print(text)