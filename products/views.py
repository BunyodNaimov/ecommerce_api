from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.filters import SearchFilter, OrderingFilter

from paginations import CustomPageNumberPagination
from products.models import Product
from products.serializers import ProductListSerializer, ProductCreateSerializer


class ProductListCreateView(generics.ListCreateAPIView):
    queryset = Product.objects.order_by('-id')
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
    filterset_fields = ('category', 'brand')
    ordering_fields = ('id', 'price')
    search_fields = ('title', 'category__title', 'brand__title')
    pagination_class = CustomPageNumberPagination

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ProductCreateSerializer

        return ProductListSerializer


class ProductRetrieveView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductListSerializer

    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)


class ProductUpdateView(generics.UpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductCreateSerializer


class ProductDeleteView(generics.DestroyAPIView):
    queryset = Product.objects.all()


class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductListSerializer
    lookup_field = 'slug'

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return ProductCreateSerializer
        return ProductListSerializer

    """
        Shunaqa metodlrini ishlatsak xam bo'ladi
    """
    # def retrieve(self, request, *args, **kwargs):
    #     return super().retrieve(request, *args, **kwargs)
    #
    # def update(self, request, *args, **kwargs):
    #     return super().update(request, *args, **kwargs)
    #
    # def destroy(self, request, *args, **kwargs):
    #     return super().destroy(request, *args, **kwargs)


# class ProductListView(generics.ListAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer
#
#
# class ProductCreateView(generics.CreateAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer


"""
        Class APIView bilan ishlangan viewlar!
"""

#
# class ProductListCreateView(APIView):
#     permission_classes = [IsAuthenticated]
#
#     def get(self, request):
#         products = Product.objects.order_by('-id')
#         serializers = ProductSerializer(products, many=True)
#         return Response(serializers.data)
#
#     def post(self, request):
#         serializers = ProductSerializer(data=request.data)
#         if serializers.is_valid():
#             serializers.save()
#             return Response(serializers.data, status=status.HTTP_201_CREATED)
#         return Response(serializers.data, status=status.HTTP_400_BAD_REQUEST)
#
#
# class ProductDetailView(APIView):
#     def get_object(self, pk):
#         return get_object_or_404(Product, pk=pk)
#
#     def get(self, request, *args, **kwargs):
#         pk = kwargs.get('pk')
#         serializers = ProductSerializer(self.get_object(pk))
#         return Response(serializers.data)
#
#     def put(self, request, *args, **kwargs):
#         pk = kwargs.get('pk')
#         serializers = ProductSerializer(instance=self.get_object(pk), data=request.data)
#         if serializers.is_valid():
#             serializers.save()
#             return Response(serializers.data, status=status.HTTP_200_OK)
#         return Response(serializers.data, status=status.HTTP_400_BAD_REQUEST)
#
#     def delete(self, request, *args, **kwargs):
#         pk = kwargs.get('pk')
#         product = self.get_object(pk)
#         product.delete()
#         return Response('Deleted', status=status.HTTP_404_NOT_FOUND)


"""
        decorator api_view larr bilan ishlangan viewlar!
"""

# @api_view(['GET'])
# def get_products_list(request):
#     products = Product.objects.order_by('-id')  # Bu queryset
#     # products_data = [{'id': product.id, 'title': product.title} for product in products]
#     # Serializer viewda birinchi queryset qabul qiladi va querysetda ko'p malumotlar bo'lgani uchun
#     # many=True qo'shib qo'yamiz
#     serializer = ProductListSerializer(products, many=True)
#     return Response(serializer.data)
#
#
# @api_view(['GET'])
# def get_product(request, slug):
#     product = get_object_or_404(Product, slug=slug)
#     serializer = ProductListSerializer(product)
#     return Response(serializer.data)
#
#
# @api_view(['GET', 'POST'])
# def get_category(request):
#     serializer_class = CategorySerializer
#     categories = Category.objects.order_by('position')
#     serializer = serializer_class(categories, many=True)
#     if request.method == 'POST':
#         serializer = serializer_class(data=request.data)
#         if serializer.is_valid(raise_exception=True):
#             serializer.save()
#     return Response(serializer.data)
#
#
# @api_view(['GET', 'PUT', 'DELETE'])
# def category_detail(request, pk):
#     serializer_class = CategorySerializer
#     instance = get_object_or_404(Category, pk=pk)
#     if request.method == 'PUT':
#         serializer = serializer_class(instance=instance, data=request.data, partial=True)
#         if serializer.is_valid(raise_exception=True):
#             serializer.save()
#             return Response(serializer.data)
#     if request.method == 'DELETE':
#         instance.delete()
#         return Response(f"Category ID {instance.id} deleted.", status=status.HTTP_204_NO_CONTENT)
#     serializer = serializer_class(instance=instance)
#     return Response(serializer.data)
