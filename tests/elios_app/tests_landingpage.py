from django.test import TestCase
from django.template.response import TemplateResponse
from django.shortcuts import reverse
from django.http import HttpResponseRedirect, HttpResponseNotAllowed
from tests.texts_mixins import *


class LandingpageViewTest(CreateUserMixin, TestCase):
    def test_get_response_status_logged_in(self):
        response = self.client.get(reverse("landingpage"))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response, TemplateResponse)

    def test_post_response_status_logged_in(self):
        response = self.client.post(reverse("landingpage"))
        self.assertEqual(response.status_code, 405)
        self.assertIsInstance(response, HttpResponseNotAllowed)

    def test_get_response_not_logged_in(self):
        self.client.logout()
        response = self.client.get(reverse("landingpage"))
        self.assertEqual(response.status_code, 302)
        self.assertIsInstance(response, HttpResponseRedirect)

    def test_post_response_not_logged_in(self):
        self.client.logout()
        response = self.client.post(reverse("landingpage"))
        self.assertEqual(response.status_code, 302)
        self.assertIsInstance(response, HttpResponseRedirect)
