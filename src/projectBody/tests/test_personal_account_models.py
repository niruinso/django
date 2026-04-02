from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from users.models import User
from personalAccount.models import UserProfile, Profile
import os

class UserProfileModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.registration_data = {
            'first_name': 'Test',
            'last_name': 'User',
            'phone': '+7999999999'
        }
        self.user_profile = UserProfile.objects.create(
            user=self.user,
            unique_id='TEST123',
            registration_data=self.registration_data
        )

    def test_user_profile_creation(self):
        """Тест создания профиля пользователя"""
        self.assertEqual(self.user_profile.user, self.user)
        self.assertEqual(self.user_profile.unique_id, 'TEST123')
        self.assertEqual(self.user_profile.registration_data, self.registration_data)
        self.assertIsNotNone(self.user_profile.created_at)

    def test_user_profile_str(self):
        """Тест строкового представления профиля"""
        expected_str = f"TEST123 - {self.user.email}"
        self.assertEqual(str(self.user_profile), expected_str)

    def test_unique_id_constraint(self):
        """Тест уникальности поля unique_id"""
        with self.assertRaises(Exception):
            UserProfile.objects.create(
                user=self.user,
                unique_id='TEST123',
                registration_data={}
            )

class ProfileModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.profile = Profile.objects.create(user=self.user)

    def test_profile_creation(self):
        """Тест создания профиля"""
        self.assertEqual(self.profile.user, self.user)
        self.assertFalse(self.profile.avatar)

    def test_avatar_upload(self):
        """Тест загрузки аватара"""
        # Создаем тестовый файл изображения
        image_content = b'fake-image-content'
        image = SimpleUploadedFile(
            name='test_image.jpg',
            content=image_content,
            content_type='image/jpeg'
        )
        
        self.profile.avatar = image
        self.profile.save()
        
        self.assertTrue(self.profile.avatar)
        self.assertTrue(os.path.exists(self.profile.avatar.path))

    def test_avatar_deletion(self):
        """Тест удаления аватара"""
        # Создаем и загружаем аватар
        image_content = b'fake-image-content'
        image = SimpleUploadedFile(
            name='test_image.jpg',
            content=image_content,
            content_type='image/jpeg'
        )
        
        self.profile.avatar = image
        self.profile.save()
        
        # Удаляем аватар
        self.profile.delete_avatar()
        self.assertFalse(self.profile.avatar)

    def test_profile_deletion(self):
        """Тест удаления профиля"""
        # Создаем и загружаем аватар
        image_content = b'fake-image-content'
        image = SimpleUploadedFile(
            name='test_image.jpg',
            content=image_content,
            content_type='image/jpeg'
        )
        
        self.profile.avatar = image
        self.profile.save()
        
        avatar_path = self.profile.avatar.path
        self.profile.delete()
        
        # Проверяем, что файл аватара был удален
        self.assertFalse(os.path.exists(avatar_path)) 