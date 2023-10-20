import requests as requests
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery

from keyboards.start_keyboard import start_kb
from keyboards.pagination_keyboard import pagination_kb

router = Router()

@router.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer(
        "Привет!👋 В этом боте ты сможешь посмотреть самые интересные места города Брянска! Выбери, с чего начать:",
        reply_markup=start_kb()
    )

@router.callback_query(F.data == "see_all")
async def answer_all(callback: CallbackQuery):
    api_url = "http://localhost:8000/api/v1/places"
    response = requests.get(api_url)
    first_place = response.json()['data'][0]
    places_count = response.json()['total']
    await callback.message.edit_text(text=
        f"Название: {first_place['name']}\n"
        f"Тип места: {first_place['place_type']['type_name']}\n"
        f"Район: {first_place['neighborhood']['name']}\n"
        f"Адрес: {first_place['address']}\n"
        f"Номер телефона: {first_place['phone_number']}\n"
        f"Оценка: {first_place['grade']}\n"
        f"Описание: {first_place['description']}",
                          reply_markup=pagination_kb(places_count, 1),
                          parse_mode="HTML"
    )

@router.callback_query(F.data.startswith('page_'))
async def page(callback: CallbackQuery):
    page = int(callback.data.split('_')[1])
    api_url = "http://localhost:8000/api/v1/places"
    response = requests.get(api_url)
    next_place = response.json()['data'][page-1]
    places_count = response.json()['total']
    kb = pagination_kb(places_count, page)
    await callback.message.edit_text(
        text=
        f"Название: {next_place['name']}\n"
        f"Тип места: {next_place['place_type']['type_name']}\n"
        f"Район: {next_place['neighborhood']['name']}\n"
        f"Адрес: {next_place['address']}\n"
        f"Номер телефона: {next_place['phone_number']}\n"
        f"Оценка: {next_place['grade']}\n"
        f"Описание: {next_place['description']}",
        reply_markup=pagination_kb(places_count, page),
        parse_mode="HTML"
    )
@router.callback_query(F.data == "main")
async def back_to_main(callback: CallbackQuery):
    await callback.message.edit_text(
        "Привет!👋 В этом боте ты сможешь посмотреть самые интересные места города Брянска! Выбери, с чего начать:",
        reply_markup=start_kb()
    )
