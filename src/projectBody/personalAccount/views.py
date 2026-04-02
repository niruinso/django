from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, update_session_auth_hash, logout
from users.models import User
from .models import UserProfile, Profile
from .forms import CustomPasswordChangeForm, EmailChangeForm, PhoneNumberChangeForm, AddressChangeForm, AvatarUploadForm
from django.contrib import messages
from django.core.files.storage import default_storage
import os
from django.http import JsonResponse, HttpResponseForbidden
from .avatar_utils import handle_avatar_upload
from orders.models import Order
from django.utils import timezone

# users/views.py

def init_user_dashboard(request, user_id):
    # Инициализация профиля пользователя по user_id, создаёт профиль с уникальным ID и регистрационными данными, если отсутствует
    user = get_object_or_404(User, pk=user_id)
    profile, created = UserProfile.objects.get_or_create(
        user=user,
        defaults={
            'unique_id': f"USER-{user.id:04d}-{user.phone_number[-4:]}",
            'registration_data': {
                'email': user.email,
                'phone': user.phone_number,
                'username': user.username
            }
        }
    )
    return render(request, 'user_dashboard/init.html', {'profile': profile})

@login_required
def dashboard(request):
    # Отображение личного кабинета пользователя с профилем, создаёт профиль при первом заходе
    user = request.user
    profile, created = UserProfile.objects.get_or_create(
        user=user,
        defaults={
            'unique_id': f"USER-{user.id:04d}-{user.phone_number[-4:] if user.phone_number else '0000'}",
            'registration_data': {
                'email': user.email,
                'phone': user.phone_number if user.phone_number else None,
                'username': user.username
            }
        }
    )
    return render(request, 'personalAccount/profile.html', {
        'user': user,
        'profile': profile
    })

def custom_login(request):
    # Кастомный логин: аутентификация по username и паролю, при успехе — редирект в личный кабинет
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('user_dashboard:mainAccount')
    return render(request, 'users/login.html')

@login_required
def user_settings(request):
    # Управление настройками пользователя: смена пароля, email, телефона, адреса и загрузка аватара
    profile, created = Profile.objects.get_or_create(user=request.user)
    password_form = CustomPasswordChangeForm(request.user)
    email_form = EmailChangeForm(instance=request.user)
    phone_form = PhoneNumberChangeForm(instance=request.user)
    address_form = AddressChangeForm(instance=request.user)

    if request.method == 'POST': 
        if 'avatar' in request.FILES:
            # Обработка загрузки нового аватара
            form = AvatarUploadForm(request.POST, request.FILES)
            if form.is_valid():
                try:
                    saved_path = handle_avatar_upload(request.user, request.FILES['avatar'])
                    profile.avatar = saved_path
                    profile.save()
                    messages.success(request, 'Аватар успешно обновлён!')
                    return redirect('user_dashboard:user_settings')
                except Exception as e:
                    messages.error(request, f'Ошибка: {str(e)}')

        if 'change_password' in request.POST:
            # Обработка смены пароля
            password_form = CustomPasswordChangeForm(request.user, request.POST)
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)  # Чтобы не выкидывало после смены пароля
                messages.success(request, 'Ваш пароль был успешно изменен.')
                return redirect('user_dashboard:user_settings')
            else:
                messages.error(request, 'Пожалуйста, исправьте ошибки в форме смены пароля.')
        elif 'change_email' in request.POST:
            # Обработка смены email
            email_form = EmailChangeForm(request.POST, instance=request.user)
            if email_form.is_valid():
                email_form.save()
                messages.success(request, 'Ваш email был успешно изменен.')
                return redirect('user_dashboard:user_settings')
            else:
                messages.error(request, 'Пожалуйста, исправьте ошибки в форме смены email.')
        elif 'change_phone' in request.POST:
            # Обработка смены номера телефона
            phone_form = PhoneNumberChangeForm(request.POST, instance=request.user)
            if phone_form.is_valid():
                phone_form.save()
                messages.success(request, 'Ваш номер телефона был успешно изменен.')
                return redirect('user_dashboard:user_settings')
            else:
                messages.error(request, 'Пожалуйста, исправьте ошибки в форме смены номера телефона.')
        elif 'change_address' in request.POST:
            # Обработка смены адреса
            address_form = AddressChangeForm(request.POST, instance=request.user)
            if address_form.is_valid():
                address_form.save()
                messages.success(request, 'Ваш адрес был успешно изменен.')
                return redirect('user_dashboard:user_settings')
            else:
                messages.error(request, 'Пожалуйста, исправьте ошибки в форме смены адреса.')
    
    context = {
        'password_form': password_form,
        'email_form': email_form,
        'phone_form': phone_form,
        'address_form': address_form,
        'profile': profile 
    }
    return render(request, 'personalAccount/settings.html', context)


@login_required
def upload_avatar(request):
    if request.method == 'POST':
        form = AvatarUploadForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                # Обработка аватара
                messages.success(request, "Аватар успешно обновлен!")
                return redirect('user_dashboard:user_settings')  # Важно: редирект
            except Exception as e:
                messages.error(request, f"Ошибка: {str(e)}")
                return render(request, 'settings.html', {'form': form})
    
    # GET-запрос
    return render(request, 'settings.html', {'form': AvatarUploadForm()})

@login_required
def delete_avatar(request):
    profile = Profile.objects.get(user=request.user)
    profile.delete_avatar()
    return redirect('user_dashboard:mainAccount')

@login_required
def user_order_history(request):
    orders = Order.objects.filter(user=request.user, user_hidden=False).order_by('-created')
    return render(request, 'personalAccount/order_history.html', {'orders': orders})

@login_required
def hide_order_from_history(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    # Убедимся, что пользователь скрывает только свой заказ
    if order.user != request.user:
        return HttpResponseForbidden("У вас нет прав для выполнения этого действия.")
    
    if request.method == 'POST': # Обрабатываем только POST-запросы для безопасности
        order.user_hidden = True
        order.save()
        messages.success(request, f"Заказ #{order.id} был скрыт из вашей истории.")
        return redirect('user_dashboard:order_history')
    else:
        # Если это GET-запрос, просто перенаправляем (или можно показать страницу подтверждения)
        return redirect('user_dashboard:order_history')

@login_required
def delete_account(request):
    if request.method == 'POST':
        user = request.user
        
        # Delete related profiles first to avoid issues if user model is modified heavily
        UserProfile.objects.filter(user=user).delete()
        Profile.objects.filter(user=user).delete()
        
        # Anonymize and deactivate user
        user.first_name = ""
        user.last_name = ""
        # user.username = f"deleted_user_{user.id}_{timezone.now().strftime('%Y%m%d%H%M%S')}" # Optional: if you want to make username unique for deleted users
        user.phone_number = None
        user.address = None
        user.is_active = False
        user.save()
        
        logout(request) # Log the user out
        messages.success(request, 'Ваш аккаунт был успешно удален.')
        return redirect('main') # Redirect to homepage
    
    return render(request, 'personalAccount/delete_account_confirm.html')