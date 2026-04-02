from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .models import OrderItem, Order
from .forms import OrderCreateForm
from cart.cart import Cart 
from django.contrib.auth.decorators import login_required

@login_required
def order_create(request):
    # Создание заказа из содержимого корзины, доступно только авторизованным пользователям
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user  # привязываем заказ к текущему пользователю
            order.save()
            # Создаем элементы заказа для каждого товара из корзины
            for item in cart:
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'])
            cart.clear()  # очищаем корзину после оформления заказа
            request.session['order_id'] = order.id  # сохраняем id заказа в сессии для подтверждения
            return redirect(reverse('orders:order_created'))
    else:
        # Предзаполнение формы данными пользователя (если они есть)
        initial_data = {
            'first_name': request.user.first_name if hasattr(request.user, 'first_name') else '',
            'last_name': request.user.last_name if hasattr(request.user, 'last_name') else '',
            'email': request.user.email if hasattr(request.user, 'email') else ''
        }
        form = OrderCreateForm(initial=initial_data)
    return render(request, 'orders/create.html', {'cart': cart, 'form': form})


@login_required
def order_created(request):
    # Страница подтверждения успешного создания заказа
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order, id=order_id) if order_id else None
    return render(request, 'orders/created.html', {'order': order})
