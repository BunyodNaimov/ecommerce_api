# Generated by Django 4.2 on 2023-05-09 11:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_alter_customuser_managers'),
    ]

    operations = [
        migrations.CreateModel(
            name='VerificationCode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=6)),
                ('email', models.EmailField(max_length=254, null=True, unique=True)),
                ('last_sent_time', models.DateTimeField(auto_now=True)),
                ('is_verified', models.BooleanField(default=False)),
                ('expired_at', models.DateTimeField(null=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='verification_codes', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
