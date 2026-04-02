from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    # Кастомная модель пользователя с дополнительными полями и использованием email как логина
    
    USER_TYPE_CHOICES = (
        ('user', 'User'),  # Вариант типа пользователя, можно расширять
    )
    
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='user')  # Тип пользователя
    phone_number = models.CharField(max_length=15, blank=True, null=True)  # Телефонный номер пользователя
    address = models.TextField(blank=True, null=True)  # Адрес пользователя
    email = models.EmailField(unique=True)  # Email используется как уникальный идентификатор
    
    USERNAME_FIELD = 'email'  # Вход по email
    REQUIRED_FIELDS = ['username']  # Поля, обязательные при создании через createsuperuser

