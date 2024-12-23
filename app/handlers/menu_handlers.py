from aiogram import Router, F
from aiogram.filters import CommandStart, StateFilter, Command
from aiogram.filters.callback_data import CallbackData
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

import app.keyboards.menu_kb as kb
import app.keyboards.cart_kb as cart_kb
import app.keyboards.orders_kb as order_kb
from app.database.requests import (
    set_user, update_user, get_user, get_page, inc_page, dec_page,
    get_drinks, get_food,
    add_to_cart, delete_from_cart, get_cart, get_cart_by_id, get_carts_position,
    inc_pos_quantity, dec_pos_quantity)
from app.utils import get_drink_by_page

menu_router = Router()


@menu_router.callback_query(F.data == 'go_back')
async def go_back_func(callback: CallbackQuery):
    await callback.message.edit_text(text='На выбор представлены четыре раздела меню. Выберите дальнейшее действие:')
    await callback.message.edit_reply_markup(reply_markup=await kb.main_menu_kb())


#### Каталог ####

@menu_router.callback_query(F.data == 'catalog')
async def go_categories(callback: CallbackQuery):
    await callback.message.edit_text(text='Выберите категорию продуктов')
    await callback.message.edit_reply_markup(reply_markup=await kb.category_kb())


@menu_router.callback_query(F.data == 'food')
async def show_food(callback: CallbackQuery):
    page = await get_page(callback.from_user.id, 'Еда')
    food = await get_food()
    await callback.message.edit_text(text=f"{str(food[page].name).title()}  {str(food[page].price)} руб")
    await callback.message.edit_reply_markup(
        reply_markup=await kb.food_kb(await get_page(callback.from_user.id, 'Еда')))


@menu_router.callback_query(F.data == 'forward_food')
async def show_food(callback: CallbackQuery):
    await inc_page(callback.from_user.id, 'Еда')

    page = await get_page(callback.from_user.id, 'Еда')
    food = await get_food()

    await callback.message.edit_text(text=f"{str(food[page].name).title()} {str(food[page].price)} руб")
    await callback.message.edit_reply_markup(
        reply_markup=await kb.food_kb(await get_page(callback.from_user.id, "Еда")))


@menu_router.callback_query(F.data == 'backward_food')
async def show_food(callback: CallbackQuery):
    await dec_page(callback.from_user.id, 'Еда')

    page = await get_page(callback.from_user.id, 'Еда')
    food = await get_food()

    await callback.message.edit_text(text=f"{str(food[page].name).title()}  {str(food[page].price)} руб")
    await callback.message.edit_reply_markup(
        reply_markup=await kb.food_kb(await get_page(callback.from_user.id, "Еда")))


@menu_router.callback_query(F.data.startswith("cart_food"))
async def add_food_to_cart(callback: CallbackQuery):
    pos = callback.data.split('_')[2]
    await add_to_cart(callback.from_user.id, int(pos))
    await callback.answer(text="Добавлено в корзину")


@menu_router.callback_query(F.data.startswith("cart_drink"))
async def add_drink_to_cart(callback: CallbackQuery):
    pos = callback.data.split('_')[2]
    await add_to_cart(callback.from_user.id, int(pos))
    await callback.answer(text="Добавлено в корзину")


@menu_router.callback_query(F.data == 'drinks')
async def show_food(callback: CallbackQuery):
    page = await get_page(callback.from_user.id, 'Напиток')
    drinks = await get_drinks()

    drink = drinks[page - 1]
    print(drink.name)

    await callback.message.edit_text(text=drink.name)
    await callback.message.edit_reply_markup(
        reply_markup=await kb.drink_kb(await get_page(callback.from_user.id, 'Напиток')))


@menu_router.callback_query(F.data.startswith('forward_drink_'))
async def show_food(callback: CallbackQuery):
    await inc_page(callback.from_user.id, 'Напиток')

    page = await get_page(callback.from_user.id, 'Напиток')
    drink = await get_drink_by_page(page - 1)

    await callback.message.edit_text(text=drink)
    await callback.message.edit_reply_markup(
        reply_markup=await kb.drink_kb(await get_page(callback.from_user.id, "Напиток")))


@menu_router.callback_query(F.data.startswith('backward_drink_'))
async def show_food(callback: CallbackQuery):
    await dec_page(callback.from_user.id, 'Напиток')

    page = await get_page(callback.from_user.id, 'Напиток')
    drink = await get_drink_by_page(page - 1)

    await callback.message.edit_text(text=drink)
    await callback.message.edit_reply_markup(
        reply_markup=await kb.drink_kb(await get_page(callback.from_user.id, "Напиток")))


#### Корзина ####


@menu_router.callback_query(F.data == 'cart')
async def show_users_cart(callback: CallbackQuery):
    carts = await get_cart(callback.from_user.id)
    print(carts)
    if carts:
        await callback.message.edit_text(text='Ваша корзина')
        await callback.message.edit_reply_markup(reply_markup=await cart_kb.carts_kb(callback.from_user.id))
    else:
        await callback.message.edit_text(text='Корзина пустая')
        await callback.message.edit_reply_markup(reply_markup=await order_kb.created_order_kb())


@menu_router.callback_query(F.data.startswith('cart_'))
async def change_carts_object(callback: CallbackQuery):
    tmp = int(callback.data.split('_')[1])
    pos = await get_carts_position(tmp)
    cart = await get_cart_by_id(tmp)
    await callback.message.edit_text(f"Название: {pos.name}\n"
                                     f"Цена: {pos.price}\n"
                                     f"Количество: {cart.quantity}\n"
                                     f"Итого за позицию: {int(cart.quantity) * int(pos.price)}"
                                     )

    await callback.message.edit_reply_markup(reply_markup=await cart_kb.change_cart_kb(cart.id))


@menu_router.callback_query(F.data.startswith('inc_quantity'))
async def show_users_cart(callback: CallbackQuery):
    cart_id = int(callback.data.split('_')[2])

    await inc_pos_quantity(cart_id)

    pos = await get_carts_position(cart_id)
    cart = await get_cart_by_id(cart_id)

    await callback.message.edit_text(f"Название: {pos.name}\n"
                                     f"Цена: {pos.price}\n"
                                     f"Количество: {cart.quantity}\n"
                                     f"Итого за позицию: {int(cart.quantity) * int(pos.price)}"
                                     )

    await callback.message.edit_reply_markup(reply_markup=await cart_kb.change_cart_kb(cart_id))


@menu_router.callback_query(F.data.startswith('dec_quantity'))
async def show_users_cart(callback: CallbackQuery):
    cart_id = int(callback.data.split('_')[2])

    await dec_pos_quantity(cart_id)

    pos = await get_carts_position(cart_id)
    cart = await get_cart_by_id(cart_id)

    if cart.quantity == 0:
        await delete_from_cart(cart_id)
        await callback.message.edit_text(text='Ваша корзина')
        await callback.message.edit_reply_markup(reply_markup=await cart_kb.carts_kb(callback.from_user.id))
    else:
        await callback.message.edit_text(f"Название: {pos.name}\n"
                                         f"Цена: {pos.price}\n"
                                         f"Количество: {cart.quantity}\n"
                                         f"Итого за позицию: {int(cart.quantity) * int(pos.price)}"
                                         )

        await callback.message.edit_reply_markup(reply_markup=await cart_kb.change_cart_kb(cart_id))
