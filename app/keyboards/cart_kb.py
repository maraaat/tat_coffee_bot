from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

from app.database.requests import get_cart, get_carts_position


async def carts_kb(tg_id):
    carts = await get_cart(tg_id)
    kb = InlineKeyboardBuilder()
    for cart in carts:
        print(cart.position)
        position = await get_carts_position(int(cart.id))
        print(position)
        kb.add(InlineKeyboardButton(text=f"{position.name} - "
                                         f"{int(cart.quantity)} шт. - "
                                         f"{int(cart.quantity) * int(position.price)} (1 шт. - {position.price})",
                                    callback_data=f"cart_{cart.id}")
               )

    kb.row(InlineKeyboardButton(text='Оформить заказ 😇', callback_data='create_order'),
           InlineKeyboardButton(text='Меню 🏠', callback_data='go_back')
           )

    return kb.adjust(1).as_markup()


async def change_cart_kb(cart_id):
    kb = InlineKeyboardBuilder()

    kb.row(InlineKeyboardButton(text=f"➖", callback_data=f'dec_quantity_{cart_id}'),
           InlineKeyboardButton(text="Корзина 🛒", callback_data='cart'),
           InlineKeyboardButton(text=f"➕", callback_data=f'inc_quantity_{cart_id}')
           )

    return kb.as_markup()
