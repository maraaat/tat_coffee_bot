from app.database.requests import get_drinks, get_food
from app.database.models import Cart

async def get_drink_by_page(page):
    drinks = await get_drinks()

    no_repeat_drinks = []  # Т.к. повторяются напитки из-за объема, выделим неповторяющийся список
    for d in drinks:
        flag = 0
        for n in no_repeat_drinks:
            if d.name == n.name:
                flag = 1
                break
        if flag == 0:
            no_repeat_drinks.append(d)

    print(len(no_repeat_drinks))
    drink = no_repeat_drinks[page]
    print(drink.name)
    return drink.name


