import os
from dotenv import load_dotenv
from sqlalchemy import BigInteger, String, ForeignKey
from sqlalchemy.ext.asyncio import AsyncAttrs, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

load_dotenv()

engine = create_async_engine(url=os.getenv('POSTGRESQL_URL'))

async_session = async_sessionmaker(engine)


class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id = mapped_column(BigInteger)
    name: Mapped[str] = mapped_column(String(20), nullable=True)
    phone_number: Mapped[str] = mapped_column(String(20), nullable=True)


class Position(Base):
    __tablename__ = "positions"

    id: Mapped[int] = mapped_column(primary_key=True)
    category: Mapped[str] = mapped_column(String(50))
    name: Mapped[str] = mapped_column(String(50))
    volume = mapped_column(BigInteger)
    price = mapped_column(BigInteger)


class Page(Base):
    __tablename__ = 'pages'

    id: Mapped[int] = mapped_column(primary_key=True)
    page_food = mapped_column(BigInteger, default=1)
    page_drink = mapped_column(BigInteger, default=1)
    user: Mapped[int] = mapped_column(ForeignKey("users.id"))


class Cart(Base):
    __tablename__ = 'carts'

    id: Mapped[int] = mapped_column(primary_key=True)
    quantity: Mapped[int] = mapped_column(BigInteger, default=1)
    user: Mapped[int] = mapped_column(ForeignKey("users.id"))
    position: Mapped[int] = mapped_column(ForeignKey("positions.id"))


async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

