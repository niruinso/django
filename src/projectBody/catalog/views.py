from django.shortcuts import render, get_object_or_404
import os
from django.conf import settings
from collections import defaultdict
from firstpage.models import Product, Category
from cart.forms import CartAddProductForm

CATALOG_IMAGE_DIR = os.path.join(settings.MEDIA_ROOT, 'catalog_photos')

def get_catalog_images():
    """Сканирует директорию с изображениями и возвращает структурированные данные."""
    images_data = defaultdict(lambda: defaultdict(list))
    if not os.path.exists(CATALOG_IMAGE_DIR):
        return {}

    for filename in os.listdir(CATALOG_IMAGE_DIR):
        if filename.count('_') == 2: # проверяем, что в имени два разделителя 
            try:
                base_name, ext = os.path.splitext(filename)
                if ext.lower() not in ['.jpg', '.jpeg', '.png', '.gif']:
                    continue # пропускаем неизображения 

                category_id, product_id, image_num = base_name.split('_')
                
                image_url = os.path.join(settings.MEDIA_URL, 'catalog_photos', filename)
                images_data[category_id][product_id].append({
                    'url': image_url,
                    'name': filename,
                    'num': image_num
                })
            except ValueError:
                print(f"Файл не соответствует формату: {filename}")
                continue
    
    # сортируем изображения по номеру для каждого продукта
    for cat_id, products in images_data.items():
        for prod_id, image_list in products.items():
            image_list.sort(key=lambda x: int(x['num']))
            
    return images_data

def category_list(request):
    """Отображает список категорий."""
    images_data = get_catalog_images()
    
    # Получаем все категории и товары из базы данных
    categories_from_db = Category.objects.all()
    products_from_db = Product.objects.all()
    
    # Создаем словари для быстрого доступа по ID
    categories_dict = {str(c.id): c for c in categories_from_db}
    products_dict = {str(p.id): p for p in products_from_db}
    
    categories_with_products = []
    for category_id in sorted(list(images_data.keys())):
        category_obj = categories_dict.get(category_id) # Получаем объект категории
        if not category_obj: # Если категории нет в БД, пропускаем
            continue

        products_in_category = []
        for product_id, images in sorted(images_data[category_id].items()):
            product_obj = products_dict.get(product_id) # Получаем объект товара
            if product_obj: # Если товар существует в базе данных
                products_in_category.append({
                    'id': product_id,
                    'name': product_obj.name, # Используем реальное название товара
                    'images': images # Передаем все изображения
                })
        categories_with_products.append({
            'id': category_id,
            'name': category_obj.name, # Используем реальное название категории
            'products': products_in_category
        })
            
    context = {
        'categories_with_products': categories_with_products,
    }
    return render(request, 'catalog/category_list.html', context)

def product_list(request, category_id):
    """Отображает список товаров для выбранной категории."""
    images_data = get_catalog_images()
    category = get_object_or_404(Category, pk=category_id)
    
    # Получаем все товары, принадлежащие данной категории
    products_from_db = Product.objects.filter(category=category)
    
    # Создаем словарь товаров из базы данных для быстрого доступа по ID
    products_dict = {str(p.id): p for p in products_from_db}

    if category_id not in images_data:
        # Если нет изображений, но есть товары в базе, отображаем их названия
        product_items_no_images = []
        for product_db in products_from_db:
            product_items_no_images.append({
                'id': product_db.id,
                'name': product_db.name,
                'images': [] # Нет изображений
            })
        return render(request, 'catalog/product_list.html', {'products': product_items_no_images, 'category_id': category_id, 'category_name': category.name})

    products_in_category_raw = images_data[category_id]
    
    product_items = []
    for product_id, images in sorted(products_in_category_raw.items()):
        product_db = products_dict.get(product_id) # Получаем объект товара из словаря
        if product_db: # Проверяем, что товар существует в базе данных
            product_items.append({
                'id': product_id,
                'name': product_db.name, # Используем реальное название из базы данных
                'images': images # Передаем все изображения
            })

    context = {
        'products': product_items,
        'category_id': category_id,
        'category_name': category.name,
    }
    return render(request, 'catalog/product_list.html', context)

def product_detail(request, category_id, product_id):
    """Отображает детальную информацию о товаре со всеми его изображениями."""
    images_data = get_catalog_images()
    product = get_object_or_404(Product, pk=product_id)
    category = get_object_or_404(Category, pk=category_id)
    cart_product_form = CartAddProductForm()
    
    if category_id not in images_data or product_id not in images_data[category_id]:
        # Обработка ошибки, если товар не найден
        return render(request, 'catalog/product_detail.html', {'error': 'Товар не найден', 'cart_product_form': cart_product_form, 'category_name': category.name})

    product_images = images_data[category_id][product_id]
    
    context = {
        'category_id': category_id,
        'category_name': category.name,
        'product_id': product_id,
        'product_name': product.name,
        'product_description': product.description,
        'product_price': product.price,
        'product_size': product.size,
        'images': product_images,
        'product': product,
        'cart_product_form': cart_product_form,
    }
    return render(request, 'catalog/product_detail.html', context) 