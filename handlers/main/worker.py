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

import datetime

def calculate_profit_stats(start_date, end_date, user_id):
    # Фильтрация по временному интервалу
	profits = Profit.select().where((Profit.time.between(start_date, end_date)) & (Profit.worker_id==user_id))
		
		# Расчет суммы и количества profit'ов
	total_profit = sum([i.price for i in profits])
	count_profit = profits.count()
		
	return count_profit, total_profit

async def me_handler(message: types.Message, state: FSMContext):
	start_date = int(time.time() - 86400)
	end_date = int(time.time())
	day = calculate_profit_stats(start_date, end_date, message.from_user.id)
	start_date = int(time.time() - 604800)
	end_date = int(time.time())
	week = calculate_profit_stats(start_date, end_date, message.from_user.id)
	start_date = int(time.time() - 2592000)
	end_date = int(time.time())
	month = calculate_profit_stats(start_date, end_date, message.from_user.id)

	text = f'''<b>Профиты {message.from_user.first_name}:

За день: {day[0]} профитов на {day[1]} р
За неделю: {week[0]} профитов на {week[1]} р
За месяц: {month[0]} профитов на {month[1]} р</b>'''
	
	await message.answer(text)

async def support_handler(message: types.Message, state: FSMContext):
	await states.Support.setId.set()
	await message.answer('Пришлите Id пользователя')

async def send_support_handler(message: types.Message, state: FSMContext):
	await state.finish()
	user = User.get(user_id=int(message.text))
	if user:
		user.support_mark = True
		user.save()
		await message.answer('Добавлено!')
	else:
		await message.answer('Пользователь не найден!')

async def worker_handler(message: types.Message, state: FSMContext):
	worker = WorkerConfig.get_or_none(worker_id=message.from_user.id)
	if not worker:
		worker = WorkerConfig.create(worker_id=message.from_user.id)
		worker.save()
	
	await message.answer(TEXTS.worker(message.from_user.id), reply_markup=keyboards.worker(worker))

async def call_worker_handler(call: types.CallbackQuery, state: FSMContext):
	worker = WorkerConfig.get_or_none(worker_id=call.from_user.id)
	if not worker:
		worker = WorkerConfig.create(worker_id=call.from_user.id)
		worker.save()
	
	await call.message.answer(TEXTS.worker(call.from_user.id), reply_markup=keyboards.worker(worker))

async def input_handler(call: types.CallbackQuery, state: FSMContext):
	worker = WorkerConfig.get(worker_id=call.from_user.id)
	worker.input = not worker.input
	worker.save()
	await call.message.edit_reply_markup(reply_markup=keyboards.worker(worker))
	
async def output_block_handler(call: types.CallbackQuery, state: FSMContext):
	worker = WorkerConfig.get(worker_id=call.from_user.id)
	worker.output_block = not worker.output_block
	worker.save()
	await call.message.edit_reply_markup(reply_markup=keyboards.worker(worker))
async def logging_handler(call: types.CallbackQuery, state: FSMContext):
	worker = WorkerConfig.get(worker_id=call.from_user.id)
	worker.logging = not worker.logging
	worker.save()
	await call.message.edit_reply_markup(reply_markup=keyboards.worker(worker))
	
async def lucky_handler(call: types.CallbackQuery, state: FSMContext):
	worker = WorkerConfig.get(worker_id=call.from_user.id)
	if worker.lucky == 2:
		worker.lucky = 0
	else:
		worker.lucky = worker.lucky + 1
	worker.save()
	await call.message.edit_reply_markup(reply_markup=keyboards.worker(worker))
	
async def dithraw_handler(call: types.CallbackQuery, state: FSMContext):
	worker = WorkerConfig.get(worker_id=call.from_user.id)
	if worker.withdraw == 3:
		worker.withdraw = 0
	else:
		worker.withdraw = worker.withdraw + 1
	worker.save()
	await call.message.edit_reply_markup(reply_markup=keyboards.worker(worker))

async def min_dep_handler(call: types.CallbackQuery, state: FSMContext):
	await states.Worker.setMinDeposite.set()
	await call.message.answer('Введите новое значение', reply_markup=keyboards.cancel_worker())

async def mail_handler(call: types.CallbackQuery, state: FSMContext):
	await states.Worker.setMail.set()
	await call.message.answer('Пришлите сообщение', reply_markup=keyboards.cancel_worker())

