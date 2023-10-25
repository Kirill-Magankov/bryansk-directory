from aiogram.utils.markdown import hide_link
from constants import API_URL_IMAGES


def get_place_text(place, place_image):
    return f"{hide_link(API_URL_IMAGES + '/places/images/' + place_image) if place_image != '' else '🖼Изображение отсутствует'}" \
           f"\n🔖Название: {place['name']}\n" \
           f"📋Тип места: {place['place_type']['type_name']}\n" \
           f"🏙Район: {place['neighborhood']['name']}\n" \
           f"📭Адрес: {place['address']}\n" \
           f"📞Номер телефона: {place['phone_number'] if place['phone_number'] is not None else 'отсутствует'}\n" \
           f"🌟Оценка: {place['grade']}\n" \
           f"📝Описание: {place['description'] if place['description'] is not None else 'отсутствует'}"
