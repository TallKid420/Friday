import geocoder, json, requests
from vars import *

def GetWeather():
    g = geocoder.ip('me')
    latlng = g.latlng
    lat = latlng[0]
    lng = latlng[1]

    url = "https://api.openweathermap.org/data/2.5/weather?lat={}&lon={}&appid={}".format(str(lat),str(lng), WeatherAPI)

    response = requests.request("GET", url)
    weather_data = json.loads(str(response.text))
    return("It is currently {}ing. The tempeture is {} degres Fahrenheit".format(weather_data["weather"][0]["main"], int(round(((weather_data["main"]["temp"] - 32) * 5/9) / 4, 0))))