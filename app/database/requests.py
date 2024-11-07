from sqlalchemy import select, update

from app.database.models import async_session
from app.database.models import User


async def set_user(tg_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))

        if not user:
            session.add(User(tg_id=tg_id))
            await session.commit()
            return False
        else:
            return user


async def update_user(tg_id, name, number):
    async with async_session() as session:
        await session.execute(update(User).where(User.tg_id == tg_id).values(name=name, phone_number=number))
        await session.commit()