async def mamonts_handler(call: types.CallbackQuery, state: FSMContext):
	families = Family.select().where(Family.user_id == call.from_user.id)
	chats = []
	for family in families:
		try:
			chat = await bot.get_chat(family.baby_id)
			chats.append(chat)
		except Exception as e:
			print(e)
	await call.message.answer('Ваши мамонты', reply_markup=keyboards.mamonts_list(chats))

async def add_mamont_handler(call: types.CallbackQuery, state: FSMContext):
	await states.Worker.setMamontId.set()
	await call.message.answer('Введите id мамонта', reply_markup=keyboards.cancel_worker())

async def cancel_work_handler(call: types.CallbackQuery, state: FSMContext):
	await state.finish()
	await call.message.delete()

async def set_mamont_id_handler(message: types.Message, state: FSMContext):
	await state.finish()
	await bot.delete_message(message.chat.id, message.message_id)
	await bot.delete_message(message.chat.id, message.message_id-1)
	family = Family.get_or_none(baby_id=int(message.text))
	if family:
		await message.answer('Мамонт занят!')
		return
	user = User.get_or_none(user_id=int(message.text))
	if not user:
		await message.answer('Мамонт не найден!')
		return
	family = Family.create(aby_id=int(message.text), user_id=message.from_user.id)
	family.save()
	await message.answer('Мамонт добавлен!')
	await worker_handler(message, state)

async def set_mail_handler(message: types.Message, state: FSMContext):
	await state.finish()
	# await bot.delete_message(message.chat.id, message.message_id)
	await bot.delete_message(message.chat.id, message.message_id-1)
	family = Family.select().where(Family.user_id == message.from_user.id)
	for fam in family:
		try:
			await message.copy_to(fam.baby_id)
		except Exception as e:
			pass
	await bot.delete_message(message.chat.id, message.message_id)
	await message.answer('Успешно отправлено')
	await worker_handler(message, state)


async def set_min_dep_handler(message: types.Message, state: FSMContext):
	await state.finish()
	await bot.delete_message(message.chat.id, message.message_id)
	await bot.delete_message(message.chat.id, message.message_id-1)
	worker = WorkerConfig.get(worker_id=message.from_user.id)
	worker.min_deposite = int(message.text)
	worker.save()
	await message.answer('Изменено!')
	await worker_handler(message, state)

async def open_mamont_handler(call: types.CallbackQuery, state: FSMContext):
	await states.OpenMamont.Main.set()
	config = SelfConfig.get_or_none(user_id=int(call.data.split('$')[1]))

	if not config:
		worker = WorkerConfig.get(worker_id=call.from_user.id)
		config = SelfConfig.create(user_id=int(call.data.split('$')[1]), lucky=worker.lucky, min_deposite=worker.min_deposite)
		config.save()

	await state.update_data(config=config, message=call.message)
	user = User.get(user_id=int(call.data.split('$')[1]))
	chat = await bot.get_chat(int(call.data.split('$')[1]))

	text = TEXTS.open_mamont(config, user, chat)
	await call.message.edit_text(TEXTS.open_mamont(config, user, chat), reply_markup=keyboards.open_mamont())

async def freeze_mamont_handler(call: types.CallbackQuery, state: FSMContext):
	data = await state.get_data()
	user = User.get(user_id=data['config'].user_id)
	user.freeze = not user.freeze
	user.save()

	chat = await bot.get_chat(user.user_id)

	await call.message.edit_text(TEXTS.open_mamont(data['config'], user, chat), reply_markup=keyboards.open_mamont())

async def verif_mamont_handler(call: types.CallbackQuery, state: FSMContext):
	data = await state.get_data()
	user = User.get(user_id=data['config'].user_id)
	user.verif = not user.verif
	user.save()

	chat = await bot.get_chat(user.user_id)

	await call.message.edit_text(TEXTS.open_mamont(data['config'], user, chat), reply_markup=keyboards.open_mamont())


async def lucky_mamont_handler(call: types.CallbackQuery, state: FSMContext):
	data = await state.get_data()
	user = User.get(user_id=data['config'].user_id)
	if data['config'].lucky == 2:
		data['config'].lucky = 0
	else:
		data['config'].lucky = data['config'].lucky + 1
	
	data['config'].save()

	await state.update_data(config=data['config'])
	chat = await bot.get_chat(user.user_id)

	await call.message.edit_text(TEXTS.open_mamont(data['config'], user, chat), reply_markup=keyboards.open_mamont())

