from django.shortcuts import render, get_object_or_404

from basketapp.models import Basket
from mainapp.models import Product, ProductCategory


def main(request):
    products = Product.objects.all()[:4]
    content = {'title': 'Главная', 'products': products}
    return render(request, 'mainapp/index.html', content)


def products(request, pk=None):
    basket = 0
    if request.user.is_authenticated:
        basket = sum(list(Basket.objects.filter(user=request.user).values_list('quantity', flat=True)))
    links_menu = ProductCategory.objects.all()
    if pk is not None:
        if pk == 0:
            products_list = Product.objects.all().order_by('price')
            category_item = {'name': 'все', 'pk': 0}
        else:
            category_item = get_object_or_404(ProductCategory, pk=pk)
            products_list = Product.objects.filter(category=category_item)
        content = {
            'title': 'Продукты',
            'links_menu': links_menu,
            'products': products_list,
            'category': category_item,
            'basket': basket
        }
        return render(request, 'mainapp/products_list.html', content)

    content = {
        'title': 'Продукты',
        'links_menu': links_menu,
        'basket': basket
    }
    return render(request, 'mainapp/products.html', content)

def contact(request):
    content = {
        'title': 'Контакты'
    }
    return render(request, 'mainapp/contact.html', content)


