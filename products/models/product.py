import random

from django.db import models
from django.utils.text import slugify


class Product(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    price = models.FloatField(default=0)
    category = models.ForeignKey('common.Category', on_delete=models.CASCADE, related_name='product')

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        slug = self.slug
        while self.__class__.objects.first(slug=slug).exists():
            self.slug = f"{slug}--{random.randint(1, 20)}"
        self.slug = slug
        return super().save(*args, **kwargs)
