import asyncio
from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from keyboards.edit_keyboard import get_edit_keyboard
from keyboards.accept_keyboard import get_accept_keyboard
from keyboards.cities_keyboard import get_cities_keyboard
from keyboards.interval_keyboard import get_interval_keyboard
import httpx
from service.plotting import create_plot
router = Router()

class WeatherStates(StatesGroup):
    cities = State()
    interval = State()
    accept = State()
    view = State()
    add_city = State()
    

@router.message(Command("weather"))
async def cmd_weather(message: types.Message, state: FSMContext):
    async with httpx.AsyncClient() as client:
        try:
            resp = await client.get('http://api:5000/health')
            if resp.status_code != 200:
                raise Exception('Проблемы с API. Возможно не введен API_KEY')
        except Exception as e:
            await message.answer("Проблемы с подключением к API " + str(e))
            return

    await state.clear()
    await message.answer("Введите города которые вы посетите, включая начальное и конечное. Когда закончите введите СТОП",reply_markup=get_cities_keyboard())
    await state.set_state(WeatherStates.cities)

@router.message(StateFilter(WeatherStates.cities))
async def cmd_cities(message: types.Message, state: FSMContext):
    text = message.text
    if text == 'СТОП':
        data = await state.get_data()
        if not data['cities']:
            await message.answer("Вы ничего не ввели")
            return
        await message.answer("На какой период вы хотите получить прогноз?", reply_markup=get_interval_keyboard())
        await state.set_state(WeatherStates.interval)
        return
    data = await state.get_data()
    data.update(cities=data.get('cities', []) + [text])
    await state.update_data(data)
    await message.answer("Текущие города: " + '\n'.join(data['cities']))

@router.message(StateFilter(WeatherStates.interval))
async def cmd_interval(message: types.Message, state: FSMContext):
    num = message.text
    if num in ['1', '3', '5']:
        data = await state.get_data()
        data.update(interval=num)
        await state.update_data(data)
        await message.answer("Прогноз на " + num + " дней\nГорода: " + '\n'.join(data['cities']))
        await message.answer("Информация верна? ДА/НЕТ", reply_markup=get_accept_keyboard())
        await state.set_state(WeatherStates.accept)
    else:
        await message.answer("Выберите один из предложенных вариантов")
    
@router.message(StateFilter(WeatherStates.accept))
async def cmd_accept(message: types.Message, state: FSMContext):
    text = message.text
    if text == 'ДА':
        data = await state.get_data()
        try:
            for city in data['cities']:
                file = await create_plot(city, data['interval'])
                await message.answer_photo(types.FSInputFile(file, filename='plot.png'), caption=city, reply_markup=types.ReplyKeyboardRemove())
            await message.answer("Хотите что то изменить?", reply_markup=get_edit_keyboard())
            await state.set_state(WeatherStates.view)

        except Exception as e:
            await message.answer("Проблемы с подключением к API " + str(e))
            await state.clear()
            await message.answer("Введите информацию заново /weather", reply_markup=types.ReplyKeyboardRemove())

    elif text == 'НЕТ':
        await state.clear()
        await message.answer("Введите информацию заново /weather", reply_markup=types.ReplyKeyboardRemove())
    else:
        await message.answer("Выберите один из предложенных вариантов")


@router.callback_query(StateFilter(WeatherStates.view))
async def cmd_view(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    data = await state.get_data()
    if callback.data == 'end':
        await state.clear()
        await callback.message.answer('Если хотите посмотреть другие прогнозы введите /weather', reply_markup=types.ReplyKeyboardRemove())
        return
    elif callback.data == 'add_day':
        if data['interval'] == '5':
            await callback.message.answer("Нельзя добавить день, так как прогноз на 5 дней")
            return
        else:
            data['interval'] = str(int(data['interval']) + 1)
    elif callback.data == 'del_day':
        if data['interval'] == '1':
            await callback.message.answer("Нельзя удалить день, так как прогноз на 1 день")
            return
        else:
            data['interval'] = str(int(data['interval']) - 1)
    elif callback.data == 'add_city':
        await callback.message.answer("Введите город который хотите добавить")
        await state.set_state(WeatherStates.add_city)
        return

    # update graphs
    await state.update_data(data)
    for city in data['cities']:
        file = await create_plot(city, data['interval'])
        await callback.message.answer_photo(types.FSInputFile(file, filename='plot.png'), caption=city, reply_markup=types.ReplyKeyboardRemove())
    await callback.message.answer("Хотите что то изменить?", reply_markup=get_edit_keyboard())


@router.message(StateFilter(WeatherStates.add_city))
async def cmd_add_city(message: types.Message, state: FSMContext):
    data = await state.get_data()
    data.update(cities=data.get('cities', []) + [message.text])
    await state.update_data(data)
    for city in data['cities']:
        file = await create_plot(city, data['interval'])
        await message.answer_photo(types.FSInputFile(file, filename='plot.png'), caption=city, reply_markup=types.ReplyKeyboardRemove())
    await message.answer("Хотите что то изменить?", reply_markup=get_edit_keyboard())
