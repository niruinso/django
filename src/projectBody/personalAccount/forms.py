from django import forms
from django.contrib.auth.forms import PasswordChangeForm as DjangoPasswordChangeForm
from users.models import User

class CustomPasswordChangeForm(DjangoPasswordChangeForm):
    # Кастомная форма смены пароля с русскими метками и стилями для полей
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['old_password'].label = "Старый пароль"
        self.fields['new_password1'].label = "Новый пароль"
        self.fields['new_password2'].label = "Подтверждение нового пароля"
        for fieldname in ['old_password', 'new_password1', 'new_password2']:
            self.fields[fieldname].help_text = None  # Убираем подсказки по умолчанию
            self.fields[fieldname].widget.attrs.update({'class': 'form-control mb-2'})  # Добавляем классы Bootstrap

class EmailChangeForm(forms.ModelForm):
    # Форма изменения email с кастомным виджетом и меткой
    email = forms.EmailField(
        label="Новый email",
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'example@example.com'})
    )
    class Meta:
        model = User
        fields = ['email']

class PhoneNumberChangeForm(forms.ModelForm):
    # Форма изменения номера телефона с кастомным виджетом и меткой
    phone_number = forms.CharField(
        label="Новый номер телефона",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+7XXXXXXXXXX'})
    )
    class Meta:
        model = User
        fields = ['phone_number']

class AddressChangeForm(forms.ModelForm):
    # Форма изменения адреса с кастомным виджетом и меткой
    address = forms.CharField(
        label="Новый адрес",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ул. Пушкина, д. 1'})
    )
    class Meta:
        model = User
        fields = ['address']

class AvatarUploadForm(forms.Form):
    # Простая форма для загрузки аватара
    avatar = forms.ImageField(label="Загрузите аватар")
