import requests as requests
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.categories_keyboard import categories_kb
from keyboards.pagination_keyboard_types import pagination_kb_types
from keyboards.start_keyboard import start_kb

from texts.error_text import get_error_text
from texts.start_text import get_start_text
from texts.places_text import get_place_text

from constants import API_URL

router = Router()


@router.callback_query(F.data == "see_categories")
async def answer_types(callback: CallbackQuery):
    await callback.message.edit_text(
        "🗳Выбери тип места: ",
        reply_markup=categories_kb()
    )


@router.callback_query(F.data.startswith('see_type_'))
async def answer_types_places(callback: CallbackQuery):
    api_url = API_URL + "/places"
    type_filter = callback.data.split('_')[2]
    response = requests.get(api_url + "?type=" + str(type_filter) + "&sort=" + "asc")
    if response.ok:
        first_place = response.json()['data'][0]
        places_count = response.json()['total']
        try:
            first_place_img = first_place['images'][0]['uuid']
        except:
            first_place_img = ''
        answer_text = get_place_text(first_place, first_place_img)
        answer_kb = pagination_kb_types(places_count, 1, type_filter, first_place['id'])
    else:
        answer_text = get_error_text()
        answer_kb = InlineKeyboardMarkup(
            inline_keyboard=[[InlineKeyboardButton(text=f"🗳На главную", callback_data="main")]])
    await callback.message.edit_text(
        text=answer_text,
        parse_mode="HTML",
        reply_markup=answer_kb
    )


@router.callback_query(F.data.startswith('type_page_'))
async def page(callback: CallbackQuery):
    page = int(callback.data.split('_')[2])
    type_filter = callback.data.split('_')[3]
    api_url = API_URL + "/places"
    response = requests.get(api_url + "?type=" + str(type_filter) + "&sort=" + "asc")
    if response.ok:
        next_place = response.json()['data'][page - 1]
        places_count = response.json()['total']
        try:
            next_place_img = next_place['images'][0]['uuid']
        except:
            next_place_img = ''
        answer_text = get_place_text(next_place, next_place_img)
        answer_kb = pagination_kb_types(places_count, page, type_filter, next_place['id'])
    else:
        answer_text = get_error_text()
        answer_kb = InlineKeyboardMarkup(
            inline_keyboard=[[InlineKeyboardButton(text=f"🗳На главную", callback_data="main")]])
    await callback.message.edit_text(
        text=answer_text,
        parse_mode="HTML",
        reply_markup=answer_kb
    )


@router.callback_query(F.data == "main")
async def back_to_main(callback: CallbackQuery):
    await callback.message.edit_text(
        get_start_text(),
        reply_markup=start_kb()
    )
