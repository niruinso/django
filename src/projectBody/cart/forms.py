from django import forms

# Генерируем список кортежей для выбора количества товара от 1 до 20
PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 21)]  # [(1, '1'), (2, '2'), ..., (20, '20')]

class CartAddProductForm(forms.Form):
    # Поле для выбора количества товара из заданных вариантов, значение будет преобразовано в int
    quantity = forms.TypedChoiceField(
        choices=PRODUCT_QUANTITY_CHOICES,  # Список вариантов выбора количества
        coerce=int,                       # Преобразовать выбранное значение к типу int
        label='Количество'                # Метка для поля формы
    )
    # Скрытое поле типа Boolean, которое не обязательно к заполнению
    # Используется для указания, нужно ли обновить количество товара (True/False)
    update = forms.BooleanField(
        required=False,                   # Поле не обязательно для заполнения
        initial=False,                   # Значение по умолчанию False
        widget=forms.HiddenInput         # Поле скрытое (не отображается на форме)
    )
