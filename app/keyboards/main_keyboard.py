from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder


async def login_kb():
    kb = InlineKeyboardBuilder()
    kb.add(InlineKeyboardButton(text="Войти по номеру", callback_data="reg"))
    return kb.adjust(1).as_markup()


async def send_number():
    contact = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text='📞 Поделиться контактом', request_contact=True)]
    ], resize_keyboard=True, input_field_placeholder='Нажмите кнопку внизу экрана')

    return contact


async def main_menu_kb():
    kb = [
        [KeyboardButton(text="Каталог"), KeyboardButton(text="Профиль")],
        [KeyboardButton(text="Корзина"), KeyboardButton(text="История заказов")]
    ]
    keyboard = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

    return keyboard
