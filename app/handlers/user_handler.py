from aiogram import Router, F
from aiogram.filters import CommandStart, StateFilter, Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

import app.keyboards.main_keyboard as user_kb
import app.keyboards.menu_kb as menu_kb
from app.database.requests import set_user, update_user, get_user

user_router = Router()


class Registr(StatesGroup):
    name = State()
    number = State()


@user_router.message(CommandStart())
async def login_menu(message: Message, state: FSMContext):
    user = await set_user(message.from_user.id)
    if user:
        await message.answer(
            "Добро пожаловать в онлайн-кафе с самовывозом. Рады вас снова видеть!",
            reply_markup=await menu_kb.main_menu_kb()
        )
        await state.clear()
    else:
        await message.answer(
            "Добро пожаловать в онлайн-кафе с самовывозом. Пожалуйста пройдите регистрацию:",
        )
        await message.answer('Введите ваше имя: ')
        await state.set_state(Registr.name)


@user_router.message(Registr.name)
async def reg_two(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(Registr.number)
    await message.answer('Для продолжения работы необходим ваш контакт. Нажмите на кнопку "📞 Поделиться контактом"',
                         reply_markup=await user_kb.send_number()
                         )


@user_router.message(Registr.number, F.contact)
async def reg_third(message: Message, state: FSMContext):
    data = await state.get_data()
    await update_user(message.from_user.id, data['name'], message.contact.phone_number)
    await state.clear()
    await message.answer(f"Регистрация завершена. Можем приступить к заказу!", reply_markup=await menu_kb.main_menu_kb())


@user_router.message(Registr.number)
async def contact_incorrect(message: Message):
    await message.answer(
        text="Пожалуйста отправьте контакт по нажатию на кнопку\n\n",
        reply_markup=await user_kb.send_number()
    )


@user_router.callback_query(F.data == 'profile')
async def show_profile(callback: CallbackQuery):
    user = await get_user(callback.from_user.id)
    await callback.message.edit_text(f"Ваши данные:\n"
                         f"ID: {user.tg_id}\n"
                         f"Имя: {user.name}\n"
                         f"Номер телефона: {user.phone_number}\n"
                         f"Количество заказов: {user.id}"
                         )
    await callback.message.edit_reply_markup(reply_markup=await menu_kb.profile_kb())

