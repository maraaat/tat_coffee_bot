from aiogram import Router, F
from aiogram.filters import CommandStart, StateFilter, Command
from aiogram.filters.callback_data import CallbackData
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

import app.keyboards.orders_kb as kb
import app.keyboards.menu_kb as menu_kb

from app.database.requests import (
    set_user, update_user, get_user, get_page, inc_page, dec_page,
    get_drinks, get_food,
    add_to_cart, delete_from_cart, get_cart, get_cart_by_id, get_carts_position,
    inc_pos_quantity, dec_pos_quantity,
    add_order, get_orders)
from app.utils import get_drink_by_page

order_router = Router()


@order_router.callback_query(F.data == 'create_order')
async def create_new_order(callback: CallbackQuery):
    await callback.message.edit_text(text='Заказ оформлен')
    await add_order(callback.from_user.id)
    await callback.message.edit_reply_markup(reply_markup=await kb.created_order_kb())


@order_router.callback_query(F.data == 'history')
async def show_oder_history(callback: CallbackQuery):
    orders = await get_orders(callback.from_user.id)

    for order in orders:

        orders_carts = order.carts.split('_')
        line = f"Заказ № {str(order.id)}\n"
        for c in orders_carts:
            if c != "":
                cart = await get_cart_by_id(int(c))

                position = await get_carts_position(int(cart.id))

                line += f"{position.name} - {int(cart.quantity)} шт. - {int(cart.quantity) * int(position.price)}\n"

        await callback.message.answer(
            text=line
        )

    await callback.message.answer(text="История просмотрена. Дальнейшие действия?",
                                  reply_markup=await menu_kb.main_menu_kb())
