from django.conf import settings
from django.db import models

# Create your models here.
from product.models import Product


class UserProduct(models.Model):
    # settings.AUTH_USER_MODEL identify current login user

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.OneToOneField(Product,related_name='product', on_delete=models.CASCADE, null=True)
    substitutions = models.ManyToManyField(Product, related_name='substitution')

    def __str__(self):
        return '{} : {}'.format(self.user ,self.product)

    class Meta:
        ordering = ['-id']