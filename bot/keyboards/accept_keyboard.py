from aiogram import types


def get_accept_keyboard() -> types.ReplyKeyboardMarkup:
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=[[
            types.KeyboardButton(text='ДА'),
            types.KeyboardButton(text='НЕТ')
        ]],
        resize_keyboard=True
    )
    return keyboard