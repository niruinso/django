from django.test import TestCase
from django.contrib.auth import get_user_model
from decimal import Decimal
from orders.models import Order, OrderItem
from firstpage.models import Category, Product

class OrderModelTest(TestCase):
    """Тесты для models заказов"""
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
            first_name='Ruslan',
            last_name='TeamLead',
            email='Ruslan@example.com',
            address='Test Address',
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

    def test_order_creation(self):
        """Тест создания заказа"""
        self.assertEqual(self.order.first_name, 'Ruslan')
        self.assertEqual(self.order.last_name, 'TeamLead')
        self.assertEqual(self.order.email, 'Ruslan@example.com')
        self.assertEqual(self.order.address, 'Test Address')
        self.assertEqual(self.order.postal_code, '123456')
        self.assertEqual(self.order.city, 'Kazan')
        self.assertFalse(self.order.paid)
        self.assertFalse(self.order.user_hidden)

    def test_order_total_cost(self):
        """Тест подсчета общей стоимости заказа"""
        self.assertEqual(self.order.get_total_cost(), Decimal('350.00'))

    def test_order_item_cost(self):
        """Тест подсчета стоимости позиций заказа"""
        self.assertEqual(self.order_item1.get_cost(), Decimal('200.00'))
        self.assertEqual(self.order_item2.get_cost(), Decimal('150.00'))

    def test_order_hide(self):
        """Тест скрытия заказа из истории"""
        self.order.user_hidden = True
        self.order.save()
        self.assertTrue(self.order.user_hidden) 