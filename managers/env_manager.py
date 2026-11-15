import os
from dotenv import find_dotenv, load_dotenv


env_path = find_dotenv(usecwd=True)  # Поиск от рабочей папки


if env_path:
    print('.env path %s, cwd %s' % (env_path, os.getcwd()))
    load_dotenv(env_path)
else:
    print('.env NOT found %s, cwd %s' % (env_path, os.getcwd()))


class MockSettings:
    FULL_SETTINGS_SET = {k: v for k, v in os.environ.items()}


settings_key = 'FULL_SETTINGS_SET'
settings_configs = {}


try:
    from django.conf import settings
    hasattr(settings, settings_key)
except Exception:
    #logger.info('Exception from django.conf import settings: %s' % e)
    settings = MockSettings()


def get_configs(prefix: str = 'PREFIX_', app: str = 'APP_') -> dict:
    """Получить из настроек конфигурации с префиксом,
       например,
       YANDEX_S3_HOST=storage.yandexcloud.net
       YANDEX_S3_PORT=443
       значит, get_configs(prefix='YANDEX_', app='S3')
       выдаст {'yandex': {'HOST': 'storage.yandexcloud.net', 'PORT': '443'}}
       :param prefix: префикс для переменных окружения
       :param app: приложение
    """
    if not prefix or not app:
        raise Exception('prefix and app required')
    if not prefix.endswith('_') or not app.endswith('_'):
        raise Exception('prefix and app have ends with _')
    if not hasattr(settings, settings_key):
        raise Exception('%s is not in settings' % settings_key)
    s = getattr(settings, settings_key)
    if not isinstance(s, dict):
        raise Exception('settings.%s is not dict' % settings_key)
    name_starts_with = '%s%s' % (prefix, app)

    key = prefix[:-1].lower()
    app = app[:-1].lower()
    if app in settings_configs and key in settings_configs[app]:
        return settings_configs[app]

    configs = {}
    for k, v in s.items():
        if not k.startswith(name_starts_with) or not k.replace(name_starts_with, ''):
            continue
        if not app in configs:
            configs[app] = {}
        if not key in configs[app]:
            configs[app][key] = {}
        name = k.split(name_starts_with, 1)[-1]
        configs[app][key][name] = v
    if not configs.get(app, {}).get(key, {}):
        raise Exception('there are no configs %s found' % name_starts_with)
    settings_configs[app] = configs[app]
    return settings_configs[app]
