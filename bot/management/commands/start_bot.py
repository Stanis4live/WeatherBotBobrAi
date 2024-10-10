import asyncio
from django.core.management.base import BaseCommand
from bot.bot import bot, dp, onstart


class Command(BaseCommand):
    help = 'Start bot'

    def handle(self, *args, **kwargs):
        asyncio.run(self.start_bot())

    async def start_bot(self):
        await dp.start_polling(bot, on_startup=onstart)


