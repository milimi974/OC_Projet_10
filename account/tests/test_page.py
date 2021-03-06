import pytest
from django.core.paginator import Page
from django.db.models import QuerySet
from django.test import TestCase
from django.urls import reverse

from django.contrib.auth.models import User

from account.forms import UserLoginForm, UserRegisterForm

pytestmark = pytest.mark.django_db


 # Login
class LoginTestCase(TestCase):
    # test if login page return 200
    def test_login_page(self):
        response = self.client.get(reverse('login'))
        # test view render
        self.assertTemplateUsed(response, 'account/form.html')
        # test context variable
        self.failUnless(isinstance(response.context['form'], UserLoginForm))
        # test status page code
        self.assertEqual(response.status_code, 200, 'Should be callable')

# Register
class RegisterTestCase(TestCase):
    # test if Mention legal page return 200
    def test_register_page(self):
        response = self.client.get(reverse('register'))
        # test view render
        self.assertTemplateUsed(response, 'account/form.html')
        # test context variable
        self.failUnless(isinstance(response.context['form'], UserRegisterForm))
        # test status page code
        self.assertEqual(response.status_code, 200, 'Should be callable')

# Profile
class ProfileTestCase(TestCase):
    # test if Mention legal page return 200
    def test_profile_page(self):
        response = self.client.get(reverse('profile'))
        # test view render
        self.assertTemplateUsed(response, 'account/profile.html')
        # test status page code
        self.assertEqual(response.status_code, 200, 'Should be callable')

    # test if profile is updated
    def test_profile_updated(self):
        old_user = User.objects.create_user('foo', 'myemail@test.com', 'bar')
        self.client.login(username='foo', password='bar')
        response = self.client.get(reverse('edit_profile'))
        args = {
            'username': 'foo',
            'email':'myemail@test.com',
            'first_name': "yohan",
            'last_name': "solon",
        }
        response = self.client.post(reverse('edit_profile'), args)
        new_user = User.objects.filter(email='myemail@test.com')[0]

        # test field
        self.assertEqual(new_user.first_name, 'yohan', 'Should be equal')
        self.assertEqual(new_user.last_name, 'solon', 'Should be equal')

    # test changed password
    def test_changed_password(self):
        old_user = User.objects.create_user('foo', 'myemail@test.com', 'bar')
        self.client.login(username='foo', password='bar')
        args = {
            'old_password': 'bar',
            'new_password1': '1234a5678',
            'new_password2': "1234a5678",
        }
        response = self.client.post(reverse('change_password'), args)
        log_in = self.client.login(username='foo', password='1234a5678')
        self.assertTrue(log_in)
        args = {
            'old_password': '1234a5678',
            'new_password1': '1234b5678',
            'new_password2': "1234b5678",
        }
        response = self.client.post(reverse('change_password'), args)
        log_in = self.client.login(username='foo', password='1234b5678')
        self.assertTrue(log_in)

    # test if edit profile page return 200 if user login
    def test_edit_profile_return_200(self):
        user = User.objects.create_user('foo', 'myemail@test.com', 'bar')
        self.client.login(username='foo', password='bar')
        response = self.client.get(reverse('edit_profile'))
        # test view render
        self.assertTemplateUsed(response, 'account/form.html')
        # test status page code
        self.assertEqual(response.status_code, 200, 'Should be callable')

    # test if edit profile page return 302 if user logout
    def test_edit_profile_return_302(self):
        self.client.logout()
        response = self.client.get(reverse('edit_profile'))
        # test status page code
        self.assertEqual(response.status_code, 302, 'Should be redirect')


# User product list
class UserProductTestCase(TestCase):
    # test if User product list page return 200 if user login
    def test_user_product_page_return_200(self):
        user = User.objects.create_user('foo', 'myemail@test.com', 'bar')
        self.client.login(username='foo', password='bar')
        response = self.client.get(reverse('substitution'))
        # test view render
        self.assertTemplateUsed(response, 'account/user_list.html')
        # test context variable
        self.failUnless(isinstance(response.context['user_products'], Page))
        # self.failUnless(isinstance(response.context['user_products'], QuerySet))
        # test status page code
        self.assertEqual(response.status_code, 200, 'Should be callable')


    # test if User product list page return 302 if user isn't login
    def test_user_product_page_return_302(self):
        response = self.client.get(reverse('substitution'))
        self.assertEqual(response.status_code, 302, 'Should be callable')