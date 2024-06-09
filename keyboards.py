from telebot.types import KeyboardButton, ReplyKeyboardMarkup
from pu_in_base import categories_list
from pu_in_base import prod_list
# from pu_in_base import categories_list
# from pu_in_base import categories_list


def start_kb():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(
        KeyboardButton(text="Купить здесь"),
        KeyboardButton(text="Перейти на сайт")
    )
    return markup


def cat_kb():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    markup.add(*[KeyboardButton(text=item) for item in categories_list()])
    return markup


def prod_kb(cat_id):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    markup.add(*[KeyboardButton(text=item) for item in prod_list(cat_id)])
    return markup
