from django import template
import re

register = template.Library()


@register.filter(name='censor')
def censor(value):
    if not isinstance(value, str):
        raise ValueError("Input must be a string")

    # Список нежелательных слов для цензурирования
    unwanted_words = ['пизда', 'хуй', 'пидор']

    # Заменяем буквы нежелательных слов на '*'
    for word in unwanted_words:
        # Используем функцию замены с поддержкой групп, чтобы оставить первую букву в слове
        value = re.sub(fr'(\b\w){word[1:]}\b', r'\1' + '*' * (len(word) - 1), value, flags=re.IGNORECASE)

    return value
