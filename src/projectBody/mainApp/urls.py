"""
URL configuration for FirstProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from firstpage import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='main'),  # Главная страница сайта
    path('admin/', admin.site.urls),     # Админка Django
    path('users/', include('users.urls')),  # URL-ы приложения пользователей
    path('profile/', include(('personalAccount.urls'), namespace='user_dashboard')),  # Личный кабинет с namespace
    path('catalog/', include('catalog.urls')),  # Каталог товаров
    path('orders/', include('orders.urls', namespace='orders')),  # Заказы с namespace
]

if settings.DEBUG:
    # При разработке добавляем маршруты для медиафайлов (картинки и т.п.)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
