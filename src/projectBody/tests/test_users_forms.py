from django.test import TestCase
from users.forms import UserRegistrationForm
from users.models import User

class UserRegistrationFormTest(TestCase):
    """
    Тесты для формы регистрации пользователя.
    """
    def setUp(self):
        self.valid_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': 'testpass123',
            'password2': 'testpass123',
            'phone_number': '+7(999)1234567',
            'address': 'Test Address'
        }
    
    def test_form_validation(self):
        """Проверка успешной валидации формы с корректными данными"""
        form = UserRegistrationForm(data=self.valid_data)
        self.assertTrue(form.is_valid())
    
    def test_form_validation_duplicate_email(self):
        """Проверка валидации при попытке использовать существующий email"""
        User.objects.create_user(
            username='existing',
            email='test@example.com',
            password='testpass123'
        )
        form = UserRegistrationForm(data=self.valid_data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)
        self.assertEqual(form.errors['email'][0], 'Этот email уже используется')

    def test_form_validation_password_mismatch(self):
        """Проверка валидации при несовпадении паролей"""
        data = self.valid_data.copy()
        data['password2'] = 'anotherpass'
        form = UserRegistrationForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)

    def test_form_validation_reqiured_fields(self):
        """Проверка валидации обязательных полей формы"""
        required_fields = ['username', 'email', 'password1', 'password2', 'phone_number']
        for field in required_fields:
            data = self.valid_data.copy()
            del data[field]
            form = UserRegistrationForm(data=data)
            self.assertFalse(form.is_valid())
            self.assertIn(field, form.errors)