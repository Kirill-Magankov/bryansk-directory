import requests as requests
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.pagination_keyboard_reviews import pagination_kb_reviews
from keyboards.start_keyboard import start_kb

from texts.start_text import get_start_text
from texts.reviews_text import get_review_text
from texts.error_text import get_error_text

from constants import API_URL

router = Router()


@router.callback_query(F.data.startswith('see_reviews_'))
async def see_reviews(callback: CallbackQuery):
    place_id = callback.data.split('_')[2]
    api_url = API_URL + f"/places/{place_id}/reviews"
    response = requests.get(api_url)
    if response.ok:
        try:
            first_review = response.json()['data'][0]
            reviews_count = len(response.json()['data'])
            answer_text = get_review_text(first_review)
            answer_kb = pagination_kb_reviews(reviews_count, 1, place_id)
        except:
            answer_text = "❓Никто еще не оставил отзыв на это место :("
            answer_kb = InlineKeyboardMarkup(
                inline_keyboard=[[InlineKeyboardButton(text=f"🏠На главную", callback_data="main")]])
    else:
        answer_text = get_error_text()
        answer_kb = InlineKeyboardMarkup(
            inline_keyboard=[[InlineKeyboardButton(text=f"🏠На главную", callback_data="main")]])
    await callback.message.edit_text(text=answer_text,
                                     parse_mode="HTML",
                                     reply_markup=answer_kb
                                     )


@router.callback_query(F.data.startswith("see_rev_p_"))
async def see_reviews_next(callback: CallbackQuery):
    place_id = callback.data.split('_')[4]
    page = int(callback.data.split('_')[3])
    api_url = API_URL + f"/places/{place_id}/reviews"
    response = requests.get(api_url)
    if response.ok:
        next_review = response.json()['data'][page - 1]
        reviews_count = len(response.json()['data'])
        answer_text = get_review_text(next_review)
        answer_kb = pagination_kb_reviews(reviews_count, page, place_id)
    else:
        answer_text = "❓Никто еще не оставил отзыв на это место :("
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
