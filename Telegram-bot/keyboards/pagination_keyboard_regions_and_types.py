from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

def pagination_kb_regions_types(data_length: int, page: int, type: str, region: str) -> InlineKeyboardMarkup:
    kb={'inline_keyboard': []}
    buttons=[]
    if page > 1:
        buttons.append({'text':'⬅', 'callback_data':f'rtp_{page-1}_{region}_{type}'})
    buttons.append({'text':f'{page}/{data_length}', 'callback_data':'none'})
    if page < data_length:
        buttons.append({'text':'➡', 'callback_data':f'rtp_{page+1}_{region}_{type}'})
    kb['inline_keyboard'].append(buttons)
    kb['inline_keyboard'].append([{'text': 'Назад', 'callback_data': f"see_region_{region}"}])
    kb['inline_keyboard'].append([{'text': 'На главную', 'callback_data':'main'}])
    return kb