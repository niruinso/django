from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

@register.filter(name='format_price')
def format_price(value):
    """Форматирует цену: 12345.67 -> 12 345,67 ₽."""
    try:
        price_str = f"{float(value):.2f}".replace('.', ',')
        parts = price_str.split(',')
        integer_part = parts[0]
        formatted_integer_part = ""
        for i, digit in enumerate(reversed(integer_part)):
            if i > 0 and i % 3 == 0:
                formatted_integer_part = " " + formatted_integer_part
            formatted_integer_part = digit + formatted_integer_part
        
        if len(parts) > 1:
            return f"{formatted_integer_part},{parts[1]} ₽"
        else:
            return f"{formatted_integer_part} ₽"
    except (ValueError, TypeError):
        return value