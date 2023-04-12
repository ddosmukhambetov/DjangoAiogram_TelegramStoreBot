from django.core.management import BaseCommand
from aiogram import executor, types
from bot_file.handlers import default_handlers_register, catalog_handlers_register, authorization_handlers_register
from bot_file.keyboards import default_kb
from bot_file.loader import dp


async def on_startup(_):
    print("Bot has been successfully launched!")


# Запуск бота, обязательно management -> commands -> название -> создание класса Command(BaseCommand)
class Command(BaseCommand):

    def handle(self, *args, **options):
        default_handlers_register()
        catalog_handlers_register()
        authorization_handlers_register()

        @dp.message_handler(commands=None, regexp=None)
        async def unknown_text(message: types.Message):
            await message.answer("Простите, но я не понимаю вас ☹️\n\n"
                                 "Попробуйте использовать команду Помощь ⭐️",
                                 reply_markup=default_kb.only_help_markup)

        executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
