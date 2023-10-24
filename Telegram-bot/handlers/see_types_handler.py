import requests as requests
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.utils.markdown import hide_link

from constants import API_URL
from keyboards.start_keyboard import start_kb
from keyboards.categories_keyboard import categories_kb
from keyboards.pagination_keyboard_types import pagination_kb_types

router = Router()


@router.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer(
        "Привет!👋 В этом боте ты сможешь посмотреть самые интересные места города Брянска! Выбери, с чего начать:",
        reply_markup=start_kb()
    )


@router.callback_query(F.data == "see_categories")
async def answer_types(callback: CallbackQuery):
    await callback.message.edit_text(
        "Выбери тип места: ",
        reply_markup=categories_kb()
    )


@router.callback_query(F.data.startswith('see_type_'))
async def answer_types_places(callback: CallbackQuery):
    api_url = API_URL + "/places"
    type_filter = callback.data.split('_')[2]
    response = requests.get(api_url + "?type=" + str(type_filter) + "&sort=" + "asc")
    first_place = response.json()['data'][0]
    places_count = response.json()['total']
    try:
        first_place_img = first_place['images'][0]['uuid']
    except:
        first_place_img = ''
    await callback.message.edit_text(
        text=
        f"{hide_link(API_URL + '/places/images/' + first_place_img) if first_place_img != '' else 'Изображение отсутствует'}"
        f"\nНазвание: {first_place['name']}\n"
        f"Тип места: {first_place['place_type']['type_name']}\n"
        f"Район: {first_place['neighborhood']['name']}\n"
        f"Адрес: {first_place['address']}\n"
        f"Номер телефона: {first_place['phone_number'] if first_place['phone_number'] != None else 'отсутсвует'}\n"
        f"Оценка: {first_place['grade']}\n"
        f"Описание: {first_place['description'] if first_place['description'] != None else 'отсутсвует'}",
        parse_mode="HTML",
        reply_markup=pagination_kb_types(places_count, 1, type_filter)
    )


@router.callback_query(F.data.startswith('type_page_'))
async def page(callback: CallbackQuery):
    page = int(callback.data.split('_')[2])
    type_filter = callback.data.split('_')[3]
    api_url = API_URL + "/places"
    response = requests.get(api_url + "?type=" + str(type_filter) + "&sort=" + "asc")
    next_place = response.json()['data'][page - 1]
    places_count = response.json()['total']
    try:
        next_place_img = next_place['images'][0]['uuid']
    except:
        next_place_img = ''
    await callback.message.edit_text(
        text=
        f"{hide_link(API_URL + '/places/images/' + next_place_img) if next_place_img != '' else 'Изображение отсутствует'}"
        f"\nНазвание: {next_place['name']}\n"
        f"Тип места: {next_place['place_type']['type_name']}\n"
        f"Район: {next_place['neighborhood']['name']}\n"
        f"Адрес: {next_place['address']}\n"
        f"Номер телефона: {next_place['phone_number'] if next_place['phone_number'] != None else 'отсутсвует'}\n"
        f"Оценка: {next_place['grade']}\n"
        f"Описание: {next_place['description'] if next_place['description'] != None else 'отсутсвует'}",
        parse_mode="HTML",
        reply_markup=pagination_kb_types(places_count, page, type_filter)
    )


@router.callback_query(F.data == "main")
async def back_to_main(callback: CallbackQuery):
    await callback.message.edit_text(
        "Привет!👋 В этом боте ты сможешь посмотреть самые интересные места города Брянска! Выбери, с чего начать:",
        reply_markup=start_kb()
    )
