import re
import requests as requests
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from states.leaving_feedback import LeaveFeedback

from keyboards.start_keyboard import start_kb

from texts.start_text import get_start_text

from constants import API_URL

router = Router()


@router.callback_query(F.data == 'feedback')
async def leave_feedback(callback: CallbackQuery, state: FSMContext):
    await state.update_data(user_id=callback.from_user.id,
                            chat_id=callback.message.chat.id,
                            username=callback.from_user.username)
    await callback.message.answer(
        text="📧Введите свой email",
        reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(LeaveFeedback.email)


@router.message(LeaveFeedback.email)
async def leave_feedback(message: Message, state: FSMContext):
    await message.answer(
        text="✍Введите текст предложения/жалобы",
        reply_markup=ReplyKeyboardRemove()
    )
    await state.update_data(email=message.text)
    await state.set_state(LeaveFeedback.comment)


@router.message(LeaveFeedback.comment)
async def leave_feedback(message: Message, state: FSMContext):
    await state.update_data(comment=message.text)
    user_data = await state.get_data()
    pattern = re.compile(r'[\w.-]+@[\w-]+\.(com|ru)')
    if pattern.match(user_data['email']):
        feedback = {'tg_username': user_data['username'], 'tg_user_id': str(user_data['user_id']),
                    'tg_chat_id': str(user_data['chat_id']), 'email': user_data['email'], 'message': user_data['comment']}
        response = requests.post(API_URL + "/feedbacks", json=feedback)
        if response.ok:
            answer_text = "✅Поздравляю! Ваше обращение было успешно зарегистрировано"
        else:
            answer_text = "⚠️Произошла ошибка, обращение не было отправлено :("
    else:
        answer_text = "⚠️Ошибка при указании электронной почты"
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
