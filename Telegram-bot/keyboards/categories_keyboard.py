import requests as requests
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from constants import API_URL


def categories_kb():
    buttons = []
    api_url = API_URL + "/places/types"
    response = requests.get(api_url)
    places_types = response.json()['data']
    for item in places_types:
        buttons.append([InlineKeyboardButton(text=f"{item['type_name']}", callback_data=f"see_type_{item['type_name']}")])
    buttons.append([InlineKeyboardButton(text="На главную", callback_data="main")])
    kb = InlineKeyboardMarkup(inline_keyboard=buttons)
    return kb