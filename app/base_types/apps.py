from django.apps import AppConfig


class BaseTypesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'base_types'
    verbose_name = 'Объекты корпоративного профиля'
