def get_review_text(review):
    return f"👤Автор отзыва: {review['author_name'] if review['author_name'] is not None else 'Аноним'}" \
                          f"📆Дата отзыва: {review['date']}" \
                          f"🔗Ссылка на отзыв: {review['url'] if review['url'] is not None else 'отзыв оставил пользователь бота'}" \
                          f"🌟Оценка: {review['grade']}" \
                          f"📝Текст отзыва: {review['description'] if review['description'] is not None else 'отсутствует'}"