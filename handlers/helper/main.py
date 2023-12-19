from aiogram.dispatcher import FSMContext
from aiogram.types import InputFile

from start_bot.helper_bot import bot, dp
from aiogram import types, Dispatcher

from data import config
from models import *
from handlers.helper import keyboards
from handlers.helper import states

from handlers.helper import TEXTS, utils

import time

async def set_card_handler(message: types.Message, state: FSMContext):
	args = message.get_args()
	if args:
		args = args.split()
		if len(args) != 1:
			await message.answer('Неверный ввод!\n\n<code>/set_card new_value</code>')
			return
	else:
		await message.answer('Неверный ввод!\n\n<code>/set_card new_value</code>')
		return
	t = TeamConfig.select()
	t[0].card = args[0]
	t[0].save()
	await message.answer('Готово!')
	
async def set_number_handler(message: types.Message, state: FSMContext):
	args = message.get_args()
	if args:
		args = args.split()
		if len(args) != 1:
			await message.answer('Неверный ввод!\n\n<code>/set_number new_value</code>')
			return
	else:
		await message.answer('Неверный ввод!\n\n<code>/set_number new_value</code>')
		return

	t = TeamConfig.select()
	t[0].number = args[0]
	t[0].save()
	await message.answer('Готово!')
	
async def profit_handler(message: types.Message, state: FSMContext):
	args = message.get_args()
	if args:
		print(args)
		args = args.split()
		if len(args) != 2:
			await message.answer('Неверный ввод!\n\n<code>/profit userId value</code>')
			return
		profit = Profit(
			worker_id=int(args[0]),
			mamont_id=None,
			price=int(args[1]),
			time=time.time()
		)
		profit.save()
		worker = Worker.get(user_id=int(args[0]))
		chat = await bot.get_chat(int(args[0]))
		if profit.price < 10_000:
			photo = 'profit_1.png'
		elif profit.price < 30_000:
			photo = 'profit_2.png'
		else:
			photo = 'profit_3.png'
		photo = InputFile(photo)
		await message.answer('start')
		# await bot.send_message(config.CHAT, TEXTS.new_profit(worker=worker, worker_chat=chat, profit=profit, mamont=mamont))
		await bot.send_photo(config.CHAT, photo, caption=TEXTS.new_profit(worker=worker, worker_chat=chat, profit=profit, mamont=None))
		await message.answer('Готово')

		# await bot.send_message(config.CHAT, TEXTS.new_profit(worker=worker, worker_chat=chat, profit=profit, mamont=None))
	else:
		await message.answer('/profit user_id price')

async def start_handler(message: types.Message, state: FSMContext):
	await state.finish()
	worker = Worker.get_or_none(user_id=message.from_user.id)
	if not worker:
		worker = Worker.create(
             	user_id=message.from_user.id,
                tag=utils.generate_random_tag(),
                created_time=time.time()
                )
		worker.save()
	await message.answer(TEXTS.start, reply_markup=keyboards.start())


async def bots(message: types.Message, state: FSMContext):
    await message.answer('<b>📊 Трейдинг 2.0</b>', reply_markup=keyboards.bots())

async def main_menu(message: types.Message, state: FSMContext):
	profits = Profit.select()
	profits = [i.price for i in profits]
	text = f'''<b>💻 О проекте</b>
	
💠 Мы открылись: 14.02.2023
💸Количество профитов: <b>{len(profits)}</b>
💰Общая сумма профитов: <b>{sum(profits)} ₽</b>

<b>Выплаты</b> проекта:
Залет - <b>80%</b>
Залет с помощью тех. поддержки - <b>70%</b>

<b>Состояние</b> сервисов:
🟡 Трейдинг 2.0
🟡 Общий статус: Ворк'''
	await message.answer(text, reply_markup=keyboards.main())

async def profile(message: types.Message, state: FSMContext):
    await message.answer(TEXTS.profile(message.from_user), reply_markup=keyboards.profile())


