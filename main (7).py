from dotenv import load_dotenv
from telebot import TeleBot, types

import os
import keyboards as kb
from pu_in_base import prod_list, categories_list, show_cat_id, show_detail
load_dotenv()

TOKEN = os.getenv('TOKEN')

bot = TeleBot(token=TOKEN)


@bot.message_handler(commands=['start'])
def start(message: types.Message):
    chat_id = message.chat.id
    first_name = message.from_user.first_name
    bot.send_message(chat_id, f'''{first_name}. Добропожаловать в наш магазин еды.
Выберите действие снизу.
''',  reply_markup=kb.start_kb())


@bot.message_handler(func=lambda msg: msg.text == 'Перейти на сайт')
def sayt(message: types.Message):
    chat_id = message.chat.id
    html = 'https://yaponamama.uz/'
    bot.send_message(chat_id, f'наш сайт {html}')


@bot.message_handler(func=lambda msg: msg.text == 'Купить здесь')
def cat(message: types.Message):
    chat_id = message.chat.id
    bot.send_message(chat_id, 'Выберите тип блюда которого вы хотите. ', reply_markup=kb.cat_kb())


@bot.message_handler(func=lambda msg: msg.text in categories_list())
def prod1(message: types.Message):
    chat_id = message.chat.id
    cat_id = show_cat_id(message.text)
    bot.send_message(chat_id, 'Выберите блюда. ', reply_markup=kb.prod_kb(cat_id))
    bot.register_next_step_handler(message, show_product)


def show_product(message: types.Message):
    chat_id = message.chat.id
    title = message.text
    costs = show_detail(message.text)
    text = f"""
{title}
{costs}
"""
    bot.send_message(chat_id, text)


bot.polling(none_stop=True)
