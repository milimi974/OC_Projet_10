import pytest
from django.test import TestCase
from mixer.backend.django import mixer
from types import *
from product.models import Category, Product
from django.core import management

pytestmark = pytest.mark.django_db


 # Update Product
class UpdateProductTestCase(TestCase):


    # test that a new product is made
    def test_new_product_is_made(self):
        old_product = Product.objects.count()
        qty = 1
        response = management.call_command('updateproducts', product=qty , category=1, api=True)
        new_product = Product.objects.count()
        self.assertEqual(old_product+qty, new_product)
        old_product = Product.objects.count()
        qty = 10
        response = management.call_command('updateproducts', product=qty, category=1, api=True)
        new_product = Product.objects.count()
        self.assertEqual(old_product + qty, new_product)

    # test that a new category is made
    def test_new_category_is_made(self):
        old_category = Category.objects.count()
        qty = 1
        response = management.call_command('updateproducts', product=1, category=qty, api=True)
        new_category = Category.objects.count()
        self.assertEqual(old_category + qty, new_category)
        old_category = Category.objects.count()

        qty = 10
        add_entry = qty - new_category
        response = management.call_command('updateproducts', product=1, category=qty, api=True)
        new_category = Category.objects.count()
        self.assertEqual(old_category + add_entry, new_category)