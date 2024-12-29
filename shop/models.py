from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator

class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    product_name = models.CharField(_("Product Name"), max_length=50)
    meta = models.CharField(_("Meta keywords"), max_length=300)
    brand =models.CharField(_("Brand"), max_length=50,blank=True, null=True)
    alt = models.CharField(_("alt"), max_length=50, blank=True, null=True)
    desc = models.TextField(validators=[MinLengthValidator(50)])
    category = models.CharField(max_length=200)
    price = models.IntegerField()
    prev_price = models.IntegerField()
    image = models.ImageField(upload_to='shop/images')
    
    # New fields for bullet points
    bullet_point_1 = models.CharField(max_length=255, blank=True, null=True)
    bullet_point_2 = models.CharField(max_length=255, blank=True, null=True)
    bullet_point_3 = models.CharField(max_length=255, blank=True, null=True)
    bullet_point_4 = models.CharField(max_length=255, blank=True, null=True)
    bullet_point_5 = models.CharField(max_length=255, blank=True, null=True)
    bullet_point_6 = models.CharField(max_length=255, blank=True, null=True)
    bullet_point_7 = models.CharField(max_length=255, blank=True, null=True)
    bullet_point_8 = models.CharField(max_length=255, blank=True, null=True)
    bullet_point_9 = models.CharField(max_length=255, blank=True, null=True)
    bullet_point_10 = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.product_name


class CartItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ('user', 'product')

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
