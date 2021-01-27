from django.test import TestCase
from django.shortcuts import reverse
from django.http import HttpResponseRedirect
from tests.texts_mixins import *
from core.views import AccountRegisterView


class AccountRegisterViewTest(TestCase):
    def test_create_new_user(self):
        username = "Adam"
        password = "123456"
        data = {"username": username, "first_name": "Adam", "last_name": "Test", "password": password}

        # Create account, not yet confirmed
        response = self.client.post(reverse("account-register"), data=data)
        new_user = User.objects.get(username="Adam")
        self.assertEqual(len(new_user.email_confirm_secret), 24)
        self.assertFalse(new_user.is_active)
        self.assertEqual(response.status_code, 302)
        self.assertIn("success", response.url)
        self.assertIn("message", response.url)
        self.assertTrue(new_user.check_password(password))

        # Try login for not confirmed user -> should not word
        new_response = self.client.post(reverse("login-url"), {"username": username, "password": password})
        self.assertEqual(self.client.get(reverse("landingpage")).status_code, 302)
        self.assertFalse(new_response.context['request'].user.is_authenticated)
        self.assertIn('login', new_response.template_name[0])

        # After E-Mail confirmation
        new_user.is_active = True
        new_user.save()
        self.assertTrue(new_user.is_active)
        third_response = self.client.post(reverse("login-url"), {"username": username, "password": password})
        self.assertEqual(third_response.status_code, 302)
        self.assertIsInstance(third_response, HttpResponseRedirect)
        self.assertNotIn("login", third_response.url)

    def test_duplicate_username(self):
        self.assertEqual(0, User.objects.filter(username="Adam").count())
        username = "Adam"
        password = "123456"
        data = {"username": username, "first_name": "Adam", "last_name": "Test", "password": password}
        response = self.client.post(reverse("account-register"), data=data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(1, User.objects.filter(username="Adam").count())
        response = self.client.post(reverse("account-register"), data=data)
        self.assertIsInstance(response.context_data['view'], AccountRegisterView)
        self.assertFalse(response.context_data['form'].is_valid())
        self.assertEqual(1, User.objects.filter(username="Adam").count())

    def test_username_to_short(self):
        username = "a"
        password = "123456"
        data = {"username": username, "first_name": "Adam", "last_name": "Test", "password": password}
        response = self.client.post(reverse("account-register"), data=data)
        self.assertFalse(response.context_data['form'].is_valid())


class AccountConfirmationViewTest(TestCase):
    def test_new_user(self):
        username = "Adam"
        password = "123456"
        data = {"username": username, "first_name": "Adam", "last_name": "Test", "password": password}
        # Create account, not yet confirmed
        self.client.post(reverse("account-register"), data=data)
        self.assertFalse(User.objects.get(username=username).email_confirmed)

        # Request without GET data
        response = self.client.get(reverse("account-confirm"))
        self.assertEqual(response.status_code, 302)
        self.assertIsInstance(response, HttpResponseRedirect)
        self.assertIn("failure", response.url)

        # Request with not existing user
        url = reverse("account-confirm") + "?username=abc"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertIsInstance(response, HttpResponseRedirect)
        self.assertIn("failure", response.url)

        # Request with not existing user and wrong code
        url = reverse("account-confirm") + "?username=abc&confirmation_code=abcdefg"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertIsInstance(response, HttpResponseRedirect)
        self.assertIn("failure", response.url)

        # Request with existing user and wrong code
        url = reverse("account-confirm") + "?username=Adam&confirmation_code=abcdefg"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertIsInstance(response, HttpResponseRedirect)
        self.assertIn("failure", response.url)

        # Request with existing user and no code
        url = reverse("account-confirm") + "?username=Adam"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertIsInstance(response, HttpResponseRedirect)
        self.assertIn("failure", response.url)

    def test_successfull(self):
        username = "Adam"
        password = "123456"
        data = {"username": username, "first_name": "Adam", "last_name": "Test", "password": password}
        # Create account, not yet confirmed
        self.client.post(reverse("account-register"), data=data)
        self.assertFalse(User.objects.get(username=username).email_confirmed)

        # Request with existing user and correct code
        user = User.objects.get(username=username)
        url = reverse("account-confirm") + f"?username={username}&confirmation_code={user.email_confirm_secret}"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertIsInstance(response, HttpResponseRedirect)
        self.assertIn("success", response.url)
        self.assertTrue(User.objects.get(username=username).email_confirmed)

    def test_post(self):
        response = self.client.post(reverse("account-confirm"))
        self.assertEqual(response.status_code, 405)
