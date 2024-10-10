import requests
from weather_app.settings import OPENWEATHER_API_KEY
from app.models import WeatherRequest


def get_weather(city: str):
    base_url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": OPENWEATHER_API_KEY,
        "units": "metric",
        "lang": "ru"
    }
    response = requests.get(base_url, params=params)
    if response.status_code != 200:
        return None
    else:
        data = response.json()
        weather_description = data["weather"][0]["description"]
        temp = data["main"]["temp"]
        feels_like = data["main"]["feels_like"]
        humidity = data["main"]["humidity"]
        wind_speed = data["wind"]["speed"]
        return weather_description, temp, feels_like, humidity, wind_speed

