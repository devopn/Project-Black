from aiogram import Router, types
from aiogram.filters import Command

router = Router()

@router.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer('''
Привет, это бот для прогноза погоды!
Он сделан чтобы помочь вам спланировать путешествие.
Чтобы посмотреть доступные команды введите /help
''')
    
@router.message(Command("help"))
async def cmd_help(message: types.Message):
    await message.answer('''
/start - приветствие
/help - помощь
/weather - прогноз погоды
''')