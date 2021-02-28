from django.test import TestCase
from django.template.response import TemplateResponse
from django.http import HttpResponseNotAllowed, HttpResponseRedirect
from core.models import *
from tests.texts_mixins import CreateStandardGroupsMixin, CreateUserMixin


class UserModelTest(CreateStandardGroupsMixin, TestCase):
    def test_get_confirm_url(self):
        data = {"username": "adam", "password": "password", "email": "example@eliu.de"}
        self.client.post(reverse("account-register"), data=data)
        user = User.objects.get(username="adam")
        self.assertIn("127.0.0.1", user.get_confirm_url())
        self.assertIn("adam", user.get_confirm_url())
        self.assertIn(user.email_confirm_secret, user.get_confirm_url())


class UserDetaiViewTest(CreateUserMixin, TestCase):
    def test_get_response_status_same_user(self):
        url = reverse("user-detail", kwargs={"slug": "adam"})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response, TemplateResponse)

    def test_post_response(self):
        url = reverse("user-detail", kwargs={"slug": "adam"})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 405)
        self.assertIsInstance(response, HttpResponseNotAllowed)

    def test_get_response_status_other_user(self):
        url = reverse("user-detail", kwargs={"slug": "bdam"})
        print(url)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response, TemplateResponse)

    def test_get_response_user_not_existing(self):
        response = self.client.get(reverse("user-detail", kwargs={"slug": "abc"}))
        self.assertEqual(response.status_code, 404)

    def test_get_response_status_other_user_inactive_account(self):
        self.user2.is_active = False
        self.user2.save()
        response = self.client.get(reverse("user-detail", kwargs={"slug": "bdam"}))
        self.assertEqual(response.status_code, 404)

    def test_get_response_not_logged_in(self):
        self.client.logout()
        response = self.client.get(reverse("user-detail", kwargs={"slug": "adam"}))
        self.assertEqual(response.status_code, 302)
        self.assertIsInstance(response, HttpResponseRedirect)
