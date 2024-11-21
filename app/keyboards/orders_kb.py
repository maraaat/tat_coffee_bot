from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

from app.database.requests import get_cart, get_carts_position


async def created_order_kb():
    kb = InlineKeyboardBuilder()

    kb.row(InlineKeyboardButton(text='Вернуться на главную 🏠', callback_data='go_back'),

           )

    return kb.adjust(1).as_markup()
