# Generated by Django 4.2.1 on 2023-05-15 09:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0002_brand'),
    ]

    operations = [
        migrations.AlterField(
            model_name='brand',
            name='logo',
            field=models.ImageField(null=True, upload_to='brands'),
        ),
    ]
