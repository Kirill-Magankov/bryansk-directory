from aiogram.utils.markdown import hide_link

def get_place_text(place, place_image):
    return f"{hide_link('https://bryansk-directory-startup.onrender.com/api/v1/places/images/' + place_image) if place_image != '' else '🖼Изображение отсутствует'}" \
                      f"\n🔖Название: {place['name']}\n" \
                      f"📋Тип места: {place['place_type']['type_name']}\n" \
                      f"🏙Район: {place['neighborhood']['name']}\n" \
                      f"📭Адрес: {place['address']}\n" \
                      f"📞Номер телефона: {place['phone_number'] if place['phone_number'] != None else 'отсутсвует'}\n" \
                      f"🌟Оценка: {place['grade']}\n" \
                      f"📝Описание: {place['description'] if place['description'] != None else 'отсутсвует'}"