import geocoder
import requests
from vars import *

def GetWeather():
    g = geocoder.ip('me')
    latlng = g.latlng
    lat = latlng[0]
    lng = latlng[1]

    url = "https://api.openweathermap.org/data/2.5/weather?lat={}&lon={}&appid={}".format(str(lat),str(lng), WeatherAPI)

    response = requests.request("GET", url)
    return(response.text)