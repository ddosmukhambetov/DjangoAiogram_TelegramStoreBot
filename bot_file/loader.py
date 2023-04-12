from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from config import settings

# Создаем нашего бота и диспатчер, MemoryStorage хранилище состояний
bot = Bot(settings.TOKEN_API, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
