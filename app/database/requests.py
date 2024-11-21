from sqlalchemy import select, update, delete

from app.database.models import async_session
from app.database.models import User, Position, Page, Cart, Order


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
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        session.add(Page(user=user.id))
        await session.commit()


async def get_user(tg_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(tg_id == User.tg_id))
        print(user)
        return user


async def get_positions():
    async with async_session() as session:
        catalog = await session.scalars(select(Position))

        return catalog.all()


async def get_food():
    async with async_session() as session:
        food = await session.scalars(select(Position).where(Position.category == 'Еда'))

        return food.all()


async def get_drinks():
    async with async_session() as session:
        drinks = await session.scalars(select(Position).where(Position.category == 'Напиток'))
        return drinks.all()


async def get_page(tg_id, category):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        page = await session.scalar(select(Page).where(Page.user == user.id))

        if category == 'Еда':
            return int(page.page_food)
        else:
            return int(page.page_drink)


async def inc_page(tg_id, category):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        page = await session.scalar(select(Page).where(Page.user == user.id))
        if category == 'Еда':
            page.page_food += 1
        else:
            page.page_drink += 1

        await session.commit()


async def dec_page(tg_id, category):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        page = await session.scalar(select(Page).where(Page.user == user.id))
        if category == 'Еда':
            page.page_food -= 1
        else:
            page.page_drink -= 1
        await session.commit()


async def add_to_cart(tg_id, pos_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        position = await session.scalar(select(Position).where(Position.id == pos_id))

        cart = await session.scalar(select(Cart).where(Cart.user == user.id, Cart.position == position.id))
        if not cart:
            session.add(Cart(user=user.id, position=pos_id))

        else:
            cart.quantity += 1

        await session.commit()


async def delete_from_cart(cart_id):
    async with async_session() as session:
        await session.execute(delete(Cart).where(Cart.id == cart_id))

        await session.commit()


async def clear_users_cart(tg_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        await session.execute(delete(Cart).where(user=user.id))
        await session.commit()


async def get_cart(tg_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        carts = await session.scalars(select(Cart).where(user.id == Cart.user, Cart.placed == 0))

        return carts.all()


async def get_cart_by_id(cart_id):
    async with async_session() as session:
        cart = await session.scalar(select(Cart).where(Cart.id == cart_id))

        return cart


async def get_carts_position(cart_id):
    async with async_session() as session:
        cart = await session.scalar(select(Cart).where(Cart.id == cart_id))

        position = await session.scalar(select(Position).where(Position.id == cart.position))

        return position


async def inc_pos_quantity(cart_id):
    async with async_session() as session:
        cart = await session.scalar(select(Cart).where(Cart.id == cart_id))
        cart.quantity += 1

        await session.commit()


async def dec_pos_quantity(cart_id):
    async with async_session() as session:
        cart = await session.scalar(select(Cart).where(Cart.id == cart_id))
        cart.quantity -= 1

        await session.commit()


### ORDERS

async def add_order(tg_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        carts = await session.scalars(select(Cart).where(Cart.user == user.id))

        cart_list = ""
        total = 0
        for cart in carts:
            cart_list += f"{str(cart.id)}_"
            position = await session.scalar(select(Position).where(Position.id == cart.position))
            total += cart.quantity * position.price

            cart.placed = 1

        session.add(Order(user=user.id, carts=cart_list, total=total))

        await session.commit()


async def get_orders(tg_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        orders = await session.scalars(select(Order).where(user.id == Order.user))

        return orders.all()
