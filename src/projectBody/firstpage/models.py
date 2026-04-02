from django.db import models
from django.urls import reverse
from django.utils.text import slugify

class Category(models.Model):
    name = models.CharField('Название', max_length=100)  # Название категории
    slug = models.SlugField(unique=True, blank=True)    # Уникальный слаг для URL, генерируется из name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)  # Автоматически создаём слаг из имени, если он не задан
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name  # Читаемое представление объекта — название категории

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')  # Связь с категорией
    name = models.CharField('Название', max_length=100)          # Название продукта
    description = models.TextField('Описание')                   # Описание продукта
    price = models.DecimalField('Цена', max_digits=10, decimal_places=2)  # Цена с двумя знаками после запятой
    size = models.CharField('Размер', max_length=50, blank=True) # Размер продукта, необязательное поле
    created_at = models.DateTimeField(auto_now_add=True)         # Дата создания записи

    def __str__(self):
        return self.name  # Читаемое представление — название продукта

    def get_absolute_url(self):
        # URL для детального просмотра продукта с передачей id категории и самого продукта
        return reverse('catalog:product_detail', args=[str(self.category.id), str(self.id)])

def product_image_path(instance, filename):
    # Генерация пути загрузки для изображения продукта в формате media/catalog_photos/categoryID_productID_order.jpg
    return f'catalog_photos/{instance.product.category.id}_{instance.product.id}_{instance.order}.jpg'

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')  # Изображения связаны с продуктом
    image = models.ImageField('Фото', upload_to=product_image_path)  # Загружаемое изображение с кастомным путем
    order = models.PositiveIntegerField('Порядковый номер', default=0)  # Порядок отображения изображений

    class Meta:
        ordering = ['order']  # Сортировка изображений по полю order

    def __str__(self):
        return f"Фото {self.order} для {self.product.name}"  # Строковое представление с порядком и названием продукта