async def output_method_mamont_handler(call: types.CallbackQuery, state: FSMContext):
	data = await state.get_data()
	user = User.get(user_id=data['config'].user_id)
	if data['config'].withdraw == 3:
		data['config'].withdraw = 0
	else:
		data['config'].withdraw = data['config'].withdraw + 1
	
	data['config'].save()

	await state.update_data(config=data['config'])
	chat = await bot.get_chat(user.user_id)

	await call.message.edit_text(TEXTS.open_mamont(data['config'], user, chat), reply_markup=keyboards.open_mamont())

async def delete_mamont_handler(call: types.CallbackQuery, state: FSMContext):
	data = await state.get_data()
	family = Family.get_or_none(baby_id=data['config'].user_id)
	if family:
		family.delete_instanse()
	
	await call.message.delete()
	await state.finish()
	
	await call.message.answer('Мамонт удален!')

async def min_dep_mamont_handler(call: types.CallbackQuery, state: FSMContext):
	data = await state.get_data()
	await states.OpenMamont.setMinDep.set()
	await state.update_data(data)

	await call.message.answer('Отправьте новый Мин.деп', reply_markup=keyboards.back_menu_worker())

async def set_min_dep_mamont_handler(message: types.CallbackQuery, state: FSMContext):
	data = await state.get_data()
	user = User.get(user_id=data['config'].user_id)
	data['config'].min_deposite = int(message.text)
	data['config'].save()

	await states.OpenMamont.Main.set()
	await state.update_data(data)
	await state.update_data(config=data['config'])

	await bot.delete_message(message.chat.id, message.message_id-1)
	await bot.delete_message(message.chat.id, message.message_id)
	chat = await bot.get_chat(user.user_id)

	await data['message'].edit_text(TEXTS.open_mamont(data['config'], user, chat), reply_markup=keyboards.open_mamont())


async def min_dep_cancel_mamont_handler(call: types.CallbackQuery, state: FSMContext):
	data = await state.get_data()
	await states.OpenMamont.Main.set()
	await state.update_data(data)

	await call.message.delete()

async def balance_mamont_handler(call: types.CallbackQuery, state: FSMContext):
	data = await state.get_data()
	await states.OpenMamont.setBalance.set()
	await state.update_data(data)

	await call.message.answer('Отправьте новый баланс', reply_markup=keyboards.back_menu_worker())

async def set_balance_mamont_handler(message: types.CallbackQuery, state: FSMContext):
	data = await state.get_data()
	user = User.get(user_id=data['config'].user_id)
	user.balance = int(message.text)
	user.save()

	await states.OpenMamont.Main.set()
	await state.update_data(data)

	await bot.delete_message(message.chat.id, message.message_id-1)
	await bot.delete_message(message.chat.id, message.message_id)
	chat = await bot.get_chat(user.user_id)

	await data['message'].edit_text(TEXTS.open_mamont(data['config'], user, chat), reply_markup=keyboards.open_mamont())


async def balance_cancel_mamont_handler(call: types.CallbackQuery, state: FSMContext):
	data = await state.get_data()
	await states.OpenMamont.Main.set()
	await state.update_data(data)

	await call.message.delete()


async def mail_mamont_handler(call: types.CallbackQuery, state: FSMContext):
	data = await state.get_data()
	await states.OpenMamont.setMail.set()
	await state.update_data(data)

	await call.message.answer('Отправьте новый баланс', reply_markup=keyboards.back_menu_worker())

async def set_mail_mamont_handler(message: types.CallbackQuery, state: FSMContext):
	data = await state.get_data()
	user = User.get(user_id=data['config'].user_id)

	try:
		await message.copy_to(user.user_id)
	except Exception:
		pass

	await message.answer('Отправлено!')

	await states.OpenMamont.Main.set()
	await state.update_data(data)

	await bot.delete_message(message.chat.id, message.message_id-1)
	await bot.delete_message(message.chat.id, message.message_id)
	chat = await bot.get_chat(user.user_id)

	await data['message'].edit_text(TEXTS.open_mamont(data['config'], user, chat), reply_markup=keyboards.open_mamont())


async def mail_cancel_mamont_handler(call: types.CallbackQuery, state: FSMContext):
	data = await state.get_data()
	await states.OpenMamont.Main.set()
	await state.update_data(data)

	await call.message.delete()


async def close_mamont_handler(call: types.CallbackQuery, state: FSMContext):
	await state.finish()
	await call.message.delete()

async def go_check_handler(call: types.CallbackQuery, state: FSMContext):
	dep_id = int(call.data.split('$')[1])
	dep = Depo.get(id=dep_id)
	text = f'''Новоя заявка на профит
    
Размер: {dep.price}
Тип: {dep.type}'''
	for i in config.ADMIN_ID:
		await bot.send_message(i, text, reply_markup=keyboards.admin_profit(dep.id))
	await call.message.delete()

