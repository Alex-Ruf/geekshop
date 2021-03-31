from django import template
from django.conf import settings

register = template.Library()


@register.filter(name='media_for_users')
def media_for_users(string):
    if not string:
        string = "user_avatars/default.jpg"
    return f'{settings.MEDIA_URL}{string}'



def media_for_products(string):
    if not string:
        string = "products_images/default.jpg"
    return f'{settings.MEDIA_URL}{string}'


register.filter('media_for_products', media_for_products)