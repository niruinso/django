from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from users.models import User
from django.core.files.storage import default_storage
from personalAccount.models import Profile
from personalAccount.avatar_utils import handle_avatar_upload
import os

class AvatarUtilsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.profile = Profile.objects.create(user=self.user)
        
        # Создаем тестовый файл изображения
        self.image_content = b'fake-image-content'
        self.image = SimpleUploadedFile(
            name='test_image.jpg',
            content=self.image_content,
            content_type='image/jpeg'
        )

    def tearDown(self):
        # Очищаем тестовые файлы после каждого теста
        avatar_dir = f"avatars/user_{self.user.id}/"
        if default_storage.exists(avatar_dir):
            for file in default_storage.listdir(avatar_dir)[1]:
                default_storage.delete(os.path.join(avatar_dir, file))
            default_storage.delete(avatar_dir)

    def test_handle_avatar_upload(self):
        """Тест загрузки аватара"""
        saved_path = handle_avatar_upload(self.user, self.image)
        
        # Проверяем, что файл был сохранен
        self.assertTrue(default_storage.exists(saved_path))
        
        # Проверяем, что путь соответствует ожидаемому формату
        expected_dir = f"avatars/user_{self.user.id}/"
        self.assertTrue(saved_path.startswith(expected_dir))
        self.assertTrue(saved_path.endswith('.jpg'))

    def test_handle_avatar_upload_creates_directory(self):
        """Тест создания директории для аватара"""
        # Удаляем директорию, если она существует
        avatar_dir = f"avatars/user_{self.user.id}/"
        if default_storage.exists(avatar_dir):
            for file in default_storage.listdir(avatar_dir)[1]:
                default_storage.delete(os.path.join(avatar_dir, file))
            default_storage.delete(avatar_dir)
        
        # Загружаем аватар
        handle_avatar_upload(self.user, self.image)
        
        # Проверяем, что директория была создана
        self.assertTrue(default_storage.exists(avatar_dir))

    def test_handle_avatar_upload_with_different_extension(self):
        """Тест загрузки аватара с другим расширением"""
        # Создаем файл с расширением .png
        png_image = SimpleUploadedFile(
            name='test_image.png',
            content=b'fake-png-content',
            content_type='image/png'
        )
        
        saved_path = handle_avatar_upload(self.user, png_image)
        
        # Проверяем, что файл был сохранен с правильным расширением
        self.assertTrue(saved_path.endswith('.png'))
        self.assertTrue(default_storage.exists(saved_path)) 