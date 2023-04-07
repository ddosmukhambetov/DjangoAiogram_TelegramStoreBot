from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData
from asgiref.sync import sync_to_async
from ..models import Category

category_cb = CallbackData('category', 'id', 'action')


@sync_to_async
def get_categories():
    categories = Category.objects.all()
    markup = InlineKeyboardMarkup(row_width=1)
    for category in categories:
        markup.add(InlineKeyboardButton(text=category.name,
                                        callback_data=category_cb.new(id=category.id, action='view')))
    return markup