async def change_tag(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer('Пришлите новый тег', reply_markup=keyboards.cancel())
    await states.Tag.Set.set()

async def switch_tag(call: types.CallbackQuery, state: FSMContext):
    worker = Worker.get(user_id=call.from_user.id)
    worker.useTag = not worker.useTag
    worker.save() 
    await call.message.edit_text(TEXTS.profile(call.from_user), reply_markup=keyboards.profile())
    
async def cancel_handler(call: types.CallbackQuery, state: FSMContext):
     await state.finish()
     await call.message.delete()

async def link_mentor_handler(call: types.CallbackQuery, state: FSMContext):
     await state.finish()
     await call.message.delete()
     mentor_id = int(call.data.split('$')[1])
     worker = Worker.get(user_id=call.from_user.id)
     worker.mentor_id = mentor_id
     worker.save()
    

async def set_tag(message: types.Message, state: FSMContext):
	worker = Worker.get(user_id=message.from_user.id)
	worker.tag = message.text[:15]
	worker.save()
	await message.answer(TEXTS.profile(message.from_user), reply_markup=keyboards.profile())
    
async def mentor_handler(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer('Выберите куратора:', reply_markup=keyboards.mentors())
 
async def check_check(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer('Пришлите чек', reply_markup=keyboards.cancel())
    await states.Check.Send.set()

async def report_card(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer('Пришлите карту', reply_markup=keyboards.cancel())
    await states.Card.Send.set()

async def set_card(message: types.Message, state: FSMContext):
	await message.answer('Жалоба отправлена')
	await state.finish()
	report = ReportedCard.create(value=message.text)
	report.save()
      
async def set_check(message: types.Message, state: FSMContext):
	await message.answer('Чек отправлен')
	await state.finish()
	for user_id in config.CHECKERS:
		try:
			await bot.copy_message(user_id, message.chat.id, message_id=message.message_id)
			await bot.send_message(user_id, f'''Новый чек!\n\nДля регистрации профита:\n
				<code>/profit {message.from_user.id} </code> и сумма''')
		except Exception as e:
			print(e)

def calculate_profit_stats(start_date, end_date, user_id):
    # Фильтрация по временному интервалу
	profits = Profit.select().where((Profit.time.between(start_date, end_date)) & (Profit.worker_id==user_id))
		
		# Расчет суммы и количества profit'ов
	total_profit = sum([i.price for i in profits])
	count_profit = profits.count()
		
	return count_profit, total_profit


async def me_handler(message: types.Message, state: FSMContext):
	worker = Worker.get_or_none(user_id=message.from_user.id)
	if not worker:
		await message.answer('Вы не являетесь воркером')
		return
	
	start_date = int(time.time() - 86400)
	end_date = int(time.time())
	day = calculate_profit_stats(start_date, end_date, message.from_user.id)
	start_date = int(time.time() - 604800)
	end_date = int(time.time())
	week = calculate_profit_stats(start_date, end_date, message.from_user.id)
	start_date = int(time.time() - 2592000)
	end_date = int(time.time())
	month = calculate_profit_stats(start_date, end_date, message.from_user.id)
	full = calculate_profit_stats(0, end_date, message.from_user.id)
	chat = await bot.get_chat(message.from_user.id)
	work = f'<a href="{chat.user_url}">{chat.first_name}</a>'
	dates = round((time.time() - worker.created_time)//(24*60*60))

	text = f'''👨‍💻 Воркер - {work}
Telegram ID: {message.from_user.id}

<b>{full[0]}</b> профитов на сумму: <b>{full[1]}₽</b>

Чистый профит: <b>{round(full[1] * 0.8)}₽</b>
Средний профит: <b>{round((full[1] / full[0]) if full[0] else 0)}₽</b>
В команде: {dates} дня, 0 варнов'''
# 	text = f'''<b>Профиты {message.from_user.first_name}:

# За день: {day[0]} профитов на {day[1]} р
# За неделю: {week[0]} профитов на {week[1]} р
# За месяц: {month[0]} профитов на {month[1]} р</b>'''
	
	await message.answer(text)


async def info_handler(message: types.Message, state: FSMContext):
	text = '''🎾 Команды чата 

🏆 Топ месяца/недели/дня
┣ /top - Показать топ за все время
┣ /topd - Показать топ за день
┗ /topm - Показать топ за месяц

✅ Основные команды
┣ /curators - Список кураторов
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
1.5 Попрошайничество/вымогательство 
1.6 Спам/Флуд стикерами и/или сообщениями
1.7 Профит без воркера - на развитие проекта (Если работник в течении 24 часов не прислал документа, подтверждающего что профит его)
 
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

def get_top_10_workers(min_time=0):
    # Подсчет суммы price для каждого worker_id с условием time больше min_time
    worker_prices = Profit.select(Profit.worker_id, fn.Sum(Profit.price).alias('price_sum')) \
        .where(Profit.time > min_time) \
        .group_by(Profit.worker_id) \
        .order_by(SQL('price_sum DESC')) \
        .limit(10)

    top_10_worker_ids = [worker.worker_id for worker in worker_prices]

    # Создание списка для каждого worker_id с данными [worker_id, price_sum, price_len]
    top_10_workers = []

    for worker_id in top_10_worker_ids:
        worker_data = [worker_id, 0.0, 0]

        # Получение суммы price и количества записей для текущего worker_id с условием time больше min_time
        worker_info = Profit.select(fn.Sum(Profit.price).alias('price_sum'), fn.Count(Profit.price).alias('price_len')) \
            .where(Profit.worker_id == worker_id, Profit.time > min_time) \
            .group_by(Profit.worker_id) \
            .first()

        if worker_info:
            worker_data[1] = worker_info.price_sum
            worker_data[2] = worker_info.price_len

        top_10_workers.append(worker_data)

    return top_10_workers

async def top_handler(message: types.Message, state: FSMContext):
	top_10_workers = get_top_10_workers()
	print(top_10_workers)
	full_profit = Profit.select().where(Profit.time > 0)
	full_profit = sum([i.price for i in full_profit])
	text = f'''<b>🪐 Топ воркеров за все время:</b>\n\n'''
	num = 0
	for i in top_10_workers:
		num += 1
		worker = Worker.get(user_id=i[0])
		worker_chat = await bot.get_chat(i[0])
		if num == 1:
			number = '🥇'
		elif num == 2:
			number = '🥈'
		elif num == 3:
			number = '🥉'
		else: 
			number = num
		tag = f'#{worker.tag}' if worker.useTag else f'''<a href="{worker_chat.user_url}">{worker_chat.first_name}</a>'''
		tag = f'{tag} - <b>{i[1]}₽</b> - Профитов: {i[2]}'
		tag = f'{number} - {tag}\n'
		text+=tag
	text += f'\n<b>💰Общий профит: {full_profit}₽</b>'
	await message.answer(text)

async def topd_handler(message: types.Message, state: FSMContext):
	min_time = time.time() - 7 * 24* 60 * 60
	top_10_workers = get_top_10_workers(min_time)
	print(top_10_workers)
	full_profit = Profit.select().where(Profit.time > min_time)
	full_profit = sum([i.price for i in full_profit])
	text = f'''<b>🪐 Топ воркеров за день:</b>\n\n'''
	num = 0
	for i in top_10_workers:
		num += 1
		worker = Worker.get(user_id=i[0])
		worker_chat = await bot.get_chat(i[0])
		if num == 1:
			number = '🥇'
		elif num == 2:
			number = '🥈'
		elif num == 3:
			number = '🥉'
		else: 
			number = num
		tag = f'#{worker.tag}' if worker.useTag else f'''<a href="{worker_chat.user_url}">{worker_chat.first_name}</a>'''
		tag = f'{tag} - <b>{i[1]}₽</b> - Профитов: {i[2]}'
		tag = f'{number} - {tag}\n'
		text+=tag
	text += f'\n<b>💰Общий профит: {full_profit}₽</b>'
	await message.answer(text)

async def topm_handler(message: types.Message, state: FSMContext):
	min_time = time.time() - 30 * 24* 60 * 60
	top_10_workers = get_top_10_workers(min_time)
	print(top_10_workers)
	full_profit = Profit.select().where(Profit.time > min_time)
	full_profit = sum([i.price for i in full_profit])
	text = f'''<b>🪐 Топ воркеров за месяц:</b>\n\n'''
	num = 0
	for i in top_10_workers:
		num += 1
		worker = Worker.get(user_id=i[0])
		worker_chat = await bot.get_chat(i[0])
		if num == 1:
			number = '🥇'
		elif num == 2:
			number = '🥈'
		elif num == 3:
			number = '🥉'
		else: 
			number = num
		tag = f'#{worker.tag}' if worker.useTag else f'''<a href="{worker_chat.user_url}">{worker_chat.first_name}</a>'''
		tag = f'{tag} - <b>{i[1]}₽</b> - Профитов: {i[2]}'
		tag = f'{number} - {tag}\n'
		text+=tag
	text += f'\n<b>💰Общий профит: {full_profit}₽</b>'
	await message.answer(text)

async def mail_handler(message: types.Message, state: FSMContext):
	await states.Worker.setMail.set()
	await message.answer('Пришлите сообщение', reply_markup=keyboards.cancel())


async def set_mail_handler(message: types.Message, state: FSMContext):
	await state.finish()
	# await bot.delete_message(message.chat.id, message.message_id)
	await bot.delete_message(message.chat.id, message.message_id-1)
	workers = Worker.select()
	for worker in workers:
		try:
			await message.copy_to(worker.user_id)
		except Exception as e:
			pass
	await bot.delete_message(message.chat.id, message.message_id)
	await message.answer('Успешно отправлено')


def register_handlers(dp: Dispatcher):
	dp.register_message_handler(mail_handler, commands=['mail'], state='*')
	dp.register_message_handler(set_mail_handler, content_types=types.ContentTypes.ANY, state=states.Worker.setMail)


	dp.register_message_handler(top_handler, commands=['top'], state='*')
	dp.register_message_handler(topd_handler, commands=['topd'], state='*')
	dp.register_message_handler(topm_handler, commands=['topm'], state='*')

	dp.register_message_handler(me_handler, commands=['info', 'me'], state='*')
	dp.register_message_handler(info_handler, commands=['help'], state='*')
	dp.register_message_handler(card_handler, commands=['card'], state='*')
	dp.register_message_handler(rules_handler, commands=['rules'], state='*')
	dp.register_message_handler(curators_handler, commands=['curators'], state='*')
	dp.register_message_handler(start_handler, commands=['start', 'restart'], state='*')
	dp.register_message_handler(profit_handler, commands=['profit'], state='*')
	dp.register_message_handler(set_card_handler, commands=['set_card'], state='*')
	dp.register_message_handler(set_number_handler, commands=['set_number'], state='*')
	dp.register_message_handler(main_menu, content_types=['text'], state='*', text='💻 О проекте')
	dp.register_message_handler(profile, content_types=['text'], state='*', text='📁 Мой профиль')
	dp.register_message_handler(bots, content_types=['text'], state='*', text='📊 Трейдинг 2.0')
	dp.register_callback_query_handler(change_tag, text='change_tag', state='*')
	dp.register_callback_query_handler(switch_tag, text='switch_tag', state='*')
	dp.register_callback_query_handler(cancel_handler, text='cancel', state='*')
	dp.register_callback_query_handler(link_mentor_handler, text_startswith='link_mentor', state='*')
	dp.register_message_handler(set_tag, content_types=['text'], state=states.Tag.Set)
	dp.register_callback_query_handler(mentor_handler, text='mentor', state='*')
	dp.register_callback_query_handler(check_check, text='check_check', state='*')
	dp.register_callback_query_handler(report_card, text='report_card', state='*')
	dp.register_message_handler(set_card, content_types=['text'], state=states.Card.Send)
	dp.register_message_handler(set_check, content_types=types.ContentTypes.ANY, state=states.Check.Send)
