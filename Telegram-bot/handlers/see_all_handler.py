import requests as requests
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters.command import Command

from keyboards.pagination_keyboard import pagination_kb
from keyboards.start_keyboard import start_kb
from handlers import see_regions_handler, see_types_handler, see_reviews_handler, leave_review_handler

from texts.error_text import get_error_text
from texts.places_text import get_place_text
from texts.start_text import get_start_text

from constants import API_URL, API_URL_IMAGES

router = Router()
router.include_routers(see_reviews_handler.router, leave_review_handler.router,
                       see_regions_handler.router, see_types_handler.router)


@router.message(Command("start"))
async def main_menu(message: Message):
    await message.answer(
        get_start_text(),
        reply_markup=start_kb()
    )


@router.callback_query(F.data == "see_all")
async def answer_all(callback: CallbackQuery):
    api_url = API_URL + "/places"
    api_url_img = API_URL_IMAGES + "/places"
    response_img = requests.get(api_url_img)
    response = requests.get(api_url)
    if response.ok:
        first_place = response.json()['data'][0]
        try:
            first_place2 = response_img.json()['data'][0]
            first_place_img = first_place2['images'][0]['uuid']
        except:
            first_place_img = ''
        places_count = response.json()['total']
        answer_text = get_place_text(first_place, first_place_img)
        answer_kb = pagination_kb(places_count, 1, first_place['id'])
    else:
        answer_text = get_error_text()
        answer_kb = InlineKeyboardMarkup(
            inline_keyboard=[[InlineKeyboardButton(text=f"🏠На главную", callback_data="main")]])
    await callback.message.edit_text(text=answer_text,
                                     parse_mode="HTML",
                                     reply_markup=answer_kb
                                     )


@router.callback_query(F.data.startswith('page_'))
async def page(callback: CallbackQuery):
    page = int(callback.data.split("_")[1])
    api_url = API_URL + "/places"
    response = requests.get(api_url)
    api_url_img = API_URL_IMAGES + "/places"
    response_img = requests.get(api_url_img)
    if response.ok:
        next_place = response.json()['data'][page - 1]
        try:
            next_place2 = response_img.json()['data'][page - 1]
            next_place_img = next_place2['images'][0]['uuid']
        except:
            next_place_img = ''
        places_count = response.json()['total']
        answer_text = get_place_text(next_place, next_place_img)
        answer_kb = pagination_kb(places_count, page, next_place['id'])
    else:
        answer_text = get_error_text()
        answer_kb = InlineKeyboardMarkup(
            inline_keyboard=[[InlineKeyboardButton(text=f"🏠На главную", callback_data="main")]])
    await callback.message.edit_text(text=answer_text,
                                     parse_mode="HTML",
                                     reply_markup=answer_kb
                                     )

@router.callback_query(F.data == "main")
async def back_to_main(callback: CallbackQuery):
    await callback.message.edit_text(
        get_start_text(),
        reply_markup=start_kb()
    )