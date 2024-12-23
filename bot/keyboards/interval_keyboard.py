from aiogram import types


def get_interval_keyboard() -> types.ReplyKeyboardMarkup:
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=[[
        types.KeyboardButton(text='1'),
        types.KeyboardButton(text='3'),
        types.KeyboardButton(text='5')
        ]],
        resize_keyboard=True
        )
    return keyboard