from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

def pagination_kb_reviews(data_length: int, page: int, place_id: int) -> InlineKeyboardMarkup:
    kb={'inline_keyboard': []}
    buttons=[]
    if page > 1:
        buttons.append({'text':'⬅', 'callback_data':f'see_rev_p_{page-1}_{place_id}'})
    buttons.append({'text':f'{page}/{data_length}', 'callback_data':'none'})
    if page < data_length:
        buttons.append({'text':'➡', 'callback_data':f'see_rev_p_{page+1}_{place_id}'})
    kb['inline_keyboard'].append(buttons)
    kb['inline_keyboard'].append([{'text': 'На главную', 'callback_data':'main'}])
    return kb