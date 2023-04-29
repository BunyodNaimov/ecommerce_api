from django.urls import path

from products.views import get_products_list, get_products_category, get_product_detail, get_category_detail

app_name = 'products'


urlpatterns = [
    path('products/', get_products_list, name='product_list'),
    path('product/<int:pk>/', get_product_detail, name='product_detail'),
    path('categories/', get_products_category, name='category_list'),
    path('category/<int:pk>/', get_category_detail, name='category_detail'),
]
