from django.urls import path
from adminapp import views as adminapp
app_name = 'adminapp'
urlpatterns = [
    path('users/create/', adminapp.UsersCreateView.as_view(), name='user_create'),
    # path('users/read/', adminapp.users, name='users_read'),
    path('users/read/', adminapp.UsersListView.as_view(), name='users_read'),
    path('users/update/<int:pk>/', adminapp.UsersUpdateView.as_view() , name='user_update'),
    path('users/delete/<int:pk>/', adminapp.UsersDeleteView.as_view(), name='user_delete'),

    path('categories/create/', adminapp.CategoryCreateView.as_view(), name='category_create'),
    path('categories/read/', adminapp.CategoriesListView.as_view(), name='category_read'),
    path('categories/update/<int:pk>/', adminapp.CategoriesUpdateView.as_view(), name='category_update'),
    path('categories/delete/<int:pk>/', adminapp.CategoryDeleteView.as_view(), name='category_delete'),

    path('products/create/<int:pk>/', adminapp.ProductCreateView.as_view(), name='product_create'),
    path('products/read/category/<int:pk>/', adminapp.ProductsListView.as_view(), name='products'),
    path('products/read/<int:pk>/', adminapp.ProductDetailView.as_view(), name='product_read'),
    path('products/update/<int:pk>/', adminapp.ProductUpdateView.as_view(), name='product_update'),
    path('products/delete/<int:pk>/', adminapp.ProductDeleteView.as_view(), name='product_delete'),

]