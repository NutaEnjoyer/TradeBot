from aiogram.dispatcher.filters.state import StatesGroup, State

class Tag(StatesGroup):
    Set = State()

class Check(StatesGroup):
    Send = State()

class Card(StatesGroup):
    Send = State()

class Worker(StatesGroup):
    setMail = State()