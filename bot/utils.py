import requests
from asgiref.sync import sync_to_async
from django.core.cache import cache

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

async def create_response(city, user_id):
    cached_weather = cache.get(city)
    if cached_weather:
        await sync_to_async(WeatherRequest.objects.create)(user_id=user_id, command=city, response=cached_weather)
        print('cached')
        return cached_weather

    weather = get_weather(city)
    if not weather:
        return f"Не удалось получить погоду в {city}. Убедитесь, что название города указано верно."

    weather_description, temp, feels_like, humidity, wind_speed = weather
    response_text = (f"Погода в {city}: - {weather_description}\n"
                     f"Температура: {temp} °C\n"
                     f"Ощущается температура: {feels_like} °C\n"
                     f"Влажность: {humidity} %\n"
                     f"Скорость ветра: {wind_speed} м/с")

    cache.set(city, response_text, timeout=1800)

    await sync_to_async(WeatherRequest.objects.create)(user_id=user_id, command=city, response=cached_weather)
    print('no cached')

    return response_text