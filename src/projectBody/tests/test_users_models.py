from django.test import TestCase
from django.core.exceptions import ValidationError
from users.models import User

class UserModelTest(TestCase):
    """
    Тесты для модели пользователя.
    """
    def setUp(self):
        self.user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpass123',
            'phone_number': '+7(999)1234567',
            'address': 'Test Address'
        }

    def test_create_user(self):
        """Проверка создания обычного пользователя с корректными данными"""
        user = User.objects.create_user(**self.user_data)
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.email, 'test@example.com')
        self.assertTrue(user.check_password('testpass123'))
        self.assertEqual(user.phone_number, '+7(999)1234567')
        self.assertEqual(user.address, 'Test Address')
    
    def test_create_superuser(self):
        """Проверка создания суперпользователя с правильными правами"""
        admin = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='adminpass123'
        )
        self.assertTrue(admin.is_superuser)
        self.assertTrue(admin.is_staff)
    
    def test_create_user_unique_email(self):
        """Проверка уникальности email при создании пользователей"""
        User.objects.create_user(**self.user_data)
        with self.assertRaises(Exception):
            User.objects.create_user(
                username='another',
                email='test@example.com',
                password='testpass123'
            )