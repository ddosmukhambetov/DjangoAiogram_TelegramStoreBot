from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData
from asgiref.sync import sync_to_async
from ..models import Category, SubCategory

category_cb = CallbackData('category', 'id', 'action')
subcategory_cb = CallbackData('subcategory', 'id', 'action')


# Реализована клавиатура для вывода категории
@sync_to_async
def get_categories():
    categories = Category.objects.all()
    markup = InlineKeyboardMarkup(row_width=1)
    for category in categories:
        markup.add(InlineKeyboardButton(text=category.name,
                                        callback_data=category_cb.new(id=category.id, action='view_categories')))
    return markup


# Реализована клавиатура для вывода подкатегории
@sync_to_async
def get_subcategories(cat_id):
    subcategories = SubCategory.objects.filter(subcategory_category_id=cat_id)
    subcategory_markup = InlineKeyboardMarkup(row_width=2)
    for subcategory in subcategories:
        subcategory_markup.add(InlineKeyboardButton(text=subcategory.name,
                                                    callback_data=subcategory_cb.new
                                                    (id=subcategory.id, action='view_subcategories')))
    return subcategory_markup
