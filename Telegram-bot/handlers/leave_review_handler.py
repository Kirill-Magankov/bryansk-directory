from datetime import datetime

import requests as requests
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from states.leaving_review import LeaveReview

from keyboards.start_keyboard import start_kb

from texts.start_text import get_start_text

from constants import API_URL

router = Router()


@router.callback_query(F.data.startswith('review_'))
async def leave_review(callback: CallbackQuery, state: FSMContext):
    await state.update_data(place_id=callback.data.split('_')[1])
    await callback.message.answer(
        text="✍Введите своё имя",
        reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(LeaveReview.author_name)


@router.message(LeaveReview.author_name)
async def leave_review(message: Message, state: FSMContext):
    await message.answer(
        text="✍Введите текст отзыва",
        reply_markup=ReplyKeyboardRemove()
    )
    await state.update_data(author_name=message.text)
    await state.set_state(LeaveReview.description)


@router.message(LeaveReview.description)
async def leave_review(message: Message, state: FSMContext):
    await message.answer(
        text="✍Введите оценку:",
        reply_markup=ReplyKeyboardRemove()
    )
    await state.update_data(description=message.text)
    await state.set_state(LeaveReview.grade)


@router.message(LeaveReview.grade)
async def leave_review(message: Message, state: FSMContext):
    await state.update_data(grade=message.text)
    user_data = await state.get_data()
    review = {'date': datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f"), 'author_name': user_data['author_name'],
              'description': user_data['description'], 'url': None, 'grade': int(user_data['grade'])}
    response = requests.post(API_URL + f'/places/{user_data["place_id"]}/reviews', json=review)
    if response.ok:
        answer_text = "✅Поздравляю! Ваш отзыв был успешно зарегистрирован"
    else:
        answer_text = "⚠️Произошла ошибка, отзыв не был добавлен :("
    await message.answer(
        text=answer_text,
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[[InlineKeyboardButton(text=f"На главную", callback_data="main")]])
    )
    await state.clear()


@router.callback_query(F.data == "main")
async def back_to_main(callback: CallbackQuery):
    await callback.message.edit_text(
        get_start_text(),
        reply_markup=start_kb()
    )
