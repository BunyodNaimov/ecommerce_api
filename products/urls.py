from django.urls import path

from products.views import ProductListCreateView, ProductRetrieveView, ProductUpdateView, ProductDeleteView, \
    ProductDetailView

app_name = 'products'

urlpatterns = [
    path('', ProductListCreateView.as_view(), name='product_list_create'),
    # path('<int:pk>/', ProductRetrieveView.as_view(), name='product_read'),
    # path('<int:pk>/edit/', ProductUpdateView.as_view(), name='product_edit'),
    # path('<int:pk>/delete/', ProductDeleteView.as_view(), name='product_delete'),
    path('<slug:slug>/', ProductDetailView.as_view(), name='product_detail'),

]
