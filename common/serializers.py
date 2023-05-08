from rest_framework import serializers

from common.models import Category


class CategoryParentSerializers(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'title')


class CategorySerializers(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Category
        fields = ('id', 'title', 'position', 'parent')


class CategoryCreateSerializers(serializers.ModelSerializer):
    # slug = serializers.IntegerField(required=False)

    class Meta:
        model = Category
        fields = ('id', 'title', 'position', 'parent')

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["parent"] = CategoryParentSerializers(instance.parent).data
        return data
