from aiogram import types
from ..loader import bot, dp
from ..keyboards.catalog_ikb import get_categories, category_cb
from ..keyboards import sign_inup_kb
from ..models import Product
from aiogram.dispatcher.filters import Text
from .authorization import sign_in


# @dp.message_handler(Text(equals='Каталог 🛒'))
async def cmd_catalog(message: types.Message):
    if sign_in['current_state']:
        await bot.send_message(chat_id=message.chat.id, text="Выберите категорию из списка 📂",
                               reply_markup=await get_categories())
    else:
        await message.answer("Вы не вошли в аккаунт, попробуйте войти в профиль ‼️",
                             reply_markup=sign_inup_kb.markup)


async def get_products(query):
    await bot.send_message(chat_id=query.message.chat.id, text="Список товаров которые есть в этой категорий: ")
    elem = query.data.split(':')
    async for product in Product.objects.filter(product_category_id=elem[1]):
        photo_id = product.photo.open('rb').read()
        text = f"Товар 🚀: {product.name}\n\n" \
               f"Описание 💬: {product.description}\n\n" \
               f"Цена 💰: {product.price} рублей"
        await bot.send_photo(chat_id=query.message.chat.id, photo=photo_id, caption=text)


@dp.callback_query_handler(category_cb.filter(action='view'))
async def show_products(query: types.CallbackQuery):
    await query.answer(text="Каталог товаров")
    await get_products(query)


def catalog_handlers_register():
    dp.register_message_handler(cmd_catalog, Text(equals='Каталог 🛒'))
