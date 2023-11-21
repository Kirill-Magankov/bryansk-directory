import requests as requests
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.regions_keyboard import regions_kb
from keyboards.categories_for_regions_keyboard import categories_types_kb
from keyboards.pagination_keyboard_regions_and_types import pagination_kb_regions_types
from keyboards.pagination_keyboard_regions import pagination_kb_regions
from keyboards.start_keyboard import start_kb

from texts.places_text import get_place_text
from texts.start_text import get_start_text

from constants import API_URL, API_URL_IMAGES

router = Router()


@router.callback_query(F.data == "see_regions")
async def answer_types(callback: CallbackQuery):
    await callback.message.edit_text(
        "🗳Выбери район: ",
        reply_markup=regions_kb()
    )


@router.callback_query(F.data.startswith('see_region_'))
async def answer_types_places(callback: CallbackQuery):
    await callback.message.edit_text(
        "🗳Выбери тип места: ",
        reply_markup=categories_types_kb(callback.data)
    )


@router.callback_query(F.data.startswith('rt_'))
async def answer_types_places(callback: CallbackQuery):
    api_url = API_URL + "/places"
    region_filter = callback.data.split('_')[1]
    type_filter = callback.data.split('_')[2]
    response = requests.get(
        api_url + "?neighborhood=" + str(region_filter) + "&type=" + str(type_filter) + "&sort=" + "asc")
    api_url_img = API_URL_IMAGES + "/places"
    response_img = requests.get(
        api_url_img + "?neighborhood=" + str(region_filter) + "&type=" + str(type_filter) + "&sort=" + "asc")
    if response.ok:
        first_place = response.json()['data'][0]
        places_count = response.json()['total']
        try:
            first_place2 = response_img.json()['data'][0]
            first_place_img = first_place2['images'][0]['url']
        except:
            first_place_img = ''
        answer_text = get_place_text(first_place, first_place_img)
        reply_kb = pagination_kb_regions_types(places_count, 1, type_filter, region_filter, first_place['id'])
    else:
        answer_text = "❓Таких мест нет в этом районе :("
        buttons = [
            [InlineKeyboardButton(text=f"↩Назад", callback_data=f"see_region_{region_filter}")],
            [InlineKeyboardButton(text=f"🏠На главную", callback_data="main")]
        ]
        reply_kb = InlineKeyboardMarkup(inline_keyboard=buttons)
    await callback.message.edit_text(
        text=
        answer_text,
        parse_mode="HTML",
        reply_markup=reply_kb
    )


@router.callback_query(F.data.startswith('rtp_'))
async def answer_types_places(callback: CallbackQuery):
    api_url = API_URL + "/places"
    page = int(callback.data.split('_')[1])
    region_filter = callback.data.split('_')[2]
    type_filter = callback.data.split('_')[3]
    response = requests.get(
        api_url + "?neighborhood=" + str(region_filter) + "&type=" + str(type_filter) + "&sort=" + "asc")
    api_url_img = API_URL_IMAGES + "/places"
    response_img = requests.get(
        api_url_img + "?neighborhood=" + str(region_filter) + "&type=" + str(type_filter) + "&sort=" + "asc")
    if response.ok:
        next_place = response.json()['data'][page - 1]
        places_count = response.json()['total']
        try:
            next_place2 = response_img.json()['data'][page - 1]
            next_place_img = next_place2['images'][0]['uuid']
        except:
            next_place_img = ''
        answer_text = get_place_text(next_place, next_place_img)
        reply_kb = pagination_kb_regions_types(places_count, page, type_filter, region_filter, next_place['id'])
    else:
        answer_text = "❓Таких мест нет в этом районе :("
        buttons = [
            [InlineKeyboardButton(text=f"↩Назад", callback_data=f"see_region_{region_filter}")],
            [InlineKeyboardButton(text=f"🏠На главную", callback_data="main")]
        ]
        reply_kb = InlineKeyboardMarkup(inline_keyboard=buttons)
    await callback.message.edit_text(
        text=
        answer_text,
        parse_mode="HTML",
        reply_markup=reply_kb
    )


@router.callback_query(F.data.startswith('rta_'))
async def answer_types_places(callback: CallbackQuery):
    api_url = API_URL + "/places"
    region_filter = callback.data.split('_')[1]
    response = requests.get(api_url + "?neighborhood=" + str(region_filter) + "&sort=" + "asc")
    api_url_img = API_URL_IMAGES + "/places"
    response_img = requests.get(
        api_url_img + "?neighborhood=" + str(region_filter) + "&sort=" + "asc")
    if response.ok:
        first_place = response.json()['data'][0]
        places_count = response.json()['total']
        try:
            first_place2 = response_img.json()['data'][0]
            first_place_img = first_place2['images'][0]['url']
        except:
            first_place_img = ''
        answer_text = get_place_text(first_place, first_place_img)
        reply_kb = pagination_kb_regions(places_count, 1, region_filter, first_place['id'])
    else:
        answer_text = "❓Пока мы не нашли интересных мест в этом районе :("
        buttons = [
            [InlineKeyboardButton(text=f"↩Назад", callback_data=f"see_region_{region_filter}")],
            [InlineKeyboardButton(text=f"🏠На главную", callback_data="main")]
        ]
        reply_kb = InlineKeyboardMarkup(inline_keyboard=buttons)
    await callback.message.edit_text(
        text=
        answer_text,
        parse_mode="HTML",
        reply_markup=reply_kb
    )


@router.callback_query(F.data.startswith('rtap_'))
async def answer_types_places(callback: CallbackQuery):
    api_url = API_URL + "/places"
    page = int(callback.data.split('_')[1])
    region_filter = callback.data.split('_')[2]
    response = requests.get(api_url + "?neighborhood=" + str(region_filter) + "&sort=" + "asc")
    api_url_img = API_URL_IMAGES + "/places"
    response_img = requests.get(api_url_img + "?neighborhood=" + str(region_filter) + "&sort=" + "asc")
    if response.ok:
        next_place = response.json()['data'][page - 1]
        places_count = response.json()['total']
        try:
            next_place2 = response_img.json()['data'][page - 1]
            next_place_img = next_place2['images'][0]['uuid']
        except:
            next_place_img = ''
        answer_text = get_place_text(next_place, next_place_img)
        reply_kb = pagination_kb_regions(places_count, page, region_filter, next_place['id'])
    else:
        answer_text = "❓Пока мы не нашли интересных мест в этом районе :("
        buttons = [
            [InlineKeyboardButton(text=f"↩Назад", callback_data=f"see_region_{region_filter}")],
            [InlineKeyboardButton(text=f"🏠На главную", callback_data="main")]
        ]
        reply_kb = InlineKeyboardMarkup(inline_keyboard=buttons)
    await callback.message.edit_text(
        text=
        answer_text,
        parse_mode="HTML",
        reply_markup=reply_kb
    )


@router.callback_query(F.data == "main")
async def back_to_main(callback: CallbackQuery):
    await callback.message.edit_text(
        get_start_text(),
        reply_markup=start_kb()
    )
