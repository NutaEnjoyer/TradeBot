from aiogram import types 
import data.config as config
from models import *

def start():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    b1 = types.KeyboardButton('📁 Мой профиль')
    b2 = types.KeyboardButton('📊 Трейдинг 2.0')
    b3 = types.KeyboardButton('💻 О проекте')
    keyboard.add(b1)
    keyboard.add(b2)
    keyboard.add(b3)

    return keyboard

def bots():
    keyboard = types.InlineKeyboardMarkup()
    b1 = types.InlineKeyboardButton('BITGET TRADE', url='https://t.me/BitgetTelegramBot')
    keyboard.add(b1)

    return keyboard


def mentors():
    keyboard = types.InlineKeyboardMarkup()
    mentors = Mentor.select()
    for mentor in mentors:
        b = types.InlineKeyboardButton(f'{mentor.name}', callback_data=f'link_mentor${mentor.id}')
        keyboard.add(b)
    b1 = types.InlineKeyboardButton('Отмена', callback_data='cancel')
    keyboard.add(b1)

    return keyboard

def cancel():
    keyboard = types.InlineKeyboardMarkup()
    b1 = types.InlineKeyboardButton('Отмена', callback_data='cancel')
    keyboard.add(b1)

    return keyboard

def profile():
    keyboard = types.InlineKeyboardMarkup()
    b1 = types.InlineKeyboardButton('Изменить FAKE тег', callback_data='change_tag')
    b2 = types.InlineKeyboardButton('Вкл/Выкл FAKE тег', callback_data='switch_tag')
    keyboard.add(b1)
    keyboard.add(b2)

    return keyboard

def main():
    keyboard = types.InlineKeyboardMarkup()
    b1 = types.InlineKeyboardButton('💬 Общий чат', url=config.CHAT_URL)
    b2 = types.InlineKeyboardButton('🤑 Канал профитов', url=config.PAYMENTS_URL)
    b3 = types.InlineKeyboardButton('👨‍💻 Закрепиться за наставником', callback_data='mentor')
    b4 = types.InlineKeyboardButton('🧾 Проверка чеков', callback_data='check_check')
    b5 = types.InlineKeyboardButton('❗️ Пожаловаться на карту', callback_data='report_card')
    keyboard.add(b1, b2)
    keyboard.add(b3, b4)
    # keyboard.add(b5)

    return keyboard