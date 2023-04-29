from django.db import models


class Product(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    price = models.FloatField(default=0)
    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='product')

    def __str__(self):
        return self.title