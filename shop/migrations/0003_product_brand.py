# Generated by Django 4.2.13 on 2024-09-24 07:30

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_product_bullet_point_1_product_bullet_point_10_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='brand',
            field=models.CharField(default=django.utils.timezone.now, max_length=50, verbose_name='Brand'),
            preserve_default=False,
        ),
    ]