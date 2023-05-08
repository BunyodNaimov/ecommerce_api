from rest_framework import serializers

from common.models import Category
from products.models import Product


class ProductCategorySerializers(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'title')


class ProductListSerializer(serializers.ModelSerializer):
    # id = serializers.IntegerField(read_only=True)
    category = ProductCategorySerializers()

    class Meta:
        model = Product
        fields = ['id', 'title', 'slug', 'price', 'category']

    # def to_representation(self, instance):
    #     data = super().to_representation(instance)
    #     data["category"] = ProductCategorySerializers(instance.category).data
    #     return data


class ProductCreateSerializer(serializers.ModelSerializer):
    slug = serializers.IntegerField(required=False)

    class Meta:
        model = Product
        fields = ['id', 'title', 'slug', 'price', 'category']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["category"] = ProductCategorySerializers(instance.category).data
        return data