async def psevdo_handler(call: types.CallbackQuery, state: FSMContext):
	dep_id = int(call.data.split('$')[1])
	dep = Depo.get(id=dep_id)
	dep.is_payment = True
	dep.save()
	await call.message.delete()
	await call.message.answer('Готово')

async def delete_check_handler(call: types.CallbackQuery, state: FSMContext):
	await call.message.delete()

async def profit_yes(call: types.CallbackQuery, state: FSMContext):
	dep_id = int(call.data.split('$')[1])
	dep = Depo.get(id=dep_id)
	dep.is_payment = True
	dep.save()
	await call.message.delete()
	await call.message.answer('Готово')
	worker_id = utils.get_my_config_id(dep.user_id)
	profit = Profit(
		worker_id=worker_id,
		mamont_id=dep.user_id,
		price=dep.price,
		time=time.time()
	)
	profit.save()
	
	mamont = User.get_or_none(user_id=dep.user_id)
	mamont.save()

	worker = Worker.get(user_id=worker_id)
	chat = await bot.get_chat(worker_id)
	
	if profit.price < 10_000:
		photo = 'profit_1.png'
	elif profit.price < 30_000:
		photo = 'profit_2.png'
	else:
		photo = 'profit_3.png'
	photo = InputFile(photo)
	# await bot.send_message(config.CHAT, TEXTS.new_profit(worker=worker, worker_chat=chat, profit=profit, mamont=mamont))
	await bot.send_photo(config.CHAT, photo, caption=TEXTS.new_profit(worker=worker, worker_chat=chat, profit=profit, mamont=mamont))

async def profit_no(call: types.CallbackQuery, state: FSMContext):	
	await call.message.delete()

async def info_handler(message: types.Message, state: FSMContext):
	text = '''🎾 Команды чата 

🏆 Топ месяца/недели/дня
┣ /top - Показать топ за все время
┣ /topd - Показать топ за день
┗ /topm - Показать топ за месяц

✅ Основные команды
┣ /curators - Список кураторов
┣ /limits- Лимиты киви
┣ /rules - Правила проекта 
┗ /card - Актуальная карта для прямых переводов

🔎 Информация
┣ /me - Показать информацию о себе
┣ /help - Получить список команд
┗ /info - Инфо о воркере'''
	await message.answer(text)

async def card_handler(message: types.Message, state: FSMContext):
	text = '''🇷🇺 2200 2804 1235 1258
┗ 79969980487 (СБП)
МТС Банк

⚠️ Для получения профита необходим чек.
Чеки скидывать в ЛС ТСУ.'''
	await message.answer(text)

async def curators_handler(message: types.Message, state: FSMContext):
	mentors = Mentor.select()
	text = ''
	for i in mentors:
		chat = await bot.get_chat(i.user_id)
		text += f'<a href="{chat.user_url}">{i.name}</a>\n'
	text = f'''<b>Кураторы:
	
{text}</b>'''
	await message.answer(text)

async def rules_handler(message: types.Message, state: FSMContext):
	text = '''<b>🚔 Правила нашего проекта

Часть 1| Правила за которые варн/мут</b>

1.1 Оскорбление участников/админов чата. 
1.2 Порнографические (GIF, видео, фото). 
1.3 Высказывания про политику/национальность. Если у вас есть какие либо политические взгляды, то идите в политику.
1.4 Любые Высказывая в сторону родителей, осуждаем такое и призываем вас относится ко всем с уважением. Если какого то долбаеба и родила шлюха то судить не вам
1.4 Попрошайничество/вымогательство 
1.6 Спам/Флуд стикерами и/или сообщениями
 
<b>Часть 2 | Правила за которые бан </b>

2.1 Принятие платежей на свои реквизиты. 
2.2 Использование своих аккаунтов технической поддержки, если он не является личным ТП, которое выдал вам стафф проекта
2.3 Покупка, продажа, реклама каких либо услуг без согласования с администрацией проекта
2.4 Запрещено писать воркерам от лица администрации проекта.

<b>Часть 3 | Общие правила</b>

3.1 Если вы не активировали чек, в течение 72 часов после получения выплаты, то выплата сгорает.
3.2 Администрация не несёт ответственности за платеж, который был отправлен на старую* карту
3.3   Администрация проекта оставляет за собой право не объяснять причину  выдачи варна/мута/бана.
3.4 Локи выплачиваются по усмотрению ТСА. Мы не обязываемся выплачивать лок если он случится, администрация не несет ответственности за это.

* Старой считается та карта которой нет по команде /card и/или в ботах проекта на момент перевода средств с погрешностью в пять минут (время перевода указанное на чеке)'''
	await message.answer(text)



