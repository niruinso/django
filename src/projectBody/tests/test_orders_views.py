from django.test import TestCase, Client
from django.urls import reverse
from users.models import User
from orders.models import Order, OrderItem
from firstpage.models import Product, Category
from cart.cart import Cart
from decimal import Decimal

class OrderCreateTest(TestCase):
    """
    Тесты для представления создания заказа.
    Проверяет успешное создание заказа и обработку ошибок.
    """
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            first_name='Test',
            last_name='User'
        )
        self.client.login(username='test@example.com', password='testpass123')
        self.category = Category.objects.create(name='Test Category')
        self.product = Product.objects.create(
            name='Test Product',
            description='Test Description',
            price=Decimal('100.00'),
            category=self.category
        )
        self.cart = Cart(self.client)
        self.cart.add(product=self.product, quantity=1)
        
    def test_order_create_success(self):
        """Проверка успешного создания заказа"""
        response = self.client.post(reverse('orders:order_create'), {
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'test@example.com',
            'address': 'Test Address',
            'postal_code': '123456',
            'city': 'Test City'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Order.objects.filter(user=self.user).exists())

class OrderCreatedTest(TestCase):
    """
    Тесты для представления успешного создания заказа.
    """
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.client.login(username='test@example.com', password='testpass123')
        self.order = Order.objects.create(
            user=self.user,
            first_name='Test',
            last_name='User',
            email='test@example.com',
            address='Test Address',
            postal_code='123456',
            city='Test City'
        )
        
    def test_order_created_success(self):
        """Проверка отображения страницы успешного создания заказа"""
        session = self.client.session
        session['order_id'] = self.order.id
        session.save()
        response = self.client.get(reverse('orders:order_created'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['order'], self.order)

    def test_order_created_without_order_id(self):
        """Проверка отображения страницы без ID заказа в сессии"""
        response = self.client.get(reverse('orders:order_created'))
        self.assertEqual(response.status_code, 200)
        self.assertIsNone(response.context['order']) 