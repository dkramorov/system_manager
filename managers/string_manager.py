# -*- coding: utf-8 -*-
import string


def camel2snake(text: str):
    """Преобразование CamelCase to snake_case
       :param text: текст
    """
    result = ''
    if not text:
        return text
    for i, letter in enumerate(text):
        if i == 0:
            letter = letter.lower()
        if letter in string.ascii_uppercase:
            letter = '_%s' % letter.lower()
        result += letter
    return result