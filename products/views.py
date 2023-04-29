from django.shortcuts import render, get_object_or_404

from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from products.models import Product, Category
from products.serializers import ProductListSerializer, CategoryListSerializer, ProductDetailSerializer, \
    CategoryDetailSerializer


@api_view(['GET'])
def get_products_list(request):
    products = Product.objects.order_by('-id')  # Bu queryset
    # products_data = [{'id': product.id, 'title': product.title} for product in products]
    # Serializer viewda birinchi queryset qabul qiladi va querysetda ko'p malumotlar bo'lgani uchun
    # many=True qo'shib qo'yamiz
    serializer = ProductListSerializer(products, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_products_category(request):
    categories = Category.objects.all()
    serializer = CategoryListSerializer(categories, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_product_detail(request, pk):
    product = get_object_or_404(queryset=Product, pk=pk)
    serializer = ProductDetailSerializer(product)
    return Response(serializer.data)


@api_view(['GET'])
def get_category_detail(request, pk):
    category = get_object_or_404(queryset=Category, pk=pk)
    serializer = CategoryDetailSerializer(category)
    return Response(serializer.data)
