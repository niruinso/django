from django.apps import AppConfig

class CatalogConfig(AppConfig):
    # Устанавливает тип поля по умолчанию для автоматического создания первичных ключей в моделях этого приложения
    default_auto_field = 'django.db.models.BigAutoField'
    
    # Имя приложения, которое Django будет использовать для его идентификации
    name = 'catalog' 