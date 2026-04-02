from django.test import TestCase, Client
from django.urls import reverse
from users.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from personalAccount.models import UserProfile, Profile
from orders.models import Order
from django.contrib import messages

class PersonalAccountViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            phone_number='+7999999999'
        )
        self.profile = Profile.objects.create(user=self.user)
        self.user_profile = UserProfile.objects.create(
            user=self.user,
            unique_id='TEST123',
            registration_data={
                'email': self.user.email,
                'phone': self.user.phone_number,
                'username': self.user.username
            }
        )
        # Убедимся, что пользователь аутентифицирован
        self.client.force_login(self.user)

    def test_dashboard_view(self):
        """Тест отображения личного кабинета"""
        response = self.client.get(reverse('user_dashboard:mainAccount'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'personalAccount/profile.html')
        self.assertIn('user', response.context)
        self.assertIn('profile', response.context)

    def test_user_settings_view_get(self):
        """Тест отображения страницы настроек (GET)"""
        response = self.client.get(reverse('user_dashboard:user_settings'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'personalAccount/settings.html')
        self.assertIn('password_form', response.context)
        self.assertIn('email_form', response.context)
        self.assertIn('phone_form', response.context)
        self.assertIn('address_form', response.context)
        self.assertIn('profile', response.context)

    def test_change_password(self):
        """Тест изменения пароля"""
        response = self.client.post(
            reverse('user_dashboard:user_settings'),
            {
                'change_password': True,
                'old_password': 'testpass123',
                'new_password1': 'newpass123',
                'new_password2': 'newpass123'
            }
        )
        self.assertEqual(response.status_code, 302)
        # Обновляем пользователя из базы данных
        self.user.refresh_from_db()
        # Проверяем, что пароль изменился
        self.assertTrue(self.user.check_password('newpass123'))

    def test_change_email(self):
        """Тест изменения email"""
        response = self.client.post(
            reverse('user_dashboard:user_settings'),
            {
                'change_email': True,
                'email': 'new@example.com'
            }
        )
        self.assertEqual(response.status_code, 302)
        # Обновляем пользователя из базы данных
        self.user.refresh_from_db()
        self.assertEqual(self.user.email, 'new@example.com')

    def test_change_phone(self):
        """Тест изменения номера телефона"""
        response = self.client.post(
            reverse('user_dashboard:user_settings'),
            {
                'change_phone': True,
                'phone_number': '+7888888888'
            }
        )
        self.assertEqual(response.status_code, 302)
        # Обновляем пользователя из базы данных
        self.user.refresh_from_db()
        self.assertEqual(self.user.phone_number, '+7888888888')

    def test_change_address(self):
        """Тест изменения адреса"""
        response = self.client.post(
            reverse('user_dashboard:user_settings'),
            {
                'change_address': True,
                'address': 'Новый адрес'
            }
        )
        self.assertEqual(response.status_code, 302)
        # Обновляем пользователя из базы данных
        self.user.refresh_from_db()
        self.assertEqual(self.user.address, 'Новый адрес')

    def test_upload_avatar(self):
        """Тест загрузки аватара"""
        image_content = b'fake-image-content'
        image = SimpleUploadedFile(
            name='test_image.jpg',
            content=image_content,
            content_type='image/jpeg'
        )
        response = self.client.post(
            reverse('user_dashboard:user_settings'),
            {'avatar': image}
        )
        self.assertEqual(response.status_code, 200)
        # Обновляем профиль из базы данных
        self.profile.refresh_from_db()
        self.assertIsNotNone(self.profile.avatar)

    def test_delete_avatar(self):
        """Тест удаления аватара"""
        # Создаем тестовый аватар
        image_content = b'fake-image-content'
        image = SimpleUploadedFile(
            name='test_image.jpg',
            content=image_content,
            content_type='image/jpeg'
        )
        self.profile.avatar = image
        self.profile.save()
        
        # Проверяем, что аватар был создан
        self.assertTrue(self.profile.avatar)
        
        # Удаляем аватар
        self.profile.delete_avatar()
        
        # Обновляем профиль из базы данных
        self.profile.refresh_from_db()
        
        # Проверяем, что аватар был удален
        self.assertFalse(self.profile.avatar)

    def test_order_history(self):
        """Тест отображения истории заказов"""
        # Создаем тестовый заказ
        order = Order.objects.create(
            user=self.user,
            first_name='Test',
            last_name='User',
            email='test@example.com',
            address='Test Address',
            postal_code='123456',
            city='Test City',
            paid=True
        )
        
        response = self.client.get(reverse('user_dashboard:order_history'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'personalAccount/order_history.html')
        self.assertIn('orders', response.context)
        self.assertEqual(len(response.context['orders']), 1)

    def test_hide_order(self):
        """Тест скрытия заказа из истории"""
        # Создаем тестовый заказ
        order = Order.objects.create(
            user=self.user,
            first_name='Test',
            last_name='User',
            email='test@example.com',
            address='Test Address',
            postal_code='123456',
            city='Test City',
            paid=True
        )
        
        response = self.client.post(
            reverse('user_dashboard:hide_order_from_history', args=[order.id])
        )
        self.assertEqual(response.status_code, 302)
        # Обновляем заказ из базы данных
        order.refresh_from_db()
        self.assertTrue(order.user_hidden)

    def test_delete_account(self):
        """Тест удаления аккаунта"""
        response = self.client.post(reverse('user_dashboard:delete_account'))
        self.assertEqual(response.status_code, 302)
        
        # Обновляем пользователя из базы данных
        self.user.refresh_from_db()
        self.assertFalse(self.user.is_active)
        
        # Проверяем, что профили удалены
        self.assertFalse(UserProfile.objects.filter(user=self.user).exists())
        self.assertFalse(Profile.objects.filter(user=self.user).exists()) 