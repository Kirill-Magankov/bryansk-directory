from datetime import datetime

import requests as requests
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.utils.markdown import hide_link
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from states.leaving_review import LeaveReview
from keyboards.start_keyboard import start_kb
from keyboards.regions_keyboard import regions_kb
from keyboards.categories_for_regions_keyboard import categories_types_kb
from keyboards.pagination_keyboard_regions_and_types import pagination_kb_regions_types
from keyboards.pagination_keyboard_regions import pagination_kb_regions
from keyboards.pagination_keyboard_reviews import pagination_kb_reviews

router = Router()

@router.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer(
        "Привет!👋 В этом боте ты сможешь посмотреть самые интересные места города Брянска! Выбери, с чего начать:",
        reply_markup=start_kb()
    )

@router.callback_query(F.data == "see_regions")
async def answer_types(callback: CallbackQuery):
    await callback.message.edit_text(
        "Выбери район: ",
        reply_markup=regions_kb()
    )

@router.callback_query(F.data.startswith('see_region_'))
async def answer_types_places(callback: CallbackQuery):
    await callback.message.edit_text(
        "Выбери тип места: ",
        reply_markup=categories_types_kb(callback.data)
    )

@router.callback_query(F.data.startswith('rt_'))
async def answer_types_places(callback: CallbackQuery):
    api_url = "https://bryansk-directory-startup.onrender.com/api/v1/places"
    region_filter = callback.data.split('_')[1]
    type_filter = callback.data.split('_')[2]
    response = requests.get(api_url + "?neighborhood=" + str(region_filter) + "&type=" + str(type_filter) + "&sort=" + "asc")
    if response.ok:
        first_place = response.json()['data'][0]
        places_count = response.json()['total']
        try:
            first_place_img = first_place['images'][0]['uuid']
        except:
            first_place_img = ''
        answer_text =  f"{hide_link('https://bryansk-directory-startup.onrender.com/api/v1/places/images/' + first_place_img) if first_place_img != '' else 'Изображение отсутствует'}"\
                       f"\nНазвание: {first_place['name']}\n"\
                       f"Тип места: {first_place['place_type']['type_name']}\n"\
                       f"Район: {first_place['neighborhood']['name']}\n"\
                       f"Адрес: {first_place['address']}\n"\
                       f"Номер телефона: {first_place['phone_number'] if first_place['phone_number'] != None else 'отсутсвует'}\n"\
                       f"Оценка: {first_place['grade']}\n"\
                       f"Описание: {first_place['description'] if first_place['description'] != None else 'отсутсвует'}"
        reply_kb = pagination_kb_regions_types(places_count, 1, type_filter, region_filter, first_place['id'])
    else:
        answer_text = "Таких мест нет в этом районе :("
        buttons = [
            [InlineKeyboardButton(text=f"Назад", callback_data=f"see_region_{region_filter}")],
            [InlineKeyboardButton(text=f"На главную", callback_data="main")]
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
    api_url = "https://bryansk-directory-startup.onrender.com/api/v1/places"
    page = int(callback.data.split('_')[1])
    region_filter = callback.data.split('_')[2]
    type_filter = callback.data.split('_')[3]
    response = requests.get(api_url + "?neighborhood=" + str(region_filter) + "&type=" + str(type_filter) + "&sort=" + "asc")
    if response.ok:
        next_place = response.json()['data'][page-1]
        places_count = response.json()['total']
        try:
            next_place_img = next_place['images'][0]['uuid']
        except:
            next_place_img = ''
        answer_text = f"{hide_link('https://bryansk-directory-startup.onrender.com/api/v1/places/images/' + next_place_img) if next_place_img != '' else 'Изображение отсутствует'}"\
                      f"\nНазвание: {next_place['name']}\n"\
                      f"Тип места: {next_place['place_type']['type_name']}\n"\
                      f"Район: {next_place['neighborhood']['name']}\n"\
                      f"Адрес: {next_place['address']}\n"\
                      f"Номер телефона: {next_place['phone_number'] if next_place['phone_number'] != None else 'отсутсвует'}\n"\
                      f"Оценка: {next_place['grade']}\n"\
                      f"Описание: {next_place['description'] if next_place['description'] != None else 'отсутсвует'}"
        reply_kb = pagination_kb_regions_types(places_count, page, type_filter, region_filter, next_place['id'])
    else:
        answer_text = "Таких мест нет в этом районе :("
        buttons = [
            [InlineKeyboardButton(text=f"Назад", callback_data=f"see_region_{region_filter}")],
            [InlineKeyboardButton(text=f"На главную", callback_data="main")]
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
    api_url = "https://bryansk-directory-startup.onrender.com/api/v1/places"
    region_filter = callback.data.split('_')[1]
    response = requests.get(api_url + "?neighborhood=" + str(region_filter) + "&sort=" + "asc")
    if response.ok:
        next_place = response.json()['data'][0]
        places_count = response.json()['total']
        try:
            next_place_img = next_place['images'][0]['uuid']
        except:
            next_place_img = ''
        answer_text = f"{hide_link('https://bryansk-directory-startup.onrender.com/api/v1/places/images/' + next_place_img) if next_place_img != '' else 'Изображение отсутствует'}"\
                      f"\nНазвание: {next_place['name']}\n"\
                      f"Тип места: {next_place['place_type']['type_name']}\n"\
                      f"Район: {next_place['neighborhood']['name']}\n"\
                      f"Адрес: {next_place['address']}\n"\
                      f"Номер телефона: {next_place['phone_number'] if next_place['phone_number'] != None else 'отсутсвует'}\n"\
                      f"Оценка: {next_place['grade']}\n"\
                      f"Описание: {next_place['description'] if next_place['description'] != None else 'отсутсвует'}"
        reply_kb = pagination_kb_regions(places_count, 1, region_filter, next_place['id'])
    else:
        answer_text = "Пока мы не нашли интересных мест в этом районе :("
        buttons = [
            [InlineKeyboardButton(text=f"Назад", callback_data=f"see_region_{region_filter}")],
            [InlineKeyboardButton(text=f"На главную", callback_data="main")]
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
    api_url = "https://bryansk-directory-startup.onrender.com/api/v1/places"
    page = int(callback.data.split('_')[1])
    region_filter = callback.data.split('_')[2]
    response = requests.get(api_url + "?neighborhood=" + str(region_filter) + "&sort=" + "asc")
    if response.ok:
        next_place = response.json()['data'][page-1]
        places_count = response.json()['total']
        try:
            next_place_img = next_place['images'][0]['uuid']
        except:
            next_place_img = ''
        answer_text = f"{hide_link('https://bryansk-directory-startup.onrender.com/api/v1/places/images/' + next_place_img) if next_place_img != '' else 'Изображение отсутствует'}"\
                      f"\nНазвание: {next_place['name']}\n"\
                      f"Тип места: {next_place['place_type']['type_name']}\n"\
                      f"Район: {next_place['neighborhood']['name']}\n"\
                      f"Адрес: {next_place['address']}\n"\
                      f"Номер телефона: {next_place['phone_number'] if next_place['phone_number'] != None else 'отсутсвует'}\n"\
                      f"Оценка: {next_place['grade']}\n"\
                      f"Описание: {next_place['description'] if next_place['description'] != None else 'отсутсвует'}"
        reply_kb = pagination_kb_regions(places_count, page, region_filter, next_place['id'])
    else:
        answer_text = "Пока мы не нашли интересных мест в этом районе :("
        buttons = [
            [InlineKeyboardButton(text=f"Назад", callback_data=f"see_region_{region_filter}")],
            [InlineKeyboardButton(text=f"На главную", callback_data="main")]
        ]
        reply_kb = InlineKeyboardMarkup(inline_keyboard=buttons)
    await callback.message.edit_text(
        text=
        answer_text,
        parse_mode="HTML",
        reply_markup=reply_kb
    )
@router.callback_query(F.data == "see_reviews_")
async def answer_all(callback: CallbackQuery):
    place_id = callback.data.split('_')[2]
    api_url = f"https://bryansk-directory-startup.onrender.com/api/v1/places/{place_id}/reviews"
    response = requests.get(api_url)
    if response.ok:
        first_review = response.json()['data'][0]
        reviews_count = response.json()['total']
        answer_text = f"Автор отзыва: {first_review['author_name'] if first_review['author_name'] is not None else 'Аноним'}"\
                      f"Дата отзыва: {first_review['date']}"\
                      f"Ссылка на отзыв: {first_review['url'] if first_review['url'] is not None else 'отзыв оставил пользователь бота'}"\
                      f"Оценка: {first_review['grade']}"\
                      f"Текст отзыва: {first_review['description'] if first_review['description'] is not None else 'отсутствует'}"
        answer_kb = pagination_kb_reviews(reviews_count, 1, place_id)
    else:
        answer_text = "Никто еще не оставил отзыв на это место :("
        answer_kb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text=f"На главную", callback_data="main")]])
    await callback.message.edit_text(text=answer_text,
                        parse_mode="HTML",
                        reply_markup=answer_kb
    )

