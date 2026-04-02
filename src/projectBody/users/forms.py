from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User
class UserRegistrationForm(UserCreationForm):
    # Форма регистрации пользователя с полями username, email, пароль, телефон и адрес
    
    username = forms.CharField(
        label='Имя пользователя*',
        help_text='Требуется ввести уникальное имя, до 25 символов',
        required=True
    )
    
    email = forms.EmailField(
        label='Электронная почта*',
        help_text='Адрес должен содержать символ "@"',
        required=True
    )
    
    password1 = forms.CharField(
        label='Пароль*',
        widget=forms.PasswordInput,
        help_text='Пароль должен содержать не менее 8 символов'
    )
    
    password2 = forms.CharField(
        label='Подтвердите пароль*',
        widget=forms.PasswordInput,
        help_text='Повторите пароль'
    )
    
    phone_number = forms.CharField(
        label='Телефон',
        max_length=15,
        required=True,
        help_text='Формат: +7(999)1234567'
    )

    address = forms.CharField(
        label='Адрес',
        max_length=255,
        required=False,
        help_text='Введите ваш адрес'
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'phone_number', 'address')

    def clean_email(self):
        # Проверка, что email уникален (не зарегистрирован у другого пользователя)
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Этот email уже используется")
        return email
