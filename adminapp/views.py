from multiprocessing import connection

from django.contrib.auth.decorators import user_passes_test
from django.db.models import F
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404

from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView

from adminapp.forms import ShopUserAdminEditForm, ProductCategoryEditForm, ProductEditForm
from authapp.forms import ShopUserRegisterForm
from authapp.models import ShopUser
from mainapp.models import Product, ProductCategory


# @user_passes_test(lambda u: u.is_superuser)
# def user_create(request):
#     if request.method == 'POST':
#         user_form = ShopUserRegisterForm(request.POST, request.FILES)
#         if user_form.is_valid():
#             user_form.save()
#             return HttpResponseRedirect(reverse('admin:users_read'))
#     else:
#         user_form = ShopUserRegisterForm()
#     content = {
#         'form': user_form
#
#     }
#     return render(request, 'adminapp/user_update.html', content)


class UsersListView(ListView):
    model = ShopUser
    template_name = 'adminapp/users.html'

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class UsersCreateView(CreateView):
    model = ShopUser
    template_name = 'adminapp/user_update.html'
    success_url = reverse_lazy('admin:users_read')
    form_class = ShopUserRegisterForm

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


# @user_passes_test(lambda u: u.is_superuser)
# def users(request):
#     users_list = ShopUser.objects.all().order_by('-is_active', '-is_superuser', '-is_staff', 'username')
#     content = {
#         'objects': users_list
#     }
#     return render(request, 'adminapp/users.html', content)
#

class UsersUpdateView(UpdateView):
    model = ShopUser
    template_name = 'adminapp/user_update.html'
    success_url = reverse_lazy('admin:users_read')
    form_class = ShopUserAdminEditForm

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


#
# @user_passes_test(lambda u: u.is_superuser)
# def user_update(request, pk):
#     edit_user = get_object_or_404(ShopUser, pk=pk)
#     if request.method == 'POST':
#         user_form = ShopUserAdminEditForm(request.POST, request.FILES, instance=edit_user)
#         if user_form.is_valid():
#             user_form.save()
#             return HttpResponseRedirect(reverse('admin:users_read'))
#     else:
#         user_form = ShopUserAdminEditForm(instance=edit_user)
#     content = {
#         'form': user_form
#
#     }
#
#     return render(request, 'adminapp/user_update.html', content)


class UsersDeleteView(DeleteView):
    model = ShopUser
    template_name = 'adminapp/user_delete.html'
    success_url = reverse_lazy('admin:users_read')

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.is_active:
            self.object.is_active = False
        else:
            self.object.is_active = True
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


# @user_passes_test(lambda u: u.is_superuser)
# def user_delete(request, pk):
#     user_item = get_object_or_404(ShopUser, pk=pk)
#     if request.method == 'POST':
#         if user_item.is_active:
#             user_item.is_active = False
#         else:
#             user_item.is_active = True
#         user_item.save()
#         return HttpResponseRedirect(reverse('admin:users_read'))
#     content = {
#         'user_to_delete': user_item
#     }
#     return render(request, 'adminapp/user_delete.html', content)


class CategoryCreateView(CreateView):
    model = ProductCategory
    template_name = 'adminapp/category_update.html'
    success_url = reverse_lazy('admin:category_read')
    form_class = ProductCategoryEditForm

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


#
#
# @user_passes_test(lambda u: u.is_superuser)
# def category_create(request):
#     if request.method == 'POST':
#         category_form = ProductCategoryEditForm(request.POST, request.FILES)
#         if category_form.is_valid():
#             category_form.save()
#             return HttpResponseRedirect(reverse('admin:category_read'))
#     else:
#         category_form = ProductCategoryEditForm()
#     content = {
#         'form': category_form
#
#     }
#
#     return render(request, 'adminapp/category_update.html', content)


class CategoriesListView(ListView):
    model = ProductCategory
    template_name = 'adminapp/categories.html'

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return ProductCategory.objects.all().order_by('-is_active')


# @user_passes_test(lambda u: u.is_superuser)
# def categories(request):
#     categories_list = ProductCategory.objects.all().order_by('-is_active')
#     content = {
#         'objects': categories_list
#     }
#     return render(request, 'adminapp/categories.html', content)


class CategoriesUpdateView(UpdateView):
    model = ProductCategory
    template_name = 'adminapp/category_update.html'
    success_url = reverse_lazy('admin:category_read')
    form_class = ProductCategoryEditForm

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Редактирование категории '
        print(context)
        return context

    def form_valid(self, form):
       if 'discount' in form.cleaned_data:
           discount = form.cleaned_data['discount']
           if discount:
               self.object.product_set.update(price=F('price') * (1 - discount / 100))
               db_profile_by_type(self.__class__, 'UPDATE', connection.queries)

       return super().form_valid(form)

