from django.test import TestCase
from django.template.response import TemplateResponse
from django.shortcuts import reverse
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseNotAllowed
from tests.texts_mixins import *  # noqa


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
