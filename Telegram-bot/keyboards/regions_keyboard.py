import requests as requests
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

def regions_kb():
    buttons = []
    api_url = "https://bryansk-directory-startup.onrender.com/api/v1/places/neighborhood"
    response = requests.get(api_url)
    places_regions = response.json()['data']
    for item in places_regions:
        buttons.append(
            [InlineKeyboardButton(text=f"{item['name']}", callback_data=f"see_region_{item['name']}")])
    buttons.append([InlineKeyboardButton(text="На главную", callback_data="main")])
    kb = InlineKeyboardMarkup(inline_keyboard=buttons)
    return kb