#
# @user_passes_test(lambda u: u.is_superuser)
# def category_update(request, pk):
#     edit_category = get_object_or_404(ProductCategory, pk=pk)
#     if request.method == 'POST':
#         update_form = ProductCategoryEditForm(request.POST, request.FILES, instance=edit_category)
#         if update_form.is_valid():
#             update_form.save()
#             return HttpResponseRedirect(reverse('admin:category_read'))
#     else:
#         update_form = ProductCategoryEditForm(instance=edit_category)
#     content = {
#         'form': update_form
#     }
#
#     return render(request, 'adminapp/category_update.html', content)

class CategoryDeleteView(DeleteView):
    model = ProductCategory
    template_name = 'adminapp/category_delete.html'
    success_url = reverse_lazy('admin:category_read')

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.is_active:
            self.object.is_active = False
        else:
            self.object.is_active = True
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


# @user_passes_test(lambda u: u.is_superuser)
# def category_delete(request, pk):
#     category_item = get_object_or_404(ProductCategory, pk=pk)
#     if request.method == 'POST':
#         if category_item.is_active:
#             category_item.is_active = False
#         else:
#             category_item.is_active = True
#         category_item.save()
#         return HttpResponseRedirect(reverse('admin:category_read'))
#     content = {
#         'category_to_delete': category_item
#     }
#     return render(request, 'adminapp/category_delete.html', content)


class ProductCreateView(CreateView):
    model = Product
    template_name = 'adminapp/product_create.html'
    form_class = ProductEditForm



    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_item = get_object_or_404(ProductCategory, pk=self.kwargs['pk'])
        context['category'] = category_item
        title = 'Редактирование товара'
        context['title'] = title
        return context

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        category_pk = self.get_object().category.pk
        return reverse_lazy('admin:products', args=[category_pk])




    # @user_passes_test(lambda u: u.is_superuser)
# def product_create(request, pk):
#     category_item = get_object_or_404(ProductCategory, pk=pk)
#     if request.method == 'POST':
#         product_form = ProductEditForm(request.POST, request.FILES)
#         if product_form.is_valid():
#             product_form.save()
#             return HttpResponseRedirect(reverse('admin:products', args=[pk]))
#     else:
#         product_form = ProductEditForm()
#     content = {
#         'form': product_form,
#         'category': category_item
#     }
#
#     return render(request, 'adminapp/product_update.html', content)


class ProductsListView(ListView):
    model = Product
    template_name = 'adminapp/products.html'

    def get_success_url(self):

        return reverse_lazy('admin:products')

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        qs= super().get_queryset().filter(category=self.kwargs['pk']).order_by('-is_active')

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category= get_object_or_404(ProductCategory, pk=self.kwargs['pk'])
        context['category'] = category

        return context


# @user_passes_test(lambda u: u.is_superuser)
# def products(request, pk):
#     category_item = get_object_or_404(ProductCategory, pk=pk)
#     products_list = Product.objects.filter(category=category_item).order_by('-is_active')
#     content = {
#         'objects': products_list,
#         'category': category_item
#     }
#     return render(request, 'adminapp/products.html', content)


class ProductDetailView(DetailView):
    model = Product
    template_name = 'adminapp/product_detail.html'

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


# @user_passes_test(lambda u: u.is_superuser)
# def product_read(request, pk):
#     products_list = get_object_or_404(Product, pk=pk)
#     content = {
#         'object': products_list
#     }
#     return render(request, 'adminapp/product_detail.html', content)


class ProductUpdateView(UpdateView):
    model = Product
    template_name = 'adminapp/product_update.html'

    form_class = ProductEditForm

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        category_pk = self.get_object().category.pk
        return reverse_lazy('admin:products', args=[category_pk])


# @user_passes_test(lambda u: u.is_superuser)
# def product_update(request, pk):
#     edit_product = get_object_or_404(Product, pk=pk)
#     if request.method == 'POST':
#         update_form = ProductEditForm(request.POST, request.FILES, instance=edit_product)
#         if update_form.is_valid():
#             update_form.save()
#             return HttpResponseRedirect(reverse('admin:products', args=[edit_product.category_id]))
#     else:
#         update_form = ProductEditForm(instance=edit_product)
#     content = {
#         'form': update_form,
#         'category': edit_product.category
#
#     }
#
#     return render(request, 'adminapp/product_update.html', content)


class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'adminapp/product_delete.html'

    def get_success_url(self):
        category_pk = self.get_object().category.pk
        return reverse_lazy('admin:products', args=[category_pk])

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.is_active:
            self.object.is_active = False
        else:
            self.object.is_active = True
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

#
# @user_passes_test(lambda u: u.is_superuser)
# def product_delete(request, pk):
#     edit_product = get_object_or_404(Product, pk=pk)
#     if request.method == 'POST':
#
#         if edit_product.is_active:
#             edit_product.is_active = False
#         else:
#             edit_product.is_active = True
#         edit_product.save()
#         return HttpResponseRedirect(reverse('admin:products', args=[edit_product.category_id]))
#
#     content = {
#         'product_delete': edit_product
#
#     }
#     return render(request, 'adminapp/product_delete.html', content)
