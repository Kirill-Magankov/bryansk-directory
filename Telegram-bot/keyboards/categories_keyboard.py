from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

def start_kb():
    buttons = [
        [InlineKeyboardButton(text="Просмотреть все места", callback_data="see_all")],
        [InlineKeyboardButton(text="Просмотреть места по категориям", callback_data="see_categories")],
        [InlineKeyboardButton(text="Просмотреть места по районам", callback_data="see_regions")]
    ]
    kb = InlineKeyboardMarkup(inline_keyboard=buttons)
    return kb