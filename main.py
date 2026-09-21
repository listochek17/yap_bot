"""Главный модуль бота Yap.

Обработчики команд: /start, переход на сайт, покупка и история.
Добавлены проверки на наличие TOKEN, логирование и комментарии.
"""

from dotenv import load_dotenv
from telebot import TeleBot, types
import os
import logging
import keyboards as kb
from pu_in_base import prod_list, categories_list, show_cat_id, show_detail

load_dotenv()

# Базовая конфигурация логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')

TOKEN = os.getenv('TOKEN')
if not TOKEN:
    logging.critical('TOKEN не найден в окружении. Создайте .env с TOKEN=<ваш_токен>')
    raise RuntimeError('TOKEN not found')

bot = TeleBot(token=TOKEN)


@bot.message_handler(commands=['start'])
def start(message: types.Message):
    """Регистрация пользователя и показ главной клавиатуры."""
    chat_id = message.chat.id
    first_name = message.from_user.first_name
    bot.send_message(chat_id, f"{first_name}, добро пожаловать в наш магазин еды.\nВыберите действие снизу.", reply_markup=kb.start_kb())


@bot.message_handler(func=lambda msg: msg.text == 'Перейти на сайт')
def sayt(message: types.Message):
    chat_id = message.chat.id
    html = 'https://yaponamama.uz/'
    bot.send_message(chat_id, f'Наш сайт: {html}')


@bot.message_handler(func=lambda msg: msg.text == 'Купить здесь')
def cat(message: types.Message):
    chat_id = message.chat.id
    # Показываем список категорий
    bot.send_message(chat_id, 'Выберите тип блюда, который вы хотите:', reply_markup=kb.cat_kb())


@bot.message_handler(func=lambda msg: msg.text in categories_list())
def prod1(message: types.Message):
    """Пользователь выбрал категорию — показать продукты и ждать выбора продукта."""
    chat_id = message.chat.id
    cat_id = show_cat_id(message.text)
    if cat_id is None:
        bot.send_message(chat_id, 'Категория не найдена. Пожалуйста, выберите снова.', reply_markup=kb.cat_kb())
        return
    bot.send_message(chat_id, 'Выберите блюдо:', reply_markup=kb.prod_kb(cat_id))
    # Регистрируем следующий шаг — пользователь выберет продукт
    bot.register_next_step_handler(message, show_product)


def show_product(message: types.Message):
    """Показать детали выбранного продукта (название + цена)."""
    chat_id = message.chat.id
    title = message.text
    costs = show_detail(title)
    if costs is None:
        bot.send_message(chat_id, 'Товар не найден. Попробуйте выбрать другой.', reply_markup=kb.cat_kb())
        return
    text = f"{title}\nЦена: {costs}"
    bot.send_message(chat_id, text)


if __name__ == '__main__':
    # Запуск polling только при непосредственном запуске модуля
    bot.polling(none_stop=True)

