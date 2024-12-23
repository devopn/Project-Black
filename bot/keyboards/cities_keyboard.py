from aiogram import types


def get_cities_keyboard() -> types.ReplyKeyboardMarkup:
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=[[
            types.KeyboardButton(text='СТОП'),
        ]],
        resize_keyboard=True
    )
    return keyboard