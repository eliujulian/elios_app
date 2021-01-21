from django.test import TestCase, Client
from django.template.response import TemplateResponse
from django.shortcuts import reverse
from django.http import HttpResponseRedirect, HttpResponse
from core.models import User


class CreateUserMixin:
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user("adam", "adam@adam.de", "123456")
        self.user2 = User.objects.create_user("bdam", "adam@adam.de", "123456")
        self.client.login(username="adam", password="123456")


class LandingpageViewTest(CreateUserMixin, TestCase):
    def test_get_response_status_logged_in(self):
        response = self.client.get(reverse("landingpage"))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response, TemplateResponse)

    def test_get_response_not_logged_in(self):
        self.client.logout()
        response = self.client.get(reverse("landingpage"))
        self.assertEqual(response.status_code, 302)
        self.assertIsInstance(response, HttpResponseRedirect)


class UserDetaiViewTest(CreateUserMixin, TestCase):
    def test_get_response_status_same_user(self):
        response = self.client.get(reverse("user-detail", kwargs={"slug": "adam"}))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response, TemplateResponse)

    def test_get_response_status_other_user(self):
        response = self.client.get(reverse("user-detail", kwargs={"slug": "bdam"}))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response, TemplateResponse)

    def test_get_response_not_logged_in(self):
        self.client.logout()
        response = self.client.get(reverse("user-detail", kwargs={"slug": "adam"}))
        self.assertEqual(response.status_code, 302)
        self.assertIsInstance(response, HttpResponseRedirect)


class AccountDetailViewTest(CreateUserMixin, TestCase):
    def test_get_response_status_same_user(self):
        response = self.client.get(reverse("account-detail", kwargs={"slug": "adam"}))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response, TemplateResponse)

    def test_get_response_status_other_user(self):
        response = self.client.get(reverse("account-detail", kwargs={"slug": "bdam"}))
        self.assertEqual(response.status_code, 401)
        self.assertIsInstance(response, HttpResponse)

    def test_get_response_not_logged_in(self):
        self.client.logout()
        response = self.client.get(reverse("account-detail", kwargs={"slug": "adam"}))
        self.assertEqual(response.status_code, 302)
        self.assertIsInstance(response, HttpResponseRedirect)
