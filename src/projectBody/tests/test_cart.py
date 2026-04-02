from django.test import TestCase, Client
from django.urls import reverse
from firstpage.models import Product, Category
from decimal import Decimal
from cart.cart import Cart
from cart.forms import CartAddProductForm

class CartTest(TestCase):
    """ Тесты для функциональности корзины """
    def setUp(self):
        self.client = Client()
        # Создаем тестовую категорию
        self.category = Category.objects.create(
            name='Test Category',
            slug='test-category'
        )
        # Создаем тестовый товар
        self.product = Product.objects.create(
            name='Test Product',
            price=Decimal('100.00'),
            description='Test Description',
            category=self.category
        )
        self.product2 = Product.objects.create(
            name='Test Product 2',
            price=Decimal('200.00'),
            description='Test Description 2',
            category=self.category
        )
       

    def test_cart_class(self):
        # Тест инициализации корзины
        cart = Cart(self.client)
        self.assertEqual(len(cart), 0)
        
        # Тест добавления товара
        cart.add(self.product, quantity=2)
        self.assertEqual(len(cart), 2)
        
        # Тест обновления количества
        cart.add(self.product, quantity=1, update_quantity=True)
        self.assertEqual(len(cart), 1)

        # Тест добавления второго вида товара
        cart.add(self.product2, quantity=2)
        self.assertEqual(len(cart), 3)

        # Тест подсчета общей стоимости
        self.assertEqual(cart.get_total_price(), Decimal('500.00'))
        
        # Тест удаления товара
        cart.remove(self.product)
        cart.remove(self.product2)
        self.assertEqual(len(cart), 0)

    def test_cart_form(self):
        """Тесты для формы добавления товара в корзину"""
        # Тест валидной формы
        form_data = {'quantity': 2, 'update': False}
        form = CartAddProductForm(data=form_data)
        self.assertTrue(form.is_valid())
        
        # Тест невалидной формы
        form_data = {'quantity': 25, 'update': False}
        form = CartAddProductForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_cart_views(self):
        # Тест добавления товара в корзину
        response = self.client.post( reverse('cart:cart_add', args=[self.product.id]), {'quantity': 2, 'update': False})
        self.assertEqual(response.status_code, 302)
        
        # Тест просмотра корзины
        response = self.client.get(reverse('cart:cart_detail'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cart/detail.html')
        
        # Тест удаления товара из корзины
        response = self.client.post( reverse('cart:cart_remove', args=[self.product.id]))
        self.assertEqual(response.status_code, 302)
    
    def test_cart_context(self):
        """Тесты для проверки контекста корзины"""
        self.client.post(reverse('cart:cart_add', args=[self.product.id]), 
                        {'quantity': 2, 'update': False})
        response = self.client.get(reverse('cart:cart_detail'))
        self.assertEqual(response.status_code, 200)

        # Проверяем наличие корзины в контексте
        self.assertIn('cart', response.context)

        # Проверяем количество товара и общую стоимость
        cart = response.context['cart']
        self.assertEqual(len(cart), 2)
        self.assertEqual(cart.get_total_price(), Decimal('200.00'))
        
        