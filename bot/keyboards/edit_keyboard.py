from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import types

def get_edit_keyboard() -> types.InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        types.InlineKeyboardButton(text='+1 день', callback_data='add_day'),
        types.InlineKeyboardButton(text='-1 день', callback_data='del_day'),
    )
    builder.row(
        types.InlineKeyboardButton(text='Добавить город', callback_data='add_city'),
        types.InlineKeyboardButton(text='Закончить', callback_data='end'),
    )
    return builder.as_markup()