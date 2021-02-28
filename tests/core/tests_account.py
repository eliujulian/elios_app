from django.test import TestCase
from django.template.response import TemplateResponse
from django.http import HttpResponseNotAllowed
from tests.texts_mixins import *
from core.views import *


class AccountDetailViewTest(CreateUserMixin, TestCase):
    def test_get_response_status_same_user(self):
        response = self.client.get(reverse("account-detail"))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response, TemplateResponse)

    def test_post_response_same_user(self):
        response = self.client.post(reverse("account-detail"))
        self.assertEqual(response.status_code, 405)
        self.assertIsInstance(response, HttpResponseNotAllowed)

    def test_get_response_not_logged_in(self):
        self.client.logout()
        response = self.client.get(reverse("account-detail"))
        self.assertEqual(response.status_code, 302)
        self.assertIsInstance(response, HttpResponseRedirect)


class AccountUpdateViewTest(CreateUserMixin, TestCase):
    def test_get_response_status_same_user(self):
        response = self.client.get(reverse("account-update"))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response, TemplateResponse)

    def test_get_response_not_logged_in(self):
        self.client.logout()
        response = self.client.get(reverse("account-update"))
        self.assertEqual(response.status_code, 302)
        self.assertIsInstance(response, HttpResponseRedirect)
        self.assertIn("login", response.url)

    def test_post_response_not_logged_in(self):
        self.client.logout()
        response = self.client.post(reverse("account-update"))
        self.assertEqual(response.status_code, 302)
        self.assertIsInstance(response, HttpResponseRedirect)
        self.assertIn("login", response.url)

    def test_post_response_same_user(self):
        response = self.client.post(reverse("account-update"))
        self.assertEqual(response.status_code, 302)
        self.assertIsInstance(response, HttpResponseRedirect)
        self.assertIn("adam", response.url)

    def test_post_response_same_user_change_first_name(self):
        self.assertEqual(User.objects.get(username="adam").first_name, "Adam")
        response = self.client.post(reverse("account-update"), data={'first_name': "Aron"})
        self.assertEqual(response.status_code, 302)
        self.assertIsInstance(response, HttpResponseRedirect)
        self.assertIn("adam", response.url)
        self.assertEqual(User.objects.get(username="adam").first_name, "Aron")


class AccountDeleteViewTest(CreateUserMixin, TestCase):
    def test_get_response_status_same_user(self):
        response = self.client.get(reverse("account-delete"))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response, TemplateResponse)
        self.assertIsInstance(response.context_data['view'], AccountDeleteView)

    def test_get_response_not_logged_in(self):
        self.client.logout()
        response = self.client.get(reverse("account-delete"))
        self.assertEqual(response.status_code, 302)
        self.assertIsInstance(response, HttpResponseRedirect)
        self.assertIn("login", response.url)

    def test_post_response_not_logged_in(self):
        self.client.logout()
        response = self.client.post(reverse("account-delete"))
        self.assertEqual(response.status_code, 302)
        self.assertIsInstance(response, HttpResponseRedirect)
        self.assertIn("login", response.url)

    def test_post_response_correct_user(self):
        self.assertTrue(User.objects.get(username="adam").is_authenticated)
        response = self.client.post(reverse("account-delete"))
        self.assertEqual(response.status_code, 302)
        self.assertIsInstance(response, HttpResponseRedirect)
        self.assertFalse(User.objects.get(username="adam").is_active)
        self.assertEqual(self.client.get(reverse("landingpage")).status_code, 302)
        self.assertIsInstance(response, HttpResponseRedirect)
