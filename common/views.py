from django.shortcuts import render, get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from common.models import Category
from common.serializers import CategorySerializers
from products.models import Product


class CategoryListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        categories = Category.objects.order_by('position')
        serializers = CategorySerializers(categories, many=True)
        return Response(serializers.data)

    def post(self, request):
        serializers = CategorySerializers(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.data, status=status.HTTP_400_BAD_REQUEST)


class CategoryDetailView(APIView):
    def get_object(self, pk):
        return get_object_or_404(Category, pk=pk)

    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        serializers = CategorySerializers(self.get_object(pk))
        return Response(serializers.data)

    def put(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        serializers = CategorySerializers(instance=self.get_object(pk), data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_200_OK)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        category = self.get_object(pk)
        category.delete()
        return Response('Deleted', status=status.HTTP_204_NO_CONTENT)