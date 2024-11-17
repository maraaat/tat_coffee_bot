import asyncio
import os

from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

from app.handlers.user_handler import user_router
from app.handlers.menu_handlers import menu_router
from app.database.models import async_main


async def main():
    await async_main()
    load_dotenv()
    bot = Bot(os.getenv("TOKEN"))
    dp = Dispatcher()
    dp.include_routers(user_router, menu_router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')
