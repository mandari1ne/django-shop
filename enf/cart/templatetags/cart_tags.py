from django import template
from cart.models import Cart

# регистрация библиотеки тегов
register = template.Library()

# регистрирует тег
@register.simple_tag(takes_context=True)
def get_cart_count(context):
    request = context['request']

    if not request.session.session_key:
        return 0

    try:
        cart = Cart.objects.get(session_key=request.session.session_key)
        return cart.total_items
    except Cart.DoesNotExist:
        return 0

# регистрирует фильтр
@register.filter
def multiply(value, arg):
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return 0
