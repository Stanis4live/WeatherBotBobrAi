from aiogram import Bot, Dispatcher, Router, types
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.types import BotCommand
from aiogram.filters import Command, CommandObject
from asgiref.sync import sync_to_async

from bot.utils import get_weather
from weather_app.settings import TELEGRAM_TOKEN
from app.models import WeatherRequest

session = AiohttpSession()
bot_token = TELEGRAM_TOKEN
bot = Bot(token=bot_token, session=session)
dp = Dispatcher()
router = Router()
dp.include_router(router)


async def onstart():
    await bot.set_my_commands([
        BotCommand(command="start", description="Начать работу"),
        BotCommand(command="weather", description="Узнать погоду в городе"),
    ])


@router.message(Command(commands=['start']))
async def start_command(message: types.Message):
    await message.reply(
        "Привет! Я бот для проверки погоды. Используй команду /weather <город> для получения информации.")


@router.message(Command(commands=['weather']))
async def weather_command(message: types.Message, command: CommandObject):
    if not command.args:
        await message.reply("Не указан город. Используй команду /weather <город>.")
    else:
        city = command.args
        weather = get_weather(city)
        if not weather:
            await message.reply(f"Не удалось получить погоду в {city}. Убедитесь, что название города указано верно.")
        else:
            weather_description, temp, feels_like, humidity, wind_speed = weather
            response_text = (f"Погода в {city}: - {weather_description}\n"
                             f"Температура: {temp} °C\n"
                             f"Ощущается температура: {feels_like} °C\n"
                             f"Влажность: {humidity} %\n"
                             f"Скорость ветра: {wind_speed} м/с")

            await message.reply(response_text)

            await sync_to_async(WeatherRequest.objects.create)(
                user_id=message.from_user.id,
                command=city,
                response=response_text
            )