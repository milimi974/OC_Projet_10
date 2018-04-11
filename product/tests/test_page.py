import pytest
from django.db.models import QuerySet
from django.test import TestCase
from django.urls import reverse
from mixer.backend.django import mixer
from types import *

from product.models import Product

pytestmark = pytest.mark.django_db


 # Search
class SearchTestCase(TestCase):
    def setUp(self):
        product_qs = Product.objects.create(name="pomme")
        self.product = Product.objects.get(name="pomme")

    # test if search page return a 200
    def test_search_page(self):
        response = self.client.get(reverse('search'),{'term':'pomme'})
        # test view render
        self.assertTemplateUsed(response, 'product/search.html')
        # test context variable
        self.failUnless(isinstance(response.context['product'], Product))
        # test status page code
        self.assertEqual(response.status_code, 200, 'Should be callable')

# Show
class ShowTestCase(TestCase):

    def setUp(self):
        product_qs = Product.objects.create(name="pomme")
        self.product = Product.objects.get(name="pomme")


    # test if show page return a 200 if item exist
    def test_show_page_response_200(self):

        product_id = self.product.id
        response = self.client.get(reverse('show', kwargs={'id':product_id,}))
        # test view render
        self.assertTemplateUsed(response, 'product/show.html')
        # test context variable
        self.failUnless(isinstance(response.context['product'], Product))
        # test status page code
        self.assertEqual(response.status_code, 200, 'Should be callable')

    # test if show page return a 404 if items doesn't exists
    def test_show_page_response_404(self):
        product_id = self.product.id + 1
        response = self.client.get(reverse('show', kwargs={'id':product_id,}))
        self.assertEqual(response.status_code, 404, 'Should be callable')
