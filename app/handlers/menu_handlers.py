from aiogram import Router, F
from aiogram.filters import CommandStart, StateFilter, Command
from aiogram.filters.callback_data import CallbackData
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

import app.keyboards.menu_kb as kb
from app.database.requests import (
    set_user, update_user, get_user, get_page, inc_page, dec_page,
    get_drinks, get_food,
    add_to_cart, delete_from_cart)
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

