from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from firstpage.models import Product
from .cart import Cart
from .forms import CartAddProductForm

@require_POST
def cart_add(request, product_id):
    # Добавляет товар в корзину или обновляет количество, если форма валидна
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product,
                 quantity=cd['quantity'],
                 update_quantity=cd['update'])
    return redirect('cart:cart_detail')

@require_POST
def cart_remove(request, product_id):
    # Удаляет товар из корзины и перенаправляет на страницу корзины
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')

def cart_detail(request):
    # Показывает содержимое корзины с формами для обновления количества каждого товара
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={'quantity': item['quantity'],
                                                               'update': True})
    return render(request, 'cart/detail.html', {'cart': cart})
