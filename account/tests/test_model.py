import pytest

from django.test import RequestFactory, TestCase
from django.urls import reverse
from mixer.backend.django import mixer


from django.contrib.auth.models import AnonymousUser, User

from product.models import Category

pytestmark = pytest.mark.django_db

from ..models import *
"""
class TestUserProduct:

    def test_save(self):
        params = {'id': 347, 'sub_id': 1073}
        # create instance of pos request
        req = RequestFactory().post('/account/save', params)
        req.user = User.objects.create_user(
            username='jacob', email='jacob@…', password='top_secret')

        response = save(req)
        assert response.status_code == 200, 'Should be callable'
"""

# UserProduct model
class UserProductTestCase(TestCase):
    def setUp(self):
        User.objects.create_user('foo', 'myemail@test.com', 'bar')
        self.client.login(username='foo', password='bar')
        product_qs = Product.objects.create(name="jus d'orange")
        substitution_qs = Product.objects.create(name="jus de pamplemousse")
        self.product = Product.objects.get(name="jus d'orange")
        self.substitution = Product.objects.get(name="jus de pamplemousse")

    # test that a new user product is made
    def test_new_user_product_is_add(self):
        old_user_products = UserProduct.objects.count()
        args = {
            'id': self.product.id,
            'sub_id':self.substitution.id
        }
        response = self.client.post(reverse('save_product'), args)
        new_user_products = UserProduct.objects.count()
        self.assertEqual(old_user_products + 1, new_user_products)


    # test that a user product belong to substitution
    def test_new_user_product_belong_to_substitution(self):
        args = {
            'id': self.product.id,
            'sub_id': self.substitution.id
        }
        response = self.client.post(reverse('save_product'), args)
        user_product_qs = UserProduct.objects.first()
        substitution_qs = user_product_qs.substitutions.filter(pk=self.substitution.id)
        self.assertEqual(substitution_qs.exists(), True)