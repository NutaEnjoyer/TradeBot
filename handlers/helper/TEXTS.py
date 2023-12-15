from models import *
import time

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
def calculate_profit_stats(start_date, end_date, user_id):
	profits = Profit.select().where((Profit.time.between(start_date, end_date)) & (Profit.worker_id==user_id))
		
	total_profit = sum([i.price for i in profits])
	count_profit = profits.count()
		
	return count_profit, total_profit

start = 'Главное меню'

def profile(user):
    
    worker = Worker.get(user_id=user.id)
    profits = calculate_profit_stats(0, time.time(), user.id)
    dates = round((time.time() - worker.created_time)//(24*60*60))
    print((time.time() - worker.created_time))
    print(24*60*60)
    print(dates)
    print(worker.useTag)
    if worker.mentor_id:
        mentor = Mentor.get(id=worker.mentor_id)
        mentor = mentor.name

    else:
         mentor = '-'
    avarage = 0
    if profits[0]: avarage = profits[1] // profits[0]
    text = f'''<b>📂 Твой профиль:
{user.first_name}</b>

💸 У тебя {profits[0]} профитов на сумму {profits[1]} RUB
Средний профит: {avarage} RUB

<b>{'🌕' if worker.useTag else '🌑'} Твой скрытый тег:
#{worker.tag}</b>

👨‍💻 Статус: <b>Воркер</b>
👨‍🏫 Куратор: <b>{mentor}</b>

⚠️ Предупреждений:
[0/3]
📅 <i>В команде</i>: {dates} дн.'''
    
    return text

