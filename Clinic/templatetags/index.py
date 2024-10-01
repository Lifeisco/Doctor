# your_app/templatetags/custom_tags.py
from django import template

register = template.Library()


@register.filter
def custom_index(list, index):
    #  Возвращает элемент списка по индексу.
    try:
        return list[int(index)]
    except (IndexError, ValueError):
        return ''  # Возвращаем пустую строку или любое другое значение по умолчанию
