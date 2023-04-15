from aiogram import types
from asgiref.sync import sync_to_async

from ..loader import bot, dp
from ..keyboards.catalog_ikb import get_categories, get_subcategories, category_cb, subcategory_cb
from ..keyboards import sign_inup_kb
from ..models import Product, SubCategory, Category
from aiogram.dispatcher.filters import Text
from .authorization import sign_in
from ..keyboards.default_kb import markup


# Сделан хендлер показа категории -> подкатегории -> товаров
# @dp.message_handler(Text(equals='Каталог 🛒'))
async def show_categories(message: types.Message):
    if sign_in['current_state']:
        if await category_exists():
            await bot.send_message(chat_id=message.chat.id, text="Выберите категорию из списка 📂",
                                   reply_markup=await get_categories())
        else:
            await bot.send_message(chat_id=message.chat.id, text="К сожалению администратор пока что "
                                                                 "не добавил категории ☹️",
                                   reply_markup=markup)
    else:
        await message.answer("Вы не вошли в аккаунт, попробуйте войти в профиль ‼️",
                             reply_markup=sign_inup_kb.markup)


async def get_products(query):
    elem = query.data.split(':')
    if await subcategory_products_exists(product_subcategory_id=elem[1]):
        await bot.send_message(chat_id=query.message.chat.id, text="Список товаров которые есть в этой подкатегории 👇 ")
        async for product in Product.objects.filter(product_subcategory_id=elem[1]):
            photo_id = product.photo.open('rb').read()
            text = f"Товар 🚀: {product.name}\n\n" \
                   f"Описание 💬: {product.description}\n\n" \
                   f"Цена 💰: {product.price} рублей"
            await bot.send_photo(chat_id=query.message.chat.id, photo=photo_id, caption=text)
    else:
        await bot.send_message(query.message.chat.id, text="К сожалению в этой подкатегории нет товаров 🙁",
                               reply_markup=markup)


# @dp.callback_query_handler(category_cb.filter(action='view_categories'))
async def show_subcategories(query: types.CallbackQuery):
    if sign_in['current_state']:
        elem = query.data.split(':')
        if await category_subcategory_exists(subcategory_category_id=elem[1]):
            await query.answer(text="Подкатегории")
            await bot.send_message(chat_id=query.message.chat.id, text="Выберите подкатегорию из списка ☺️",
                                   reply_markup=await get_subcategories(elem[1]))
        else:
            await bot.send_message(chat_id=query.message.chat.id,
                                   text="Простите, но в этой категории нет товаров 😔", reply_markup=markup)
    else:
        await bot.send_message(chat_id=query.message.chat.id,
                               text="Вы не вошли в аккаунт, попробуйте войти в профиль ‼️",
                               reply_markup=sign_inup_kb.markup)


# @dp.callback_query_handler(subcategory_cb.filter(action='view_subcategories'))
async def show_products(query: types.CallbackQuery):
    if sign_in['current_state']:
        await query.answer("Каталог товаров")
        await get_products(query)
    else:
        await bot.send_message(chat_id=query.message.chat.id,
                               text="Вы не вошли в аккаунт, попробуйте войти в профиль ‼️",
                               reply_markup=sign_inup_kb.markup)


@sync_to_async
def subcategory_products_exists(product_subcategory_id):
    return Product.objects.filter(product_subcategory=product_subcategory_id).exists()


@sync_to_async
def category_subcategory_exists(subcategory_category_id):
    return SubCategory.objects.filter(subcategory_category_id=subcategory_category_id).exists()


@sync_to_async
def category_exists():
    return Category.objects.all().exists()


def catalog_handlers_register():
    dp.register_message_handler(show_categories, Text(equals='Каталог 🛒'))
    dp.register_callback_query_handler(show_subcategories, category_cb.filter(action='view_categories'))
    dp.register_callback_query_handler(show_products, subcategory_cb.filter(action='view_subcategories'))
