from django.core.management import BaseCommand
from aiogram import executor
from bot_file.handlers import default_handlers_register, catalog_handlers_register
from bot_file.loader import dp


async def on_startup(_):
    print("Bot has been successfully launched!")


class Command(BaseCommand):

    def handle(self, *args, **options):
        default_handlers_register()
        catalog_handlers_register()
        executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
