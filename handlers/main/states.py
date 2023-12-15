from aiogram.dispatcher.filters.state import StatesGroup, State

class Future(StatesGroup):
    setAmount = State()
    setTimeHand = State()
    setTime = State()
    setCredit = State()
    setType = State()

class Deposite(StatesGroup):
    setAmount = State()

class Worker(StatesGroup):
    setMinDeposite = State()
    setMail = State()
    setMamontId = State()

class OpenMamont(StatesGroup):
    Main = State()
    setLucky = State()
    setMinDep = State()
    setBalance = State()
    setMail = State()
    
class Withdraw(StatesGroup):
    setAmount = State()
    setRequisites = State()

    
class Support(StatesGroup):
    setId = State()
    
