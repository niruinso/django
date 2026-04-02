from django.urls import path, include
from . import views
from personalAccount.views import custom_login
from personalAccount.views import upload_avatar

app_name = 'user_dashboard'

urlpatterns = [
    path('init/<int:user_id>/', views.init_user_dashboard, name='init'),
    path('', views.dashboard, name='mainAccount'),
    path('login/', custom_login, name='login'),
    path('settings/', views.user_settings, name='user_settings'),
    path('upload_avatar/', upload_avatar, name='upload_avatar'),
    path('orders/', views.user_order_history, name='order_history'),
    path('order/hide/<int:order_id>/', views.hide_order_from_history, name='hide_order_from_history'),
    path('delete-account/', views.delete_account, name='delete_account'),
]
