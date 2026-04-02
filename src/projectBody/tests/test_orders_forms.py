from django.test import TestCase
from django.contrib.auth import get_user_model
from decimal import Decimal
from orders.forms import OrderCreateForm
from firstpage.models import Category, Product
from orders.models import Order, OrderItem

class OrderCreateFormTest(TestCase):
    """Тесты для forms заказов"""
    def setUp(self):
        """Подготовка тестовых данных"""
        # Создаем пользователя
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        # Создаем категорию и товары
        self.category = Category.objects.create(
            name='Test Category',
            slug='test-category'
        )
        self.product1 = Product.objects.create(
            name='Test Product 1',
            price=Decimal('100.00'),
            description='Test Description 1',
            category=self.category
        )
        self.product2 = Product.objects.create(
            name='Test Product 2',
            price=Decimal('150.00'),
            description='Test Description 2',
            category=self.category
        )
        
        # Создаем заказ
        self.order = Order.objects.create(
            user=self.user,
            first_name='Danil',
            last_name='Trofimov',
            email='Danil@example.com',
            address='Zhurnalistov 2',
            postal_code='123456',
            city='Kazan'
        )
        
        # Создаем товары в заказе
        self.order_item1 = OrderItem.objects.create(
            order=self.order,
            product=self.product1,
            price=self.product1.price,
            quantity=2
        )
        self.order_item2 = OrderItem.objects.create(
            order=self.order,
            product=self.product2,
            price=self.product2.price,
            quantity=1
        )

    def test_order_create_form_valid(self):
        """Тест валидной формы создания заказа"""
        form_data = {
            'first_name': 'Danil',
            'last_name': 'Trofimov',
            'email': 'Danil@example.com',
            'address': 'Zhurnalistov 2',
            'postal_code': '123456',
            'city': 'Kazan'
        }
        form = OrderCreateForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_order_create_form_empty_fields(self):
        """Тест формы с пустыми полями"""
        form_data = {
            'first_name': '',
            'last_name': '',
            'email': '',
            'address': '',
            'postal_code': '',
            'city': ''
        }
        form = OrderCreateForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 6)

    def test_order_create_form_invalid_email(self):
        """Тест формы с некорректным email"""
        form_data = {
            'first_name': 'Danil',
            'last_name': 'Trofimov',
            'email': 'invalid',
            'address': 'Zhurnalistov 2',
            'postal_code': '123456',
            'city': 'Kazan'
        }
        form = OrderCreateForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)