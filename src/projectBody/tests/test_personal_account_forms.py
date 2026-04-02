from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from users.models import User
from personalAccount.forms import (
    CustomPasswordChangeForm,
    EmailChangeForm,
    PhoneNumberChangeForm,
    AddressChangeForm,
    AvatarUploadForm
)
from PIL import Image
import io

class CustomPasswordChangeFormTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='oldpass123'
        )
        self.form_data = {
            'old_password': 'oldpass123',
            'new_password1': 'newpass123',
            'new_password2': 'newpass123'
        }

    def test_form_labels(self):
        """Тест меток полей формы"""
        form = CustomPasswordChangeForm(self.user)
        self.assertEqual(form.fields['old_password'].label, "Старый пароль")
        self.assertEqual(form.fields['new_password1'].label, "Новый пароль")
        self.assertEqual(form.fields['new_password2'].label, "Подтверждение нового пароля")

    def test_form_validation(self):
        """Тест валидации формы"""
        form = CustomPasswordChangeForm(self.user, self.form_data)
        self.assertTrue(form.is_valid())

    def test_form_validation_wrong_old_password(self):
        """Тест валидации формы с неверным старым паролем"""
        form_data = self.form_data.copy()
        form_data['old_password'] = 'wrongpass'
        form = CustomPasswordChangeForm(self.user, form_data)
        self.assertFalse(form.is_valid())

    def test_form_validation_password_mismatch(self):
        """Тест валидации формы с несовпадающими паролями"""
        form_data = self.form_data.copy()
        form_data['new_password2'] = 'differentpass'
        form = CustomPasswordChangeForm(self.user, form_data)
        self.assertFalse(form.is_valid())

class EmailChangeFormTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )

    def test_form_validation(self):
        """Тест валидации формы изменения email"""
        form_data = {'email': 'new@example.com'}
        form = EmailChangeForm(instance=self.user, data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_validation_invalid_email(self):
        """Тест валидации формы с неверным email"""
        form_data = {'email': 'invalid-email'}
        form = EmailChangeForm(instance=self.user, data=form_data)
        self.assertFalse(form.is_valid())

class PhoneNumberChangeFormTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )

    def test_form_validation(self):
        """Тест валидации формы изменения номера телефона"""
        form_data = {'phone_number': '+7999999999'}
        form = PhoneNumberChangeForm(instance=self.user, data=form_data)
        self.assertTrue(form.is_valid())

class AddressChangeFormTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )

    def test_form_validation(self):
        """Тест валидации формы изменения адреса"""
        form_data = {'address': 'ул. Пушкина, д. 1'}
        form = AddressChangeForm(instance=self.user, data=form_data)
        self.assertTrue(form.is_valid())

class AvatarUploadFormTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )

    def test_form_validation(self):
        """Тест валидации формы загрузки аватара"""
        # Создаем реальное изображение
        image = Image.new('RGB', (100, 100), color='red')
        image_io = io.BytesIO()
        image.save(image_io, format='JPEG')
        image_io.seek(0)
        
        # Создаем файл для загрузки
        uploaded_file = SimpleUploadedFile(
            name='test_image.jpg',
            content=image_io.getvalue(),
            content_type='image/jpeg'
        )
        
        form = AvatarUploadForm(data={'change_avatar': True}, files={'avatar': uploaded_file})
        self.assertTrue(form.is_valid(), form.errors.as_text())

    def test_form_validation_no_file(self):
        """Тест валидации формы без файла"""
        form = AvatarUploadForm(data={}, files={})
        self.assertFalse(form.is_valid())

    def test_form_validation_invalid_file_type(self):
        """Тест валидации формы с неверным типом файла"""
        image_content = b'fake-image-content'
        image = SimpleUploadedFile(
            name='test_image.txt',
            content=image_content,
            content_type='text/plain'
        )
        form = AvatarUploadForm(data={}, files={'avatar': image})
        self.assertFalse(form.is_valid()) 