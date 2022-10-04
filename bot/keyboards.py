from aiogram import types
from aiogram.types import KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

from bot.database.get import leagues
from bot.reference_info import DICT_TEAM, DICT_LEAGUE

# keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
# button_phone = types.KeyboardButton(text='Отправить контакт', request_contact=True)
# keyboard.add(button_phone)
# keyboard.row('Отменить ❌')


keyboard_1 = types.ReplyKeyboardMarkup(resize_keyboard=True)
for el in leagues:
    keyboard_1.add(el.name)

# inline_kb1 = InlineKeyboardMarkup(row_width=2)
# for el in leagues:
#     inline_btn_league = InlineKeyboardButton(f'{el.name}', callback_data=f'{el.id}')
#     inline_kb1.add(inline_btn_league)

keyboard_2 = types.ReplyKeyboardMarkup(resize_keyboard=True)
keyboard_2.row('Отправить')
keyboard_2.row('Отменить ❌')


def get_keywords(liga: str):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    # ar = list(DICT_TEAM.get(DICT_LEAGUE.get(liga)).values())
    id_league = DICT_LEAGUE.get(liga)
    ar = list(DICT_TEAM.get(id_league).keys())

    row_size = 4
    for iter in range(0, len(ar), row_size):
        keyboard.row(*ar[iter:iter + row_size])
    keyboard.row('Отменить ❌')
    return keyboard


# keyboard8 = types.ReplyKeyboardMarkup(resize_keyboard=True)
# keyboard8.row('Купить недельную подписку')
# keyboard8.row('Подписаться на месяц')
# keyboard8.row('Отменить ❌')

# keyboard9 = types.ReplyKeyboardMarkup(resize_keyboard=True)
# keyboard9.row('Отменить ❌')
