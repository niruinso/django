from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

##Название приложения
app_name = 'catalog'

##Подключаем необходимые ссылки
urlpatterns = [
    path('', views.category_list, name='category_list'),
    path('category/<str:category_id>/', views.product_list, name='product_list'),
    path('product/<str:category_id>/<str:product_id>/', views.product_detail, name='product_detail'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)