@router.callback_query(F.data == "see_rev_p_")
async def answer_all(callback: CallbackQuery):
    place_id = callback.data.split('_')[4]
    page = int(callback.data.split('_')[3])
    api_url = f"https://bryansk-directory-startup.onrender.com/api/v1/places/{place_id}/reviews"
    response = requests.get(api_url)
    if response.ok:
        next_review = response.json()['data'][page - 1]
        reviews_count = response.json()['total']
        answer_text = f"Автор отзыва: {next_review['author_name'] if next_review['author_name'] is not None else 'Аноним'}"\
                      f"Дата отзыва: {next_review['date']}"\
                      f"Ссылка на отзыв: {next_review['url'] if next_review['url'] is not None else 'отзыв оставил пользователь бота'}"\
                      f"Оценка: {next_review['grade']}"\
                      f"Текст отзыва: {next_review['description'] if next_review['description'] is not None else 'отсутствует'}"
        answer_kb = pagination_kb_reviews(reviews_count, page, place_id)
    else:
        answer_text = "Никто еще не оставил отзыв на это место :("
        answer_kb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text=f"На главную", callback_data="main")]])
    await callback.message.edit_text(text=answer_text,
                        parse_mode="HTML",
                        reply_markup=answer_kb
    )
@router.callback_query(F.data.startswith('review_'))
async def leave_review(callback: CallbackQuery, state: FSMContext):
    await state.update_data(place_id=callback.data.split('_')[1])
    await callback.message.answer(
        text="Введите своё имя",
        reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(LeaveReview.author_name)

@router.message(LeaveReview.author_name)
async def leave_review(message: Message, state: FSMContext):
    await message.answer(
        text="Введите текст отзыва",
        reply_markup=ReplyKeyboardRemove()
    )
    await state.update_data(author_name=message.text)
    await state.set_state(LeaveReview.description)
@router.message(LeaveReview.description)
async def leave_review(message: Message, state: FSMContext):
    await message.answer(
        text="Введите оценку:",
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
    response = requests.post(f'https://bryansk-directory-startup.onrender.com/api/v1/places/{user_data["place_id"]}/reviews', json=review)
    if response.ok:
        answer_text = "Поздравляю! Ваш отзыв был успешно зарегистрирован"
    else:
        answer_text = "Произошла ошибка, отзыв не был добавлен :("
    await message.answer(
        text=answer_text,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text=f"На главную", callback_data="main")]])
    )
    await state.clear()

@router.callback_query(F.data == "main")
async def back_to_main(callback: CallbackQuery):
    await callback.message.edit_text(
        "Привет!👋 В этом боте ты сможешь посмотреть самые интересные места города Брянска! Выбери, с чего начать:",
        reply_markup=start_kb()
    )