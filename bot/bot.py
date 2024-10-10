from aiogram import Bot, Dispatcher, Router, types
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.types import BotCommand
from aiogram.filters import Command, CommandObject
from asgiref.sync import sync_to_async
from django.core.cache import cache

from bot.utils import get_weather, create_response
from weather_app.settings import TELEGRAM_TOKEN
from app.models import WeatherRequest, UserSettings

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
        BotCommand(command="setcity", description="Установить предпочитаемый город"),
        BotCommand(command="getcity", description="Получить погоду в моём городе"),
    ])


@router.message(Command(commands=['start']))
async def start_command(message: types.Message):
    await message.reply(
        "👋 Привет! Я бот для проверки погоды.\n\n"
        "Вот что я умею:\n"
        "1. /weather <город> — Узнать погоду в определённом городе.\n"
        "2. /setcity <город> — Сохранить город для постоянного запроса погоды.\n"
        "3. /getcity — Узнать погоду в вашем предпочитаемом городе.",
    )


@router.message(Command(commands=['weather']))
async def weather_command(message: types.Message, command: CommandObject):
    if not command.args:
        await message.reply("Не указан город. Используй команду /weather <город>.")
    else:
        city = command.args
        response_text = await create_response(city, message.from_user.id)
        await message.reply(response_text)


@router.message(Command(commands=['setcity']))
async def set_city_command(message: types.Message, command: CommandObject):
    if not command.args:
        await message.reply("Не указан город. Используй команду /setcity <город>.")
    else:
        city = command.args
        await sync_to_async(UserSettings.objects.update_or_create)(
            user_id=message.from_user.id,
            defaults={'preferred_city': city}
        )
        await message.reply(f"Город {city} успешно сохранен как предпочитаемый.")


@router.message(Command(commands=['getcity']))
async def get_city_command(message: types.Message, command: CommandObject):
    user_settings = await sync_to_async(UserSettings.objects.filter(user_id=message.from_user.id).first)()
    if not user_settings or not user_settings.preferred_city:
        await message.reply(
            "Вы не установили предпочитаемый город. Используйте команду /setcity <город>."
        )
    else:
        city = user_settings.preferred_city
        response_text = await create_response(city, message.from_user.id)
        await message.reply(response_text)

