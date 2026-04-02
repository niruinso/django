from django.apps import AppConfig


class FirstpageConfig(AppConfig):
    # Конфигурация приложения firstpage с указанием типа автоинкремента для первичного ключа
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'firstpage'