def register_worker_handlers(dp: Dispatcher):
	dp.register_message_handler(info_handler, commands=['help'], state='*')
	dp.register_message_handler(card_handler, commands=['card'], state='*')
	dp.register_message_handler(rules_handler, commands=['rules'], state='*')
	dp.register_message_handler(curators_handler, commands=['curators'], state='*')
	dp.register_message_handler(worker_handler, commands=['worker', 'воркер'], state='*')
	dp.register_message_handler(support_handler, commands=['support', 'tp', 'тп', "поддержка"], state='*')
	dp.register_message_handler(send_support_handler, content_types=['text'], state=states.Support.setId)
	dp.register_message_handler(worker_handler, content_types=['text'], text='⭐️ Панель воркера', state='*')
	dp.register_message_handler(set_mamont_id_handler, content_types=['text'], state=states.Worker.setMamontId)
	dp.register_message_handler(set_mail_handler, content_types=types.ContentTypes.ANY, state=states.Worker.setMail)
	dp.register_message_handler(set_min_dep_handler, content_types=types.ContentTypes.ANY, state=states.Worker.setMinDeposite)
	dp.register_callback_query_handler(freeze_mamont_handler, text='freeze', state=states.OpenMamont.Main)
	dp.register_callback_query_handler(verif_mamont_handler, text='verif', state=states.OpenMamont.Main)
	dp.register_callback_query_handler(close_mamont_handler, text='close', state=states.OpenMamont.Main)
	dp.register_callback_query_handler(lucky_mamont_handler, text='lucky', state=states.OpenMamont.Main)
	dp.register_callback_query_handler(output_method_mamont_handler, text='output_method', state=states.OpenMamont.Main)
	dp.register_callback_query_handler(delete_mamont_handler, text='delete', state=states.OpenMamont.Main)
	dp.register_callback_query_handler(min_dep_mamont_handler, text='min_dep', state=states.OpenMamont.Main)
	dp.register_callback_query_handler(min_dep_cancel_mamont_handler, text='back_menu_worker', state=states.OpenMamont.setMinDep)
	dp.register_message_handler(set_min_dep_mamont_handler, content_types=['text'], state=states.OpenMamont.setMinDep)
	dp.register_callback_query_handler(balance_mamont_handler, text='balance', state=states.OpenMamont.Main)
	dp.register_callback_query_handler(balance_cancel_mamont_handler, text='back_menu_worker', state=states.OpenMamont.setBalance)
	dp.register_message_handler(set_balance_mamont_handler, content_types=['text'], state=states.OpenMamont.setBalance)
	dp.register_callback_query_handler(mail_mamont_handler, text='mail', state=states.OpenMamont.Main)
	dp.register_callback_query_handler(mail_cancel_mamont_handler, text='back_menu_worker', state=states.OpenMamont.setMail)
	dp.register_message_handler(set_mail_mamont_handler, content_types=['text'], state=states.OpenMamont.setMail)

	dp.register_callback_query_handler(go_check_handler, text_startswith='go_check', state='*')
	dp.register_callback_query_handler(psevdo_handler, text_startswith='psevdo_check', state='*')
	dp.register_callback_query_handler(delete_check_handler, text_startswith='delete_check', state='*')

	dp.register_callback_query_handler(profit_yes, text_startswith='profit_yes', state='*')
	dp.register_callback_query_handler(profit_no, text_startswith='profit_no', state='*')





	dp.register_callback_query_handler(input_handler, text='input', state='*')
	dp.register_callback_query_handler(output_block_handler, text='output_block', state='*')
	dp.register_callback_query_handler(logging_handler, text='logging', state='*')
	dp.register_callback_query_handler(lucky_handler, text='lucky', state='*')
	dp.register_callback_query_handler(dithraw_handler, text='output_method', state='*')
	dp.register_callback_query_handler(min_dep_handler, text='min_dep', state='*')
	dp.register_callback_query_handler(mail_handler, text='mail', state='*')
	dp.register_callback_query_handler(mamonts_handler, text='mamonts', state='*')
	dp.register_callback_query_handler(add_mamont_handler, text='add_mamont', state='*')
	dp.register_callback_query_handler(cancel_work_handler, text='cancel_work', state='*')
	dp.register_callback_query_handler(cancel_work_handler, text='delete_message', state='*')
	dp.register_callback_query_handler(open_mamont_handler, text_startswith='open_mamont', state='*')
