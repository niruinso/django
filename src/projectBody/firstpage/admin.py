from django.contrib import admin
from .models import Category, Product, ProductImage
from django.utils.html import format_html

class ProductImageInline(admin.TabularInline):
    # Встраиваемый класс для редактирования изображений товаров прямо в админке товара
    model = ProductImage
    extra = 1
    fields = ('image', 'order', 'image_preview')
    readonly_fields = ('image_preview',)
    
    def image_preview(self, obj):
        # Отображает миниатюру изображения в списке
        if obj.image:
            return format_html('<img src="{}" style="max-height: 100px;"/>', obj.image.url)
        return "-"
    image_preview.short_description = 'Превью'

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    # Настройка отображения и фильтров для модели Product в админке
    list_display = ('name', 'category', 'price', 'size')
    list_filter = ('category',)
    search_fields = ('name', 'description')
    inlines = [ProductImageInline]

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    # Настройка админки для модели Category с автозаполнением slug
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    # Админка для модели ProductImage с превью изображений
    list_display = ('product', 'order', 'image_preview')
    list_filter = ('product__category',)
    
    def image_preview(self, obj):
        # Миниатюрное превью изображения
        if obj.image:
            return format_html('<img src="{}" style="max-height: 50px;"/>', obj.image.url)
        return "-"
    image_preview.short_description = 'Превью'
