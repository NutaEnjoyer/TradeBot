from apscheduler.schedulers.asyncio import AsyncIOScheduler

from aiogram.utils import executor
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import BotCommand

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from start_bot.helper_bot_container import bot

scheduler = AsyncIOScheduler()

dp = Dispatcher(bot, storage=MemoryStorage())

bot_commands = [
        BotCommand(command="/help", description="Помощь"),
        BotCommand(command="/top", description="Вывод топов"),
        BotCommand(command="/card", description="Карта"),
        BotCommand(command="/me", description="Информация о вас")
    ]
async def do_some():
    pass

def schedule_job():
    scheduler.add_job(do_some, 'interval', seconds=5)

async def __on_start_up(dp: Dispatcher) -> None:
    from handlers import register_all_handlers

    register_all_handlers.register_helper(dp)

    await bot.set_my_commands(bot_commands)

    schedule_job()

def start_bot():
    scheduler.start()
    executor.start_polling(dp, skip_updates=True, on_startup=__on_start_up)
