from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from adminapp.forms import ShopUserAdminEditForm, ProductCategoryEditForm, ProductEditForm
from authapp.forms import ShopUserRegisterForm
from authapp.models import ShopUser
from mainapp.models import Product, ProductCategory


@user_passes_test(lambda u: u.is_superuser)
def user_create(request):
    if request.method == 'POST':
        user_form = ShopUserRegisterForm(request.POST, request.FILES)
        if user_form.is_valid():
            user_form.save()
            return HttpResponseRedirect(reverse('admin:users_read'))
    else:
        user_form = ShopUserRegisterForm()
    content = {
        'form': user_form

    }

    return render(request, 'adminapp/user_update.html', content)


@user_passes_test(lambda u: u.is_superuser)
def users(request):
    users_list = ShopUser.objects.all().order_by('-is_active', '-is_superuser', '-is_staff', 'username')
    content = {
        'objects': users_list
    }
    return render(request, 'adminapp/users.html', content)


@user_passes_test(lambda u: u.is_superuser)
def user_update(request, pk):
    edit_user = get_object_or_404(ShopUser, pk=pk)
    if request.method == 'POST':
        user_form = ShopUserAdminEditForm(request.POST, request.FILES, instance=edit_user)
        if user_form.is_valid():
            user_form.save()
            return HttpResponseRedirect(reverse('admin:users_read'))
    else:
        user_form = ShopUserAdminEditForm(instance=edit_user)
    content = {
        'form': user_form

    }

    return render(request, 'adminapp/user_update.html', content)


@user_passes_test(lambda u: u.is_superuser)
def user_delete(request, pk):
    user_item = get_object_or_404(ShopUser, pk=pk)
    if request.method == 'POST':
        if user_item.is_active:
            user_item.is_active = False
        else:
            user_item.is_active= True
        user_item.save()
        return HttpResponseRedirect(reverse('admin:users_read'))
    content = {
        'user_to_delete': user_item
    }
    return render(request, 'adminapp/user_delete.html', content)


@user_passes_test(lambda u: u.is_superuser)
def category_create(request):
    if request.method == 'POST':
        category_form = ProductCategoryEditForm(request.POST, request.FILES)
        if category_form.is_valid():
            category_form.save()
            return HttpResponseRedirect(reverse('admin:category_read'))
    else:
        category_form = ProductCategoryEditForm()
    content = {
        'form': category_form

    }

    return render(request, 'adminapp/category_update.html', content)


@user_passes_test(lambda u: u.is_superuser)
def categories(request):
    categories_list = ProductCategory.objects.all().order_by('-is_active')
    content = {
        'objects': categories_list
    }
    return render(request, 'adminapp/categories.html', content)


@user_passes_test(lambda u: u.is_superuser)
def category_update(request, pk):
    edit_category = get_object_or_404(ProductCategory, pk=pk)
    if request.method == 'POST':
        update_form = ProductCategoryEditForm(request.POST, request.FILES, instance=edit_category)
        if update_form.is_valid():
            update_form.save()
            return HttpResponseRedirect(reverse('admin:category_read'))
    else:
        update_form = ProductCategoryEditForm(instance=edit_category)
    content = {
        'form': update_form
    }

    return render(request, 'adminapp/category_update.html', content)


@user_passes_test(lambda u: u.is_superuser)
def category_delete(request, pk):
    category_item = get_object_or_404(ProductCategory, pk=pk)
    if request.method == 'POST':
        if category_item.is_active:
            category_item.is_active = False
        else:
            category_item.is_active = True
        category_item.save()
        return HttpResponseRedirect(reverse('admin:category_read'))
    content = {
        'category_to_delete': category_item
    }
    return render(request, 'adminapp/category_delete.html', content)


@user_passes_test(lambda u: u.is_superuser)
def product_create(request, pk):
    category_item = get_object_or_404(ProductCategory, pk=pk)
    if request.method == 'POST':
        product_form = ProductEditForm(request.POST, request.FILES)
        if product_form.is_valid():
            product_form.save()
            return HttpResponseRedirect(reverse('admin:products', args=[pk]))
    else:
        product_form = ProductEditForm()
    content = {
        'form': product_form,
        'category':category_item
    }

    return render(request, 'adminapp/product_update.html', content)


@user_passes_test(lambda u: u.is_superuser)
def products(request, pk):
    category_item = get_object_or_404(ProductCategory, pk=pk)
    products_list = Product.objects.filter(category=category_item).order_by('-is_active')
    content = {
        'objects': products_list,
        'category': category_item
    }
    return render(request, 'adminapp/products.html', content)


@user_passes_test(lambda u: u.is_superuser)
def product_read(request, pk):
    products_list = get_object_or_404(Product, pk=pk)
    content = {
        'object': products_list
    }
    return render(request, 'adminapp/product_detail.html', content)


@user_passes_test(lambda u: u.is_superuser)
def product_update(request, pk):
    edit_product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        update_form = ProductEditForm(request.POST, request.FILES, instance=edit_product)
        if update_form.is_valid():
            update_form.save()
            return HttpResponseRedirect(reverse('admin:products', args=[edit_product.category_id]))
    else:
        update_form = ProductEditForm(instance=edit_product)
    content = {
        'form': update_form,
        'category': edit_product.category

    }

    return render(request, 'adminapp/product_update.html', content)


@user_passes_test(lambda u: u.is_superuser)
def product_delete(request, pk):
    edit_product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':

        if edit_product.is_active:
            edit_product.is_active = False
        else:
            edit_product.is_active = True
        edit_product.save()
        return HttpResponseRedirect(reverse('admin:products', args=[edit_product.category_id]))


    content = {
        'product_delete': edit_product

    }
    return render(request, 'adminapp/product_delete.html', content)
