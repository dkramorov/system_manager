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


def domain2punycode(domain: str) -> str:
    """Преобразуем домен к punycode
       обратно 'xn--p1ai'.encode('idna').decode('idna') = 'ру'
       :param domain: Домен
       :return: домен строкой в punycode
    """
    if not domain:
        return ''
    if '://' in domain:
        domain = domain.split('://')[1]
    if '?' in domain:
        domain = domain.split("?")[0]
    if '/' in domain:
        domain = domain.split('/')[0]
    if '#' in domain:
        domain = domain.split('#')[0]
    domain = domain.encode('idna')
    return domain.decode('utf-8')


def translit(text: str):
    """Транслит текста с русского в латиницу
       :param text: текст для транслита
    """
    if not text:
        return ''
    alphabet = string.ascii_lowercase
    rus = ('абвгдеёжзийклмнопрстуфхцчшщъыьэюя №')
    eng = ('a', 'b', 'v', 'g', 'd', 'e', 'yo', 'j', 'z', 'i', 'y', 'k', 'l', 'm', 'n', 'o', 'p', 'r', 's', 't', 'u', 'f', 'h', 'c', 'ch', 'sh', 'shh', '', 'y', '', 'e', 'yu', 'ya', '-', '-')
    chars = ('-0123456789_%s' % (alphabet, ))
    result = ''
    for item in text:
        letter = ''
        item = item.lower()
        if item in rus:
            ind = rus.index(item)
            letter = eng[ind]
        else:
            if item in chars:
                letter = item
        result += letter
    return result


def digit_to_str(digit):
    """Число записываем прописью
       :param digit: число, которое будем писать текстом
    """
    result = ''
    measure = ('', '', 'миллион', 'миллиард', 'триллион',
               'квадриллион', 'квинтиллион', 'секстиллион',
               'септиллион', 'октиллион', 'нониллион', 'дециллион')
    measure_len = len(measure)
    if not type(digit) == int:
        try:
            digit = float(digit)
        except ValueError:
            digit = 0
    try:
        digit = int(digit)
    except ValueError:
        digit = 0
    digit_str = str(digit)

    summa = summa_format(digit)
    if ' ' in summa:
        digits = summa.split(' ')
    else:
        digits = [summa, ]
    digits.reverse()
    # Каждый триптих обрабатываем, добавляя пояснение (тысячи, милионы)
    z = 0
    for item in digits:
        woman = False
        voca = None
        triptix = item
        if z == 1: # тысячу передаем в женском роде
            woman = True
            voca = ('тысяча', 'тысяч', 'тысячи')
        else:
            if z > 1 and z < (measure_len -1):
                inf = measure[z]
                voca = (inf, inf + 'ов', inf + 'а')
        cur_digit =  analyze_triptix(triptix, woman)
        cur_name =  analyze_digit(triptix, voca)
        if result:
            result = ' ' + result
        cur_result = cur_digit
        if cur_name:
            cur_result += ' ' + cur_name
        result = cur_result + result
        z += 1
    return result


def analyze_triptix(digit, woman=False):
    """Передаем число (максимум трехзначное), пишем его прописью
       woman = False по умолчанию - мужской род, например, "один" (м.б одна)
       :param digit: число
       :param woman: если женский род
    """
    result = ''
    hundred = dozen = unit = None
    hundred_str = dozen_str = unit_str = ''

    units = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9)
    units_str = ('', 'один', 'два', 'три', 'четыре', 'пять',
                 'шесть', 'семь', 'восемь', 'девять')
    units_str_woman = ('', 'одна', 'две', 'три', 'четыре', 'пять',
                       'шесть', 'семь', 'восемь', 'девять')

    dozens_ten = (10, 11, 12, 13, 14, 15, 16, 17, 18, 19)
    dozens_ten_str =  ('десять', 'одиннадцать', 'двенадцать', 'тринадцать',
                       'четырнадцать', 'пятнадцать', 'шестнадцать',
                       'семнадцать', 'восемнадцать', 'девятнадцать')
    dozens_str = ('', '', 'двадцать', 'тридцать', 'сорок', 'пятьдесят',
                  'шестьдесят', 'семьдесят', 'восемьдесят', 'девяносто')

    hundreds_str = ('', 'сто', 'двести', 'триста', 'четыреста', 'пятьсот',
                    'шестьсот', 'семьсот', 'восемьсот', 'девятьсот')

    digit_str = str(digit)
    digit_len = len(digit_str)
    # Записываем unit
    unit = int(digit_str[-1])

    # Записываем dozen & hundred
    if digit_len == 2: # Два разряда
        dozen = int(digit_str[0])
    if digit_len == 3: # Три разряда
        hundred = int(digit_str[0])
        dozen = int(digit_str[1])
    # Если это 10-19
    if dozen == 1:
        # Создаем новый dozen - dozen_ten
        dozen_ten = int("%s%s" % (dozen, unit))
        if dozen_ten in dozens_ten:
            dozen_str = dozens_ten_str[dozens_ten.index(dozen_ten)]
    # Если это 20-99
    else:
        if dozen in units:
            dozen_str = dozens_str[units.index(dozen)]

    if unit in units and not dozen == 1:
        if woman:
            unit_str = units_str_woman[units.index(unit)]
        else:
            unit_str = units_str[units.index(unit)]

    if hundred:
        if hundred in units:
            hundred_str = hundreds_str[units.index(hundred)]

    # Пишем результат
    for item in (hundred_str, dozen_str, unit_str):
        if result and not result.endswith(' '):
            result += ' '
        result += item
    return result.strip()


def analyze_digit(digit, end: tuple = ('тысяча', 'тысяч', 'тысячи')):
    """Пишет прописью  с нужным окончанием слово (день, год, месяц)
       digit = цифра, от которой зависит окончание
       end = варианты окончаний:
       1 миллион, 10 миллионов, 2 миллиона
       (u"год", u"лет", u"года")
       (u"месяц", u"месяцев", u"месяца")
       (u"день", u"дней", u"дня")"""
    result = ''
    try:
        digit = int(digit)
    except ValueError:
        return result
    if not end:
        return result
    digit_str = str(digit)
    digit_str = int(digit_str[-1])
    # На окончания влияет 2 последних символа
    if digit_str == 0 or digit_str >=5:
        result = end[1] # тысяч
    if digit_str == 1:
        result = end[0] # тысяча
    if digit_str > 1 and digit_str < 5:
        result = end[2] # тысячи
    if digit > 9:
        digit_str2 = int(str(digit)[-2])
        if digit_str2 == 1:
            result = end[1] # тысяч
    return result


def summa_format(summa):
    """Деньга с пробелами через 3 знака с конца
       :param summa: число, которое будем разбивать
    """
    if not summa:
        if summa == 0:
            return '0'
        return summa
    summa_str = str(summa)
    if ',' in summa_str:
        summa_str = summa_str.replace(',', '.')
    rub, kop = summa_str, 0
    if '.' in summa_str:
        rub, kop = summa_str.split('.')
    summa_tmp = ''
    summa_len = len(rub)
    zero_kop = kop
    try:
        kop = int(kop)
    except ValueError:
        kop = 0

    if summa_len <= 3:
        if kop > 0:
            return summa_str
        return rub
    else:
        for i in range(summa_len):
            if i > 0 and i % 3 == 0:
                summa_tmp = ' ' + summa_tmp
            summa_tmp = rub[summa_len-i-1] + summa_tmp
        summa = summa_tmp

    if kop > 0:
        summa = '%s.%s' % (summa, zero_kop)
    return summa
