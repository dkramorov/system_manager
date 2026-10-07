import os


def isfile(path: str):
    """Проверка, что переданный путь является файлом
       :param path: путь к файлу
    """
    return os.path.isfile(path)


def islink(path: str):
    """Проверка, что переданный путь является символической ссылкой
       :param path: путь к файлу
    """
    return os.path.islink(path)


def isdir(path: str):
    """Проверка, что переданный путь является папкой
       :param path: путь к папке
    """
    return os.path.isdir(path)


def get_file_size(path: str):
    """Размер файла в байтах
       :param path: путь к файлу
    """
    return os.path.getsize(file_path)


def is_image_ext(path: str):
    """Проверка, что это изображение по расширению файла
    """
    img_ext = ('jpg', 'jpeg', 'png', 'gif', 'bmp', 'webp')
    if path.split('.')[-1].lower() in img_ext:
        return True


def replacer(from_name: str,
             to_name: str,
             path: str = '/tmp',
             drop_empty_lines: bool = False):
    """Заменить строки во всех файлах
Пример:
from managers.path_manager import replacer
from_name='<base href="">'
to_name='<base href="/static/as_bootstrap/">'
path='/Users/jocker/astwobytes/packages/as_bootstrap/as_bootstrap/templates'
replacer(from_name=from_name, to_name=to_name, path=path)
---
       :param from_name: что меняем
       :param to_name: на что меняем
       :param path: папка, в которой ищем
       :param drop_empty_lines: удалять пустые строки
    """
    if isdir(path):
        dir_items = os.listdir(path)
        for dir_item in dir_items:
            item_path = os.path.join(path, dir_item)
            replacer(from_name=from_name, to_name=to_name, path=item_path)
    elif isfile(path):
        content = None
        with open(path, 'r', encoding='utf-8') as f:
            try:
                content = f.read()
            except Exception as e:
                print('open file failed %s' % path)
        if content and from_name in content:
            new_content = []
            for line in content.split('\n'):
                if from_name in line:
                    new_line = line.replace(from_name, to_name)
                    if new_line or not drop_empty_lines:
                        new_content.append(new_line)
                else:
                    if line or not drop_empty_lines:
                        new_content.append(line)
            with open(path, 'w', encoding='utf-8') as f:
                f.write('\n'.join(new_content))
            print('--- %s touched ---' % path)
