# -*- coding: utf-8 -*-
import datetime
import os
import psutil
import sys
import socket
import subprocess


def system_cmd(cmd: list):
    """Выполнить системную команду, например, "which pg_dump"
       :param cmd: команда списком, например, ["cat", "/etc/"]
       В команду можно добавлять timeout (timeout 5 ping -c 3 somehost)
    """
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    (out, err) = proc.communicate()
    if err:
        raise Exception(err.decode('utf-8'))
    return out.decode('utf-8').strip()


def get_platform():
    """Определяем операционную систему
    """
    platform = 'unknown'
    if 'darwin' in sys.platform:
        platform = 'mac'
    elif 'linux' in sys.platform:
        platform = 'linux'
    return platform


def get_locale():
    """Возвращает локаль,
       функция здесь для информации:
       иногда через LaunchAgents запускается локаль US-ASCII (None, None)
       вместо utf-8 и проблема с записью и чтением файла начинается
    """
    import locale
    return (locale.getpreferredencoding(False), locale.getlocale())


def get_hostname():
    """Возвращаем имя хоста
    """
    return socket.gethostname()


def get_hd_space(dev: str = '/'):
    """Получить информацию по месту на диске в МБ
       :param dev: точка монтирования
    """
    space = psutil.disk_usage('/')
    return {
        'free': space.free / 1024 / 1024,
        'used': space.used / 1024 / 1024,
        'total': space.total / 1024 / 1024,
        'percent': space.percent,
    }


def search_binary(cmd):
    """Поиск исполняемого файла в системе
       :param cmd: исполняемый файл
    """
    search = '/usr/bin/which'
    search_cmd = '%s %s' % (search, cmd)
    f = os.popen(search_cmd)
    result = f.read()
    linux_prefix = '%s:' % cmd
    if linux_prefix in result:
        result = result.replace(linux_prefix, '')
    result = result.strip()
    if ' ' in result:
        result = result.split(' ')[0]
    return result.strip()


def get_psutil_attr_names():
    return list(psutil.Process().as_dict().keys())


def search_process_created_time(process):
    """Ищет время создания процесса по результатам
       работы search_process
    """
    created = 'create_time'
    if not process or not created in process:
        return

    stamp = None
    if isinstance(process, str):
        start = process.index(created) + len(created)
        end = process[start:].index(',')
        result = process[start:start+end]
        result = result.replace(':', ' ').replace('\'', '')
        result = result.strip().split('.')[0]
    elif isinstance(process, dict):
        result = str(process[created]).split('.')[0]
    if not result:
        return
    try:
        stamp = int(result)
    except ValueError:
        return None
    return datetime.datetime.fromtimestamp(stamp)


def search_process(q: list):
    """Ищем процесс

       Если возникает ошибка OSError: [Errno 5] Input/output error
       pip3 install psutil --upgrade

       :param q: список строк для поиска
       Посмотреть все свойства можно get_psutil_attr_names()
    """
    if not isinstance(q, list) and not isinstance(q, tuple):
        assert False
    mypid = os.getpid()
    myppid = os.getppid()
    for obj in psutil.process_iter():
        try:
            process = obj.as_dict(attrs=['pid', 'cmdline', 'create_time', ])
        except OSError as e:
            print(e)
            print('pip3 install psutil --upgrade')
            exit()
        if not process['cmdline']:
            continue
        if process['pid'] == mypid or process['pid'] == myppid:
            continue
        match = True
        for item in q:
            in_cmd = list(filter(lambda x: item in x, process['cmdline']))
            #print(in_cmd)
            if not in_cmd:
                match = False
                break
        if match:
            started = search_process_created_time(process)
            if isinstance(process, dict):
                process['started'] = started.strftime('%H:%M:%S %d-%m-%Y')
            return process
    return None
