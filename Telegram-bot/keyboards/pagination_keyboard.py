from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def pagination_kb(data_length: int, page: int, place_id: str) -> InlineKeyboardMarkup:
    kb = {'inline_keyboard': []}
    buttons = []
    if page > 1:
        buttons.append({'text': '⬅', 'callback_data': f'page_{page - 1}'})
    buttons.append({'text': f'{page}/{data_length}', 'callback_data': 'none'})
    if page < data_length:
        buttons.append({'text': '➡', 'callback_data': f'page_{page + 1}'})
    kb['inline_keyboard'].append(buttons)
    kb['inline_keyboard'].append([{'text': '🔎Просмотреть отзывы', 'callback_data': f'see_reviews_{place_id}'}])
    kb['inline_keyboard'].append([{'text': '🌟Оставить отзыв', 'callback_data': f'review_{place_id}'}])
    kb['inline_keyboard'].append([{'text': '🗳На главную', 'callback_data': 'main'}])
    return kb
