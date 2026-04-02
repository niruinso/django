from django.apps import AppConfig

# Конфигурация приложения "orders" для Django с указанием типа авто-поля и имени приложения
class OrdersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'orders'
