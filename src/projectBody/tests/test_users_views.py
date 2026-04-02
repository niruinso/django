from django.test import TestCase, Client
from django.urls import reverse
from users.models import User

class UserRegistrationTest(TestCase):
    """
    Тесты для представления регистрации пользователя.
    Проверяет успешную регистрацию и обработку ошибок.
    """
    def setUp(self):
        self.client = Client()
        self.register_url = reverse('register')
        self.valid_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': 'testpass123',
            'password2': 'testpass123',
            'phone_number': '+7(999)1234567'
        }

    def test_registration_success(self):
        """Проверка успешной регистрации пользователя"""
        response = self.client.post(self.register_url, self.valid_data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='testuser').exists())

    def test_registration_duplicate_email(self):
        """Проверка обработки попытки регистрации с существующим email"""
        User.objects.create_user(
            username='existing',
            email='test@example.com',
            password='testpass123'
        )
        response = self.client.post(self.register_url, self.valid_data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Этот email уже используется')
    
    def test_registration_password_mismatch(self):
        """Проверка обработки несовпадающих паролей при регистрации"""
        data = self.valid_data.copy()
        data['password2'] = 'anotherpass'
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username='testuser').exists())

class UserLoginTest(TestCase):
    """
    Тесты для представления входа пользователя.
    Проверяет успешный вход и обработку ошибок аутентификации.
    """
    def setUp(self):
        self.client = Client()
        self.login_url = reverse('login')
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
    
    def test_login_succes(self):
        """Проверка успешного входа пользователя"""
        response = self.client.post(self.login_url, {
            'username': 'test@example.com',
            'password': 'testpass123'
        })
        self.assertEqual(response.status_code, 302)
    
    def test_login_wrong_pass(self):
        """Проверка входа с неверным паролем"""
        response = self.client.post(self.login_url, {
            'username': 'test@example.com',
            'password': 'wrongpass'
        })
        self.assertEqual(response.status_code, 200)
    
    def test_login_wrong_login(self):
        """Проверка входа с несуществующим email"""
        response = self.client.post(self.login_url, {
            'username': 'notuser',
            'password': 'testpass123'
        })
        self.assertEqual(response.status_code, 200)