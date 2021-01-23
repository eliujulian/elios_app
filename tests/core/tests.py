from django.test import TestCase
from django.template.response import TemplateResponse
from django.shortcuts import reverse
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseNotAllowed
from tests.texts_mixins import *  # noqa
from core.views import *


class UserDetaiViewTest(CreateUserMixin, TestCase):
    def test_get_response_status_same_user(self):
        response = self.client.get(reverse("user-detail", kwargs={"slug": "adam"}))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response, TemplateResponse)

    def test_post_response(self):
        response = self.client.post(reverse("user-detail", kwargs={"slug": "adam"}))
        self.assertEqual(response.status_code, 405)
        self.assertIsInstance(response, HttpResponseNotAllowed)

    def test_get_response_status_other_user(self):
        response = self.client.get(reverse("user-detail", kwargs={"slug": "bdam"}))
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


class AccountDetailViewTest(CreateUserMixin, TestCase):
    def test_get_response_status_same_user(self):
        response = self.client.get(reverse("account-detail", kwargs={"slug": "adam"}))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response, TemplateResponse)

    def test_post_response_same_user(self):
        response = self.client.post(reverse("account-detail", kwargs={"slug": "adam"}))
        self.assertEqual(response.status_code, 405)
        print(type(response))
        self.assertIsInstance(response, HttpResponseNotAllowed)

    def test_get_response_status_other_user(self):
        response = self.client.get(reverse("account-detail", kwargs={"slug": "bdam"}))
        self.assertEqual(response.status_code, 401)
        self.assertIsInstance(response, HttpResponse)

    def test_get_response_not_logged_in(self):
        self.client.logout()
        response = self.client.get(reverse("account-detail", kwargs={"slug": "adam"}))
        self.assertEqual(response.status_code, 302)
        self.assertIsInstance(response, HttpResponseRedirect)


class AccountUpdateViewTest(CreateUserMixin, TestCase):
    def test_get_response_status_same_user(self):
        response = self.client.get(reverse("account-update", kwargs={"slug": "adam"}))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response, TemplateResponse)

    def test_get_response_status_other_user(self):
        response = self.client.get(reverse("account-update", kwargs={"slug": "bdam"}))
        self.assertEqual(response.status_code, 401)
        self.assertIsInstance(response, HttpResponse)

    def test_get_response_not_logged_in(self):
        self.client.logout()
        response = self.client.get(reverse("account-update", kwargs={"slug": "adam"}))
        self.assertEqual(response.status_code, 302)
        self.assertIsInstance(response, HttpResponseRedirect)
        self.assertIn("login", response.url)

    def test_post_response_not_logged_in(self):
        self.client.logout()
        response = self.client.post(reverse("account-update", kwargs={"slug": "adam"}))
        self.assertEqual(response.status_code, 302)
        self.assertIsInstance(response, HttpResponseRedirect)
        self.assertIn("login", response.url)

    def test_post_response_other_user(self):
        response = self.client.post(reverse("account-update", kwargs={"slug": "bdam"}))
        self.assertEqual(response.status_code, 401)
        self.assertIsInstance(response, HttpResponse)

    def test_post_response_same_user(self):
        response = self.client.post(reverse("account-update", kwargs={"slug": "adam"}))
        self.assertEqual(response.status_code, 302)
        self.assertIsInstance(response, HttpResponseRedirect)
        self.assertIn("adam", response.url)

    def test_post_response_same_user_change_first_name(self):
        self.assertEqual(User.objects.get(username="adam").first_name, "")
        response = self.client.post(reverse("account-update", kwargs={"slug": "adam"}), data={'first_name':"Adam"})
        self.assertEqual(response.status_code, 302)
        self.assertIsInstance(response, HttpResponseRedirect)
        self.assertIn("adam", response.url)
        self.assertEqual(User.objects.get(username="adam").first_name, "Adam")


class AccountDeleteViewTest(CreateUserMixin, TestCase):
    def test_get_response_status_same_user(self):
        response = self.client.get(reverse("account-delete", kwargs={"slug": "adam"}))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response, TemplateResponse)
        self.assertIsInstance(response.context_data['view'], AccountDeleteView)

    def test_get_response_status_other_user(self):
        response = self.client.get(reverse("account-delete", kwargs={"slug": "bdam"}))
        self.assertEqual(response.status_code, 401)
        self.assertIsInstance(response, HttpResponse)


    def test_get_response_not_logged_in(self):
        self.client.logout()
        response = self.client.get(reverse("account-delete", kwargs={"slug": "adam"}))
        self.assertEqual(response.status_code, 302)
        self.assertIsInstance(response, HttpResponseRedirect)
        self.assertIn("login", response.url)

    def test_post_response_other_user(self):
        response = self.client.post(reverse("account-delete", kwargs={"slug": "bdam"}))
        self.assertEqual(response.status_code, 401)
        self.assertIsInstance(response, HttpResponse)

    def test_post_response_not_logged_in(self):
        self.client.logout()
        response = self.client.post(reverse("account-delete", kwargs={"slug": "adam"}))
        self.assertEqual(response.status_code, 302)
        self.assertIsInstance(response, HttpResponseRedirect)
        self.assertIn("login", response.url)
