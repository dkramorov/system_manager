Описание
-----------
Менеджер для работы с системой

Установка пакетом
-----------
Для локальной разработки::
    pip install -e packages/system_manager
Для обычной установки через requirements.txt::
    system_manager @ git+https://github.com/dkramorov/system_manager.git


Импорт
-----------
Проверка::
    from managers.system_manager import system_cmd


Удаление
-----------
Удалить пакет::
    pip uninstall system_manager

Для создания пакета
https://docs.python.org/3.10/distutils/introduction.html#distutils-simple-example
https://docs.python.org/3.10/distutils/sourcedist.html
::
    python setup.py sdist




