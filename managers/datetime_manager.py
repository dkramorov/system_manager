# -*- coding:utf-8 -*-
import calendar
import datetime
import logging
import re
import time


logger = logging.getLogger()


regas_date = (
    (re.compile('^([0-9]{1,2}-[0-9]{1,2}-[0-9]{4}) ([0-9]{1,2}:[0-9]{1,2}:[0-9]{1,2})$'), '%d-%m-%Y %H:%M:%S'),
    (re.compile('^([0-9]{4}-[0-9]{1,2}-[0-9]{1,2}) ([0-9]{1,2}:[0-9]{1,2}:[0-9]{1,2})$'), '%Y-%m-%d %H:%M:%S'),
    (re.compile('^([0-9]{4}-[0-9]{1,2}-[0-9]{1,2}) ([0-9]{1,2}:[0-9]{1,2})$'), '%Y-%m-%d %H:%M'),
    (re.compile('^([0-9]{1,2}-[0-9]{1,2}-[0-9]{4}) ([0-9]{1,2}:[0-9]{1,2})$'), '%d-%m-%Y %H:%M'),
    (re.compile('^([0-9]{4}-[0-9]{1,2}-[0-9]{1,2})$'), '%Y-%m-%d'),
    (re.compile('^([0-9]{1,2}-[0-9]{1,2}-[0-9]{4})$'), '%d-%m-%Y'),
    #(re.compile('^([0-9]{1,2}/[0-9]{1,2}/[0-9]{4}) ([0-9]{1,2}:[0-9]{1,2}:[0-9]{1,2}) UTC$'), '%Y-%m-%d %H:%M:%S')
)


def calc_elapsed_time(func):
    """@DECORATOR
       Замер длительности выполнения функции
       Используем функцию как декоратор
    """
    def wrapper(*args, **kwargs):
        started = time.time()
        result = func(*args, **kwargs)
        elapsed = time.time() - started
        logger.info('[ELAPSED]: func:%s %.2f (%.1f min)' % (func.__name__, elapsed, elapsed/60))
        return result
    return wrapper


def create_utc_datetime(date: datetime.datetime):
    """Создает offset-naive из offset-awaire datetime.datetime для сравнения,
       чтобы избежать ошибки
       can't compare offset-naive and offset-aware datetimes
       :param date: datetime.datetime время
    """
    return datetime.datetime(date.year, date.month, date.day, date.hour, date.minute, date.second, tzinfo=datetime.timezone.utc)


def date_to_timestamp(date):
    """datetime.datetime to time.time()"""
    return time.mktime(date.timetuple())


def timestamp_to_date(stamp):
    """time.time() to datetime.datetime"""
    try:
        stamp = int(stamp)
    except ValueError:
        return None
    result = datetime.datetime.fromtimestamp(stamp)
    return result


def get_utc_date(in_timestamp: bool = False):
    """Вернуть текущую дату в utc
       :param in_timestamp: вернуть не дату, а timestamp
    """
    utcnow = datetime.datetime.utcnow()
    if in_timestamp:
        return utcnow.timestamp()
    return utcnow


def count_days_in_month(month, year):
    """Количество дней в месяце
       Год високосный, если он кратен 4, при этом не кратен 100
       Год високосный, если он кратен 400 (если не сработало первое условие)"""
    return calendar.monthrange(year, month)[1]


def str_to_date(date: str):
    """Дату из строки в datetime
       :param date: дата строкой
    """
    if not date:
        return None
    date = date.replace('.', '-')
    date = date.replace('/', '-')
    if date.endswith(' UTC'):
        date = date[:-4]

    for rega, formatter in regas_date:
        match = rega.match(date)
        if match:
            try:
                result = datetime.datetime.strptime(date, formatter)
            except:
                return None
            # ---------------------------------
            # Возвращаем дату, если времени нет
            # ---------------------------------
            if len(match.groups()) < 2:
                return datetime.date(result.year, result.month, result.day)
            return result
    return None


def date_plus_days(date, days=0, hours=0, minutes=0, seconds=0):
    """Сложение даты с днями/часами/минутами/секундами"""
    if type(date) == str:
        date = str_to_date(date)
    days = datetime.timedelta(days=days, hours=hours, minutes=minutes, seconds=seconds)
    date = date + days
    return date


def weekdayToStr(date, rp: bool = False, socr: bool = False):
    """День недели прописью
       :param rp: родительный падеж (кого, чего)
       :param socr: сокращенно день недели
    """
    weekdays = (('понедельник', 'понедельник', 'пн',),
                ('вторник', 'вторник', 'вт'),
                ('среда', 'среду', 'ср'),
                ('четверг', 'четверг', 'чт'),
                ('пятница', 'пятницу', 'пт'),
                ('суббота', 'суббот', 'сб'),
                ('воскресенье', 'воскресенье', 'вс'))
    if type(date) in (datetime.date, datetime.datetime):
        day = date.weekday()
    else:
        try:
            day = int(date)
        except:
            return ''

    for j in range(7):
        if day == j:
            if socr:
                return weekdays[day][2]
            if rp:
                return weekdays[day][1]
            return weekdays[day][0]
    return ''


def monthToStr(date, rp: bool = False, socr: bool = False):
    """Месяц прописью
       :param rp: родительный падеж (кого, чего)
       :param socr: сокращенно месяц
    """
    months = (('', '', ''),
              ('Январь', 'января', 'янв'),
              ('Февраль', 'февраля', 'фев'),
              ('Март', 'марта', 'мар'),
              ('Апрель', 'апреля', 'апр'),
              ('Май', 'мая', 'май'),
              ('Июнь', 'июня', 'июн'),
              ('Июль', 'июля', 'июл'),
              ('Август', 'августа', 'авг'),
              ('Сентябрь', 'сентября', 'сен'),
              ('Октябрь', 'октября', 'окт'),
              ('Ноябрь', 'ноября', 'ноя'),
              ('Декабрь', 'декабря', 'дек'))
    isCorrect = False
    try:
        month = int(date)
        isCorrect = True
    except:
        pass
    if type(date) in (datetime.date, datetime.datetime):
        month = date.month
        isCorrect = True

    if isCorrect:
        for j in range(13):
            if month == j:
                if socr:
                    return months[j][2]
                if rp:
                    return months[j][1]
                return months[j][0]
    return ''
