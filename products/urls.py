from django.urls import path

from products.views import ProductListCreateView, ProductDetailView

app_name = 'products'

urlpatterns = [
    path('', ProductListCreateView.as_view(), name='product_list_create'),
    path('<int:pk>/', ProductDetailView.as_view(), name='product_detail'),

]
