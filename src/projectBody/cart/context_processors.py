from .cart import Cart
 
def cart(request):
    # Создаёт и возвращает словарь с ключом 'cart', 
    return {'cart': Cart(request)} 