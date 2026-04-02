from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegistrationForm
from personalAccount.models import UserProfile
def register_user(request):
    # Регистрация нового пользователя через форму UserRegistrationForm
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            # Заполняем дополнительные поля и устанавливаем пароль
            user.email = form.cleaned_data['email']
            user.username = form.cleaned_data['username']
            user.phone_number = form.cleaned_data['phone_number']
            user.set_password(form.cleaned_data['password1'])
            user.save()
            # Создаем профиль с уникальным ID на основе user.id и последних 4 цифр телефона
            phone_suffix = user.phone_number[-4:] if user.phone_number and len(user.phone_number) >= 4 else '0000'
            profile_id_value = f"USER-{user.id:04d}-{phone_suffix}"
            UserProfile.objects.create(user=user, unique_id=profile_id_value)
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('main')
    else:
        form = UserRegistrationForm()
    return render(request, 'users/register_user.html', {'form': form})


@login_required
def profile(request):
    # Отображение профиля текущего пользователя
    user = request.user
    context = {
        'user': user,
    }
    return render(request, 'main_page.html', context)


def custom_login(request):
    # Кастомная функция входа пользователя по email и паролю
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('main')
    return render(request, 'users/login.html')
