from django.shortcuts import render

from mainapp.models import Product, ProductCategory


def main(request):
    products= Product.objects.all()[:4]
    content={'title': 'Главная', 'products': products}
    return render(request, 'mainapp/index.html', content)

def products(request,pk=None):

    links_menu = ProductCategory.objects.all()

    content = {
        'title': 'Продукты',
        'links_menu': links_menu
    }
    return render(request, 'mainapp/products.html', content)

def contact(request):
    content = {
        'title': 'Контакты'
    }
    return render(request, 'mainapp/contact.html', content)


