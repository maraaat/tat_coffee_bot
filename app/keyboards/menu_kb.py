from aiogram.filters.callback_data import CallbackData
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

from app.database.requests import get_food, get_drinks, get_page


class Pagination(CallbackData, prefix='pag'):
    page: int


async def main_menu_kb():
    kb = [
        [
            InlineKeyboardButton(text="Каталог ⭐", callback_data='catalog'),
            InlineKeyboardButton(text="Профиль  ℹ️", callback_data='profile')
        ],
        [
            InlineKeyboardButton(text="Корзина 🛒", callback_data='data'),
            InlineKeyboardButton(text="История заказов  ✅", callback_data='history')
        ]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb)

    return keyboard


async def category_kb():
    kb = [
        [
            InlineKeyboardButton(text="Назад 🏠", callback_data='go_back'),
            InlineKeyboardButton(text="Еда 🍰", callback_data='food')
        ],
        [
            InlineKeyboardButton(text="Напитки ☕", callback_data='drinks'),
            InlineKeyboardButton(text="Корзина 🛒", callback_data='cart')
        ]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb)

    return keyboard


async def profile_kb():
    kb = [
        [
            InlineKeyboardButton(text="Назад 🏠", callback_data='go_back'),
        ],

    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb)

    return keyboard


async def food_kb(page: int = 1):
    kb = InlineKeyboardBuilder()

    food = await get_food()
    start = page
    end = start + 1

    position = food[start]

    buttons_row = []
    if page > 1:
        buttons_row.append(
            InlineKeyboardButton(
                text="⬅️",
                callback_data=f'backward_food',
            )
        )

    #kb.row(InlineKeyboardButton(text="В корзину", callback_data=f'cart_food_{position.id}'))

    if end < len(food):
        buttons_row.append(
            InlineKeyboardButton(
                text="➡️",
                callback_data=f"forward_food",
            )
        )

    kb.row(*buttons_row)
    kb.row(InlineKeyboardButton(text="В корзину", callback_data=f'cart_food_{position.id}'))

    kb.row(InlineKeyboardButton(text=f"Выход", callback_data=f'go_back'),
           InlineKeyboardButton(text=f"Корзина", callback_data=f'go_cart')
           )

    return kb.as_markup()


async def drink_kb(page: int = 1):
    kb = InlineKeyboardBuilder()

    drinks = await get_drinks()
    no_repeat_drinks = []  # Т.к. повторяются напитки из-за объема, выделим неповторяющийся список
    for d in drinks:
        flag = 0
        for n in no_repeat_drinks:
            if d.name == n.name:
                flag = 1
                break
        if flag == 0:
            no_repeat_drinks.append(d)

    start = page - 1
    end = start + 1

    volumes = []

    drink = no_repeat_drinks[start]

    for d in drinks:  # проходим по полному списку напитков и сохраняем объемы текущего
        if drink.name == d.name:
            volumes.append(d)

    buttons_row = []

    if page > 1:
        buttons_row.append(
            InlineKeyboardButton(
                text="⬅️",
                callback_data=f'backward_drink_{drink.id}',
            )
        )
    for d in volumes:
        kb.row(InlineKeyboardButton(text=f"{str(d.volume)} ml - {str(d.price)} rub", callback_data=f'cart_drink_{d.id}'))

    if end < len(no_repeat_drinks):
        buttons_row.append(
            InlineKeyboardButton(
                text="➡️",
                callback_data=f"forward_drink_{drink.id}",
            )
        )

    kb.row(*buttons_row)

    kb.row(InlineKeyboardButton(text=f"Выход", callback_data=f'go_back'),
           InlineKeyboardButton(text=f"Корзина", callback_data=f'go_cart')
           )

    return kb.as_markup()
